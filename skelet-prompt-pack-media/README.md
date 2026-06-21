# skelet-prompt-pack-media

A `skelet` prompt pack for generative-media prompting: turn a loose idea
into a structured spec ready for a downstream generator.

| Skill | Spec | For |
|---|---|---|
| `skills/image` | `ImagePromptSpec` | text-to-image models (Midjourney, DALL-E, Stable Diffusion, ...) |
| `skills/video` | `VideoPromptSpec` | text-to-video models (Sora, Runway, Veo, ...) |
| `skills/object_3d` | `Object3DPromptSpec` | text-to-3D models (Meshy, Tripo, ...) |
| `skills/sprite_sheet` | `SpriteSheetPromptSpec` | 2D/pixel-art sprite generators |

Each skill is advisory: it shapes an LLM's structured output into a
well-formed spec, but doesn't generate pixels/meshes itself — that's the
downstream generator's job.

```bash
pip install skelet-prompt-pack-media
```

```python
from skelet_prompt_pack_media.skills.video import VIDEO_SKILL, VideoPromptSpec

system_prompt = VIDEO_SKILL.render_body()
# ... send system_prompt + the user's idea to your model, get back a VideoPromptSpec ...
```

Depends only on `skelet` core primitives. See the main repo's
[CONTRIBUTING.md](../CONTRIBUTING.md) for the `tools/`/`skills/` layout
convention this pack follows.
