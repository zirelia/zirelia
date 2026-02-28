# The Brain (AI Engine)

> [!NOTE]
> **Current State (as of 2026-02-28):** The active LLM provider is **OpenAI GPT-4 / GPT-4o-mini**. Both text generation and visual quality control (the Image Critic) run on OpenAI's API.

The "Brain" is responsible for the influencer's personality, thoughts, and content generation strategy. It is powered by **LangChain** and **LangGraph**.

## Architecture

The brain operates as a state machine (LangGraph) with the following nodes:

1.  **Trend Research**: (Optional) Searches the web for trending topics if no topic is provided.
2.  **Draft Content**: Uses the LLM (OpenAI GPT-4) to write a caption based on the `persona.yaml` voice.
3.  **Image Prompt Generation**: Converts the caption into a photorealistic image prompt (adding cinematic lighting, film grain, etc.).
4.  **Critique & Safety**: Reviews the content for policy violations or "cringe" factors before approving.

## Platform-Specific Intelligence

The Brain generates **different content styles** depending on the target platform:

| Platform | Style | Length | Hashtags |
| :--- | :--- | :--- | :--- |
| **Twitter** | Edgy shitpost, punchy | Max 280 chars | 0-1 |
| **Instagram** | Emotional, visual storytelling | Long, descriptive | 15-20 |
| **Facebook** | Community, warm, story-driven | Medium | 2-3 |
| **Threads** | Viral engagement bait | Under 300 chars | **None** |

### Threads Viral Strategy 🧵

Threads is specifically optimized for maximum engagement using 5 viral formats:

1.  **Hot Take**: Bold, slightly controversial opinions
2.  **This or That**: Binary choice questions
3.  **Relatable Vent**: Funny complaints everyone relates to
4.  **IG Tease**: Subtle cross-promo hinting at Instagram content
5.  **Shower Thought**: Random late-night musings

When a Threads post includes an image (the ~30% non-text-only posts), the brain automatically adds a **subtle Instagram cross-promo** without using "link in bio" or direct URLs.

## Persona System

The detailed personality is loaded from `config/persona.yaml` into the system prompt. This ensures the bot always stays in character.

### Memory (RAG)

The bot uses **ChromaDB** to store past posts.
Before generating new content, it queries this database to avoid repeating itself and to reference past events.

## Content Safety

The visual prompt generator includes built-in content moderation:

*   **Never generates** lingerie, underwear, bikini, or revealing intimate clothing.
*   Approved outfits: casual wear, athletic wear, streetwear, dresses, professional attire.
*   This is enforced at the LLM prompt level in `brain.py`.

## Key Files

*   `core/persona/brain.py`: The `PersonaBrain` class that manages LLM interactions.
*   `core/content/generator.py`: The high-level orchestrator.
*   `core/content/workflow.py`: The LangGraph state machine definition.
*   `core/content/templates.py`: Platform-specific prompt templates.
