# The Brain (AI Engine)

> [!NOTE]
> **Current State (as of 2026-02-20):** The only active LLM provider is **OpenAI GPT-4 / GPT-4o-mini**. Both text generation and visual quality control (the Image Critic) run on OpenAI's API. Alternative LLMs (Anthropic, local Ollama) are planned for future phases.

The "Brain" is responsible for the influencer's personality, thoughts, and content generation strategy. It is powered by **LangChain** and **LangGraph**.

## Architecture

The brain operates as a state machine (LangGraph) with the following nodes:

1.  **Trend Research**: (Optional) Searches the web for trending topics if no topic is provided.
2.  **Draft Content**: Uses the LLM (OpenAI GPT-4/3.5) to write a caption based on the `persona.yaml` voice.
3.  **Image Prompt Generation**: Converts the caption into a photorealistic image prompt (adding cinematic lighting, film grain, etc.).
4.  **Critique & Safety**: Reviews the content for policy violations or "cringe" factors before approving.

## Persona System

The detailed personality is loaded from `config/persona.yaml` into the system prompt. This ensures the bot always stays in character.

### Memory (RAG)

The bot uses **ChromaDB** to store past posts.
Before generating new content, it queries this database to avoid repeating itself and to reference past events (e.g., "Like I said yesterday...").

## Key Files

*   `core/persona/brain.py`: The `PersonaEngine` class that manages LLM interactions.
*   `core/content/generator.py`: The high-level orchestrator.
*   `core/content/workflow.py`: The LangGraph state machine definition.
