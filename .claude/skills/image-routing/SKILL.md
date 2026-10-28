---
name: image-routing
description: Route image work between artistic GPT operations and technical coding work, with explicit handoff when capabilities are unavailable.
---

Use GPT with the actual required image capabilities for artwork generation, artistic edits/inpainting, character appearance changes, and subjective assessment of design, anatomy, style, composition or visual consistency. Final artwork selection, canonical revisions and production acceptance belong to the human owner.

A coding model such as DeepSeek may inspect image files and metadata, calculate hashes, write processing/compositing software, build diagnostics/contact sheets/HTML reviews, and run technical tests. Working with image files alone does not require artistic routing.

For mixed tasks, do the technical preparation, then hand off the artistic operation to a capable GPT session. Include the requested operation, exact input paths/hashes and reference roles, constraints, output destination, spending limits and owner approval needed. If capabilities or authorization are missing, stop that operation with the handoff ready. Never claim a model switch, visual inspection or generated result that did not occur.

`scripts/route.py` provides an offline route for an explicitly classified operation. It does not classify free text, switch models, call providers, or grant permission. Deterministic diagnostics and crops are technical; selecting an aesthetically preferred result is artistic assessment.
