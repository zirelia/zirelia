# FLUX.1 Setup Guide (via Replicate)

## Perché FLUX.1?
FLUX.1 è il modello più avanzato per immagini realistiche, specialmente per:
- **Mani perfette** (problema risolto rispetto a SDXL/DALL-E)
- **Texture della pelle** ultra-realistica
- **Coerenza del personaggio** (se addestrato con LoRA)

## Costi (Replicate)
- **FLUX.1.1 Pro**: ~$0.04 per immagine (1024x1024)
- **FLUX.1 Dev**: ~$0.025 per immagine (più economico, qualità leggermente inferiore)

Per 100 immagini al mese = ~$4 (Pro) o ~$2.50 (Dev).

---

## Setup Rapido

### 1. Crea Account Replicate
1. Vai su [replicate.com](https://replicate.com/)
2. Clicca **Sign Up** (puoi usare GitHub o Google)
3. Conferma l'email

### 2. Ottieni l'API Token
1. Vai su [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens)
2. Clicca **Create token**
3. Copia il token (inizia con `r8_...`)

### 3. Aggiungi al `.env`
Apri `virtual_influencer_engine/.env` e incolla il token:

```env
REPLICATE_API_TOKEN=r8_YOUR_TOKEN_HERE
```

### 4. Scegli il Modello
Il file `.env` è già configurato con **FLUX.1.1 Pro** (il migliore):

```env
REPLICATE_MODEL_VERSION=black-forest-labs/flux-1.1-pro
```

**Alternative** (se vuoi risparmiare):
- `black-forest-labs/flux-dev` (Dev, più economico)
- `black-forest-labs/flux-schnell` (Veloce, gratis ma qualità inferiore)

---

## Test
Dopo aver configurato il token, testa con:

```bash
python -m virtual_influencer_engine.main --platform twitter --mode hybrid --topic "Morning coffee"
```

Questo genererà un'immagine + testo e posterà su X.

---

## Prossimo Step: LoRA Training
Per avere **sempre la stessa faccia di Sienna**, dovrai addestrare un LoRA personalizzato.
Vedi `GUIDE_LORA_TRAINING.md` per i dettagli.
