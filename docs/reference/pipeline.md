# Image Pipeline Reference

Path: `virtual_influencer_engine/core/image_gen/pipeline.py`

## Class: `ImageGenerator`

Handles the creation of images via external APIs (Replicate, OpenAI).

### Configuration (`.env`)
*   `REPLICATE_API_TOKEN`: Required for FLUX.1.
*   `REPLICATE_MODEL_VERSION`: The full ID of the model (Base or LoRA).

### Methods

#### `__init__(self, provider="replicate")`
*   Initializes the client.
*   Defaults to "replicate" for high-quality FLUX generation.

#### `generate_image(self, prompt: str, aspect_ratio="1:1") -> str`
Generates an image and returns a public URL.

*   **Logic**:
    1.  **Enhancement**: Appends stylistic keywords ("cinematic lighting", "film grain").
    2.  **LoRA Injection**: If a custom model is detected (not `flux-pro`), it injects the trigger word and gender anchor: `photo of TOK, a young woman, ...`
    3.  **API Call**: Sends request to Replicate.
*   **Returns**: URL string of the generated image.

#### `download_image(self, url: str) -> str`
Downloads the image from the remote URL to a temporary local file.
*   **Why**: Twitter API requires local file upload, it cannot download from URLs directly.
*   **Returns**: Absolute path to the local temporary file.
