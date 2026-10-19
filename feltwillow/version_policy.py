"""Shared version-boundary checks for stories with independent source assets."""

INDEPENDENT_STORIES = {"lion_and_mouse_v6", "lion_and_mouse_v7"}


def require_story_local_audio(story: str, audio_story: str, *, consumer: str = "") -> None:
    """Require audio staged under an independent story's runtime namespace.

    Source-recording provenance is a separate, hash-bound decision in that
    story's audio manifest (v6 explicitly retains the unchanged v5 English
    recordings). This check concerns the path consumed by the runtime.
    """
    if story in INDEPENDENT_STORIES and audio_story != story:
        context = f" in {consumer}" if consumer else ""
        raise SystemExit(
            f"VERSION_ISOLATION_FAILURE{context}: {story} requires audio staged "
            "in its own runtime namespace; "
            f"got {audio_story!r}."
        )
