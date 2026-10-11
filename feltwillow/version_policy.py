"""Shared version-boundary checks for stories with independent source assets."""

INDEPENDENT_STORIES = {"lion_and_mouse_v6"}


def require_story_local_audio(story: str, audio_story: str, *, consumer: str = "") -> None:
    """Reject another story's recordings for a production with independent audio."""
    if story in INDEPENDENT_STORIES and audio_story != story:
        context = f" in {consumer}" if consumer else ""
        raise SystemExit(
            f"VERSION_ISOLATION_FAILURE{context}: {story} requires its own audio; "
            f"got {audio_story!r}."
        )
