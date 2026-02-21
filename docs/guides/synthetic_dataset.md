# Creating a Synthetic Dataset

If you don't have real photos of a model, you can create a "Digital Twin" from scratch using AI. This guide explains how to generate a consistent dataset for LoRA training.

## The Strategy: "The Perfect Seed"

The goal is to find one specific random seed that generates a face you love, and then re-use that seed across different prompts to keep the face consistent.

### Step 1: Find the Face
1.  **Craft a detailed prompt**: Include specific facial features (e.g., "hazel eyes", "small scar on eyebrow", "freckles").
    > "A hyper-realistic close-up portrait of a 25-year-old woman with dirty blonde messy hair and hazel eyes. She has a symmetric face, sun-kissed skin texture, natural freckles. Soft natural lighting, 85mm lens."
2.  **Generate with FLUX.1**: Use Replicate to run this prompt multiple times.
3.  **Select the Winner**: Pick the face that embodies your character perfectly. **Save the Seed number.**

### Step 2: Generate Variations
Now, generate 15-20 images using the **SAME SEED** but slightly modifying the context.

*   **Close-ups (10 images)**: Keep the prompt almost identical, maybe change lighting slightly.
*   **Half-Body (5 images)**: "A medium shot of [description...] wearing a t-shirt".
*   **Full-Body (5 images)**: "A full body shot of [description...] walking in the city".

**Crucial**: Do not change the facial description part of the prompt.
Discard any images where the face looks different.

### Step 3: Prepare for Training
1.  **Crop**: Ensure faces are clear.
2.  **Rename**: `sienna_01.jpg`, `sienna_02.jpg`, etc.
3.  **Zip**: Compress them into `dataset.zip`.

You are now ready to train your LoRA!
