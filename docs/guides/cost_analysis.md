# Cost Analysis (Operational Expenses)

This document breaks down the estimated monthly cost to run Zirelia, assuming a target of **3 posts per day**.

## 1. The Brain (OpenAI API) 🧠
Used for generating text, captions, and internal monologue.
*   **Model**: GPT-4o-mini (highly capable for social posts and much cheaper than GPT-4).
*   **Cost**:
    *   Input: \$0.15 / 1M tokens
    *   Output: \$0.60 / 1M tokens
*   **Usage**: ~1,000 tokens per post (very generous estimate).
*   **Monthly**: 3 posts * 30 days = 90 posts. 90,000 tokens.
*   **Total**: < **$0.10 / month** (Negligible).

## 2. The Imagination (Replicate API) 🎨
Used for generating images with FLUX.1 [dev] or [pro] and your custom LoRA.
*   **Model**: `ostris/flux-dev-lora-trainer` (inference).
*   **Cost**: ~$0.025 - $0.04 per image.
*   **Usage**: 90 images per month.
*   **Calculation**: 90 * $0.04 = $3.60.
*   **Buffer**: +20% for failed generations / tests.
*   **Total**: ~ **$4.50 / month**.

## 3. The Hands (Twitter/X API) 🐦
*   **Pay-as-you-go**: You are currently on a metered plan (Credit System).
*   **Cost**: ~$0.01 per post.
*   **Calculation**: 90 posts * $0.01 = $0.90.
*   **Total**: ~ **$1.00 / month**.

## 4. Remotion (Video Rendering) 🎬
*(If implemented in future Phases)*
*   **Self-Hosted (Raspberry Pi)**: **$0.00**. Uses your own CPU. (Slow but free).
*   **Lambda Rendering**: ~$0.003 per minute of video.
    *   1 video/day (30s) = 15 mins/month = **$0.05 / month**.

---

## 💰 Grand Total (Monthly Estimate)

| Component | Service | Monthly Cost (3 posts/day) |
| :--- | :--- | :--- |
| **Brain** | OpenAI (GPT-4o-mini) | ~$0.10 |
| **Imagination** | Replicate (FLUX.1) | ~$4.50 |
| **Social** | Twitter API (Metered) | ~$1.00 |
| **Video** | Remotion (Self-Hosted) | $0.00 |
| **Server** | Raspberry Pi (Electricity) | ~$1.00 |
| **TOTAL** | | **~$6.60 / month** |

*Note: This is an estimate. Actual costs may vary based on experimentation and model changes.*
