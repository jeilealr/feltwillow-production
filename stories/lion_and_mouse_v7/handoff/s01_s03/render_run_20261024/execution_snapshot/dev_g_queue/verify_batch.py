import json,shlex,subprocess,sys
from pathlib import Path
import imageio_ffmpeg
launch=Path('/flash/project_465002727/jelealro/feltwillow-production/launch/20261023')
lines=(launch/'tasks.txt').read_text().splitlines()
for index in map(int,sys.argv[1:]):
    cmd=shlex.split(lines[index])
    proc=subprocess.run([sys.executable,*cmd[1:],'--audit-existing'],capture_output=True,text=True,check=True)
    audit=json.loads(proc.stdout)
    assert all(r['status']=='complete' for r in audit['seeds']),audit
    for seed in audit['seeds']:
        reader=imageio_ffmpeg.read_frames(seed['output'])
        meta=next(reader)
        count=sum(1 for _ in reader)
        assert count==81 and meta['size']==(1280,720) and meta['fps']==16,(meta,count)
        print(json.dumps(dict(task=index,output=seed['output'],receipt='verified',decoded_frames=count)),flush=True)
