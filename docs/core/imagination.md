# The Imagination (Image Generation)

> [!NOTE]
> **Current State (as of 2026-02-28):** The active image provider is **FLUX 1 via Replicate** (remote API). DALL-E 3 is available as a fallback if `REPLICATE_API_TOKEN` is not set.

The "Imagination" module converts text prompts into photorealistic images. It is powered by **FLUX.1** running on **Replicate**, augmented with custom **LoRA (Low-Rank Adaptation)** models for identity consistency.

## Architecture

1.  **Prompt Engineering**: The system takes a basic description (e.g., "Sienna running on the beach") and enhances it with stylistic keywords ("cinematic lighting", "film grain", "f/1.8", "shot on 35mm").
2.  **Content Safety Filter**: The prompt is checked to ensure it does **not** describe lingerie, underwear, bikinis, or revealing clothing. Only appropriate outfits are allowed (casual, athletic, streetwear, dresses).
3.  **Hand Safety Injection**: When the prompt involves holding objects (coffee, phone), the system automatically adjusts the composition to minimize AI hand artifacts.
4.  **Gender Anchor**: If using a custom LoRA, the system automatically injects "a young woman" into the prompt to prevent gender drift.
5.  **Generation**: The enhanced prompt is sent to `replicate.com`'s API.
6.  **Quality Control (Critic)**: A GPT-4o-mini-powered Image Critic evaluates the generated image for quality. If it fails (e.g., distorted hands, blurry face), the system retries up to 3 times.

## FLUX.1 & LoRA

We use **FLUX.1 [dev]** or **FLUX.1.1 [pro]** as the base model because of its superior realism and text adherence compared to SDXL.

### Custom LoRA (Sienna Fox)
To maintain the same face across thousands of images, we trained a LoRA adapter.
*   **Trigger Word**: `TOK` (or specific token used during training).
*   **Training Data**: 52 synthetic images generated via Midjourney/Flux with consistent facial features.

## Threads Text-Only Mode

When posting to Threads, the image generation is **skipped ~70% of the time** (controlled by `THREADS_TEXT_ONLY_RATIO`). This means:

*   70% of Threads posts are **text-only** (no image generation cost).
*   30% include an image, reused from the shared generation if posting to multiple platforms.

## Key Files
*   `core/image_gen/pipeline.py`: The `ImageGenerator` class (generation + critic loop).
*   `core/image_gen/critic.py`: The `ImageCritic` class (GPT-4o-mini quality control).
