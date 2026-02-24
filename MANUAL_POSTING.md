# Manuale Posting — Fase Warm-Up

Comandi per generare contenuto manualmente senza postare automaticamente.
Usare durante le prime settimane con account nuovo.

---

## Genera testo + immagine (senza postare)

```bash
docker compose run --rm app python main.py \
  --platform twitter \
  --mode hybrid \
  --dry-run
```

Il log mostra:
- **Generated Caption** → testo del tweet, copialo su Twitter/X
- **Generating image with prompt** → prompt usato per FLUX
- L'immagine viene salvata localmente nella cartella del container (montata su `./`)

---

## Genera solo testo (nessuna immagine, nessun costo Replicate)

```bash
docker compose run --rm app python main.py \
  --platform twitter \
  --mode text \
  --dry-run
```

---

## Forza un topic specifico

```bash
docker compose run --rm app python main.py \
  --platform twitter \
  --mode hybrid \
  --topic "morning coffee ritual" \
  --dry-run
```

---

## Posta davvero (quando sei pronto)

Rimuovi `--dry-run`:

```bash
docker compose run --rm app python main.py \
  --platform twitter \
  --mode hybrid
```

---

## Note pratiche

- I **WARN** sulle variabili mancanti (Anthropic, Meta, HuggingFace) sono normali — ignorali
- L'errore `GPU device discovery failed` è normale su Raspberry Pi — ignoralo
- Il testo del tweet è nella riga `Generated Caption:` del log
- L'URL dell'immagine è nella riga `Critic analyzing image:` — puoi scaricarla da lì
- Warm-up consigliato: **1 post al giorno** per le prime 2 settimane, poi 2-3/giorno
