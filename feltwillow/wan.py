"""Wan 2.2 (A14B, mixture of experts) through diffusers.

Everything learned running it on LUMI lives here:

* Only the I2V-A14B pipeline honours `last_image`. The TI2V-5B path
  (`expand_timesteps`) silently drops it, so first+last keyframing needs A14B.
* Two 14B experts plus the 11B text encoder do not fit one 64 GB MI250X GCD:
  weights are offloaded per module (`enable_model_cpu_offload`), which needs
  ~80-100 GB of host RAM per process.
* The Hugging Face repos ship fp32; loading converts to bf16 (10-20 min).
* Clips are 4k+1 frames at 16 fps. 81 frames is the native length; longer
  clips cost quadratically in attention (97 frames ran ~250 s/step and could
  not finish inside a 3 h dev-g job), and need VAE tiling to decode.
* Guidance is a pair: high-noise expert, low-noise expert.
  I2V default (3.5, 3.5); T2V default (4.0, 3.0).
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

MODELS = {
    "i2v": "Wan-AI/Wan2.2-I2V-A14B-Diffusers",
    "t2v": "Wan-AI/Wan2.2-T2V-A14B-Diffusers",
}
# Hugging Face repos can change under the same name; a pinned commit keeps a
# seed reproducible. Update deliberately, and note it in docs/findings-and-risks.md.
REVISIONS = {
    "i2v": "596658fd9ca6b7b71d5057529bbf319ecbc61d74",
    "t2v": "5be7df9619b54f4e2667b2755bc6a756675b5cd7",
}
# Wan2.2-Lightning (lightx2v, Apache-2.0): 4-step distillation LoRAs for I2V
# A14B. Reference settings (their ComfyUI workflow): 4 Euler steps, shift 5,
# CFG 1 (no negative pass), high-noise expert steps 0-2, low-noise 2-4, which is
# what boundary_ratio 0.9 gives with these timesteps (1000, 937 | 833, 625).
LIGHTNING = dict(
    repo="lightx2v/Wan2.2-Lightning", revision="18bccf8884ec0a078eed79785eb4ef13ea16ce1e",
    folder="Wan2.2-I2V-A14B-4steps-lora-rank64-Seko-V1",
    render=dict(steps=4, guidance=1.0, guidance_2=1.0), shift=5.0,
)
NATIVE_FRAMES = 81
FPS = 16


def check_frames(n: int) -> None:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or (n - 1) % 4:
        raise ValueError(f"Wan needs 4k+1 frames, got {n}")


def preflight(*, width, height, frames, steps, guidance, guidance_2,
              max_frames=None):
    """Validate the supported recipe without importing a model or framework."""
    check_frames(frames)
    if max_frames is not None and frames > max_frames:
        raise ValueError(f"frames {frames} exceed the declared resource bound {max_frames}")
    for name, value in (("width", width), ("height", height)):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0 or value % 16:
            raise ValueError(f"{name} must be a positive multiple of 16")
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise ValueError("steps must be a positive integer")
    if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v < 0 for v in (guidance, guidance_2)):
        raise ValueError("guidance must be finite and nonnegative")


def fitted_record(image, width, height):
    """Versioned RGB row-major pixel identity, distinct from file identity."""
    if "A" in image.getbands() and image.getchannel("A").getextrema() != (255, 255):
        raise ValueError("transparent scene inputs require an explicitly reviewed background")
    if image.mode == "P" and "transparency" in image.info:
        raise ValueError("transparent palette scene inputs are unsupported")
    fitted = fit(image, width, height)
    header = f"feltwillow.rgb.v1\nRGB\n{width} {height}\n".encode()
    return dict(schema="feltwillow.rgb.v1", mode="RGB", width=width, height=height,
                source_size=list(image.size), crop_box=fit_box(image.size,width,height), transform="center-crop-lanczos-rgb-v1",
                pixel_sha256=hashlib.sha256(header + fitted.tobytes()).hexdigest())


def endpoint_capability(pipe):
    """Inspect the actual loaded configuration; unknown is never support."""
    import inspect
    config = getattr(pipe, "config", {})
    expand = config.get("expand_timesteps") if hasattr(config, "get") else None
    supported = "last_image" in inspect.signature(pipe.__call__).parameters and expand is False
    source=inspect.getsourcefile(type(pipe))
    return dict(source_path=source,source_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest() if source and Path(source).is_file() else None, pipeline_class=f"{type(pipe).__module__}.{type(pipe).__name__}",
                expand_timesteps=expand, endpoint_supported=supported)


def fit_box(size, width, height):
    """Exact integer source crop used by fit, before RGB conversion/resizing."""
    w,h=size
    if w/h > width/height:
        nw=int(round(h*width/height));return [(w-nw)//2,0,(w-nw)//2+nw,h]
    if w/h < width/height:
        nh=int(round(w*height/width));return [0,(h-nh)//2,w,(h-nh)//2+nh]
    return [0,0,w,h]


def fit(image, width: int, height: int):
    """Centre-crop a PIL image to the target aspect, then resize."""
    from PIL import Image

    w, h = image.size
    target = width / height
    if w / h > target:
        nw = int(round(h * target))
        image = image.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    elif w / h < target:
        nh = int(round(w / target))
        image = image.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return image.convert("RGB").resize((width, height), Image.LANCZOS)


def model_id(kind: str) -> str:
    """`repo@commit`, for sidecars."""
    return f"{MODELS[kind]}@{REVISIONS[kind]}"


def lightning_lora() -> dict:
    from huggingface_hub import hf_hub_download

    def get(name: str) -> Path:
        return Path(hf_hub_download(LIGHTNING["repo"], f"{LIGHTNING['folder']}/{name}",
                                    revision=LIGHTNING["revision"]))

    return dict(name="lightning", high=get("high_noise_model.safetensors"),
                low=get("low_noise_model.safetensors"), weight=1.0)


def load(kind: str, frames: int = NATIVE_FRAMES, loras: list[dict] | None = None,
         fast: bool = False):
    """`loras`: [{name, high, low, weight}], musubi-tuner files (one per expert).

    A LoRA trained on T2V A14B loads into I2V A14B too: it only touches the
    attention and FFN layers, which have the same shapes in both (checked: all
    400 targets exist in both experts). diffusers' `transformer` is the
    high-noise expert, `transformer_2` the low-noise one. musubi's alpha/rank is
    folded into the weights by the converter, so an adapter weight of 1.0 means
    "as trained".
    """
    import torch
    from diffusers import AutoencoderKLWan, WanImageToVideoPipeline, WanPipeline

    repo, rev = MODELS[kind], REVISIONS[kind]
    vae = AutoencoderKLWan.from_pretrained(repo, subfolder="vae", revision=rev,
                                           torch_dtype=torch.float32)
    cls = WanImageToVideoPipeline if kind == "i2v" else WanPipeline
    pipe = cls.from_pretrained(repo, vae=vae, revision=rev, torch_dtype=torch.bfloat16)
    if fast:                                   # 4-step Lightning (see LIGHTNING)
        from diffusers import FlowMatchEulerDiscreteScheduler

        loras = [*(loras or []), lightning_lora()]
        pipe.scheduler = FlowMatchEulerDiscreteScheduler(num_train_timesteps=1000,
                                                         shift=LIGHTNING["shift"])
    if loras:
        for lo in loras:
            for path, second in ((Path(lo["high"]), False), (Path(lo["low"]), True)):
                pipe.load_lora_weights(str(path.parent), weight_name=path.name,
                                       adapter_name=lo["name"], load_into_transformer_2=second)
        names, weights = [lo["name"] for lo in loras], [lo.get("weight", 1.0) for lo in loras]
        pipe.transformer.set_adapters(names, weights)
        pipe.transformer_2.set_adapters(names, weights)
        for part in ("transformer", "transformer_2"):     # assert, don't assume
            layers = [m for m in getattr(pipe, part).modules() if hasattr(m, "lora_A")]
            active = {n for m in layers for n in m.lora_A.keys()}
            if len(layers) < 400 or not set(names) <= active:
                raise RuntimeError(f"LoRA not applied to {part}: {len(layers)} layers, {active}")
            print(f"LoRA {names} on {part}: {len(layers)} layers", flush=True)
    pipe.enable_model_cpu_offload()
    if frames > NATIVE_FRAMES:
        pipe.vae.enable_tiling()
    return pipe


def generate(pipe, prompt: str, *, negative: str, width: int, height: int, frames: int,
             steps: int, guidance: float, guidance_2: float, seed: int,
             image=None, last_image=None):
    """Returns a list of PIL frames. `image`/`last_image` only for I2V."""
    import torch

    preflight(width=width, height=height, frames=frames, steps=steps,
              guidance=guidance, guidance_2=guidance_2)
    if last_image is not None and not endpoint_capability(pipe)["endpoint_supported"]:
        raise ValueError("active pipeline/configuration does not establish last-image support")
    kwargs = dict(prompt=prompt, negative_prompt=negative, height=height, width=width,
                  num_frames=frames, num_inference_steps=steps, guidance_scale=guidance,
                  guidance_scale_2=guidance_2,
                  generator=torch.Generator(device="cpu").manual_seed(seed))
    if image is not None:
        kwargs["image"] = fit(image, width, height)
    if last_image is not None:
        kwargs["last_image"] = fit(last_image, width, height)
    return pipe(**kwargs).frames[0]


def save(frames, path: Path, fps: int = FPS) -> None:
    from diffusers.utils import export_to_video

    path.parent.mkdir(parents=True, exist_ok=True)
    export_to_video(frames, str(path), fps=fps)


def save_native_boundary(frame, path):
    """Preserve the pre-encoder object; float arrays remain lossless NPY.

    A PNG preview for an array is explicitly quantized and is not the native
    continuation source. PIL RGB objects are already eight-bit pixel images.
    """
    import numpy as np
    from PIL import Image
    path=Path(path)
    if isinstance(frame,Image.Image):
        frame.save(path)
        return dict(path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                    origin='model_native_before_encoding',representation='PIL '+frame.mode)
    array=np.asarray(frame)
    if array.ndim!=3 or array.shape[2]!=3 or not np.isfinite(array).all():
        raise ValueError('unexpected native frame shape or nonfinite pixels')
    native=path.with_suffix('.npy');np.save(native,array,allow_pickle=False)
    if np.issubdtype(array.dtype,np.floating):
        if array.min()<0 or array.max()>1:raise ValueError('unexpected native float pixel range')
        preview=(array*255).round().astype('uint8')
    elif array.dtype==np.uint8:preview=array
    else:raise ValueError('unsupported native pixel dtype')
    Image.fromarray(preview).save(path)
    return dict(path=str(native),sha256=hashlib.sha256(native.read_bytes()).hexdigest(),
                origin='model_native_before_encoding',representation=str(array.dtype),shape=list(array.shape),
                preview_path=str(path),preview_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                preview_conversion='float [0,1] *255 rounded to RGB8' if array.dtype!=np.uint8 else 'RGB8 lossless')


def verify_endpoint_environment(record):
    """Check frozen inspected source/cache bytes before importing/loading weights."""
    import json
    if record.get('endpoint_supported') is not True or record.get('expand_timesteps') is not False:
        raise ValueError('endpoint source/config evidence missing')
    for name in ('source','config'):
        path=Path(record.get(name+'_path',''))
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=record.get(name+'_sha256'):
            raise ValueError('installed '+name+' differs from the frozen endpoint evidence')
    config=json.loads(Path(record['config_path']).read_text())
    if config.get('_class_name')!='WanImageToVideoPipeline' or config.get('expand_timesteps',False) is not False:
        raise ValueError('cached model does not support the reviewed endpoint path')
    if record.get('model_revision')!=REVISIONS['i2v']:
        raise ValueError('model revision differs from capability evidence')
    return {'source_sha256':record['source_sha256'],'config_sha256':record['config_sha256'],'model_revision':record['model_revision']}


def package_environment():
    """Installed metadata only; no framework import, download or device query."""
    import importlib.metadata
    import platform
    import sys
    versions={}
    for name in ('diffusers','torch','transformers','accelerate','peft','numpy'):
        try:versions[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:versions[name]='unavailable'
    return dict(python=sys.version,executable=sys.executable,prefix=sys.prefix,
                platform=platform.platform(),machine=platform.machine(),packages=versions)
