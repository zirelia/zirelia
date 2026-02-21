# Persona Engine Reference

Path: `virtual_influencer_engine/core/persona/brain.py`

## Class: `PersonaEngine`

The core LLM interface that manages personality context and memory.

### Configuration (`persona.yaml`)
Loads `name`, `traits`, `voice`, and `routine` from the YAML file.

### Methods

#### `__init__(self, config_path="config/persona.yaml")`
*   Initializes OpenAI (`ChatOpenAI`).
*   Loads vector memory (`ChromaVectorStore`).
*   Configures system prompts based on the YAML identity.

#### `generate_thought(self, context: str) -> str`
Generates an internal monologue or decision based on context.

## Class: `ContentGenerator`

Path: `virtual_influencer_engine/core/content/generator.py`

Orchestrates the creation of public-facing content using a LangGraph workflow.

### Methods

#### `get_autonomous_topic(self, forced_hour=None)`
Selects a topic based on the time of day.
*   **Logic**: Maps hour (e.g., 8:00) to routine (e.g., "Morning Coffee").
*   **Enhancement**: Checks for holidays via `SmartScheduler`.

#### `generate_caption(self, platform, image_description, context)`
Generates text optimized for a specific platform.
*   **Inputs**: Platform ("twitter", "instagram"), Visual Context ("photo of girl eating...").
*   **Process**:
    1.  Drafts content using `PersonaEngine`.
    2.  Applies platform constraints (length, hashtags, emojis).
    3.  Critiques internally for tone/safety.
*   **Returns**: Final caption string.
