# Come "Ragiona" Zirelia: Logica di Posting

Questo documento spiega cosa succede "sotto il cofano" quando il bot decide di postare. Non è magia, è una catena di decisioni logiche basate sulla **Persona** che abbiamo configurato.

---

## 1. Il Cervello (Brain)
Tutto parte da `core/persona/brain.py`.
Il "Cervello" non inventa cose a caso. Segue rigorosamente le istruzioni in `config/persona.yaml`.

### Il Processo di Pensiero:
1.  **Input**: Tu dai un "Topic" (es. "Monday Motivation" o "Late Night Thoughts").
2.  **Context Retrieval (Memoria)**:
    *   Il bot controlla nel database (ChromaDB) se ha già parlato di questo argomento recentemente.
    *   *Obiettivo*: Evitare di ripetersi ("Ho già detto che amo il caffè ieri, oggi dico altro").
3.  **Personality Injection**:
    *   Costruisce un "System Prompt" combinando:
        *   **Chi è**: Sienna Fox, 23 anni, Los Angeles.
        *   **Vibe**: Flirty, Confident.
        *   **Stile**: Usa emoji, frasi brevi.
4.  **Generazione (LLM)**:
    *   Chiede a GPT-4: *"Sei Sienna. In base a questo contesto e alla tua memoria, scrivi un tweet."*

---

## 2. Il Flusso di Lavoro (Workflow)
Non basta "generare e postare". Usiamo un sistema di controllo qualità (**LangGraph** in `core/content/workflow.py`).

### Step A: Il "Drafter" (Lo Scrittore)
L'AI scrive una prima bozza.
> *Esempio Bozza*: "Hello everyone, I like coffee. It is good."

### Step B: Il "Critic" (Il Revisore)
Un secondo agente controlla la bozza:
1.  **È "In Character"?**: Suona come Sienna o come un robot noioso?
2.  **È Sicuro?**: Contiene parole vietate o offensive?
3.  **Critica**: "Troppo noioso. Sienna userebbe delle emoji e sarebbe più provocante."

### Step C: Il "Refiner" (Il Correttore)
Se il Critico boccia il post, il Drafter lo riscrive applicando i suggerimenti.
> *Esempio Finale*: "Coffee first, questions later. ☕️😉 Who's creating chaos with me today? 🔥"

---

## 3. Cosa Aspettarsi (Output Reale)

### 📝 Testo (Twitter/X e Caption)
Aspettati post che seguono le regole di `persona.yaml`:
*   **Lunghezza**: Breve per Twitter, più discorsiva per Instagram/Facebook.
*   **Emoji**: Ne userà molte (`✨`, `🔥`, `🦊`).
*   **Domande**: Cercherà spesso di chiudere con una domanda per stimolare i commenti ("E tu che fai stasera?").

### 📸 Immagini (Instagram/Twitter Hybrid)
Se attivi la modalità ibrida (Testo + Foto):
1.  Il "Cervello" descrive la scena ideale per il testo generato.
    *   *Testo*: "Serata tranquilla..."
    *   *Prompt Visivo*: "Sienna Fox sitting on a velvet couch, evening light, holding a glass of wine, wearing silk pajamas, cozy atmosphere."
2.  **FLUX (Replicate)** riceve questo prompt.
3.  Genera l'immagine usando il modello addestrato (volto coerente).
4.  Il bot unisce Testo + Foto e pubblica.

---

## Riassunto
Il bot non è "casuale". È un attore che recita una parte (`Sienna`) seguendo un copione (`persona.yaml`) e improvvisando le battute (`GPT-4`) sotto la supervisione di un regista (`Workflow`).

Se il bot posta cose che non ti piacciono (es. troppo formale, troppe emoji), **non devi toccare il codice**. Devi solo modificare le regole in `config/persona.yaml`.
