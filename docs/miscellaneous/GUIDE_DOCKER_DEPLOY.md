# Docker Deployment Guide (Raspberry Pi)

## Prerequisiti
- Raspberry Pi con Docker e Docker Compose installati
- Progetto clonato su Raspberry (`git clone ...`)
- File `.env` configurato con le chiavi (Twitter, Replicate, OpenAI)

---

## Comandi Rapidi

### 1. Build e Avvio (Prima Volta)
```bash
cd ~/Zirelia/virtual_influencer_engine
docker compose up --build -d
```

**Cosa fa:**
- `--build`: Ricostruisce l'immagine Docker (necessario la prima volta o dopo modifiche al codice)
- `-d`: Avvia in background (detached mode)

### 2. Vedere i Log in Tempo Reale
```bash
docker compose logs -f app
```

**Cosa fa:**
- `-f`: Segue i log in tempo reale (come `tail -f`)
- `app`: Nome del servizio definito in `docker compose.yml`

Per uscire: `Ctrl+C`

### 3. Vedere gli Ultimi 100 Log
```bash
docker compose logs --tail=100 app
```

### 4. Fermare il Bot
```bash
docker compose down
```

### 5. Riavviare (Senza Rebuild)
```bash
docker compose restart app
```

### 6. Vedere lo Stato dei Container
```bash
docker compose ps
```

---

## Test Manuale (Singolo Post)

Se vuoi testare un singolo post senza schedulazione:

```bash
docker compose run --rm app python -m virtual_influencer_engine.main --platform twitter --mode text
```

**Cosa fa:**
- `run --rm`: Esegue un comando one-shot e rimuove il container dopo
- `app`: Nome del servizio
- Il resto è il comando da eseguire

---

## Schedulazione Automatica (Cron su Raspberry)

Per far postare Sienna automaticamente ogni giorno:

1. **Apri il crontab:**
   ```bash
   crontab -e
   ```

2. **Aggiungi questa riga** (esempio: posta ogni giorno alle 10:00, 14:00, 18:00, 22:00):
   ```cron
   0 10,14,18,22 * * * cd ~/Zirelia/virtual_influencer_engine && docker compose run --rm app python -m virtual_influencer_engine.main --platform twitter --mode text >> ~/sienna_cron.log 2>&1
   ```

3. **Salva e esci** (`Ctrl+X`, poi `Y`, poi `Enter` su nano).

---

## Troubleshooting

### Il container crasha subito
```bash
docker compose logs app
```
Leggi l'errore completo e cercalo nei log.

### Modifiche al codice non si applicano
```bash
docker compose down
docker compose up --build -d
```

### Vedere i container attivi
```bash
docker ps -a
```

### Entrare nel container (Debug)
```bash
docker compose exec app /bin/bash
```

---

## Note per Raspberry Pi

- **ARM Architecture**: Se il Raspberry è ARM (es. Pi 4), assicurati che il `Dockerfile` usi immagini compatibili (`python:3.11-slim` funziona).
- **Memoria**: Se hai problemi di RAM, aggiungi swap o limita i worker di Celery (se usati).
- **Replicate API**: FLUX.1 gira sui server di Replicate, non sul Raspberry, quindi nessun problema di performance locale.
