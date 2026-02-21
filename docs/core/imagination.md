# The Imagination (Image Generation)

> [!NOTE]
> **Current State (as of 2026-02-20):** The only active image provider is **FLUX 1 via Replicate** (remote API). Local/offline generation is not supported at this time. DALL-E 3 is available as a fallback if `REPLICATE_API_TOKEN` is not set.

The "Imagination" module converts text prompts into photorealistic images. It is powered by **FLUX.1** running on **Replicate**, augmented with custom **LoRA (Low-Rank Adaptation)** models for identity consistency.

## Architecture

1.  **Prompt Engineering**: The system takes a basic description (e.g., "Sienna running on the beach") and enhances it with stylistic keywords ("cinematic lighting", "film grain", "f/1.8", "shot on 35mm").
2.  **Gender Anchor**: If using a custom LoRA, the system automatically injects "a young woman" into the prompt to prevent gender drift (a common issue with fine-tuned models).
3.  **Generation**: The enhanced prompt is sent to `replicate.com`'s API.
4.  **Download & Temp Storage**: The resulting image URL is downloaded to a temporary local file for upload to social platforms.

## FLUX.1 & LoRA

We use **FLUX.1 [dev]** or **FLUX.1.1 [pro]** as the base model because of its superior realism and text adherence compared to SDXL.

### Custom LoRA (Sienna Fox)
To maintain the same face across thousands of images, we trained a LoRA adapter.
*   **Trigger Word**: `TOK` (or specific token used during training).
*   **Training Data**: 52 synthetic images generated via Midjourney/Flux with consistent facial features.

## Key Files
*   `core/image_gen/pipeline.py`: The `ImageGenerator` class.
