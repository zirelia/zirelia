# Guida Completa: Creare l'Identità del Virtual Influencer (LoRA)

Questa guida spiega come addestrare un modello AI (**LoRA**) per garantire che il tuo Virtual Influencer abbia sempre lo stesso volto e corpo in ogni foto.

## 1. Cos'è un LoRA e perché serve?
*   **Problema**: I modelli base (DALL-E 3, Midjourney) generano persone sempre diverse. Anche se scrivi "donna bionda 30 anni", ogni volta sarà una donna diversa.
*   **Soluzione (LoRA)**: È un piccolo "adattatore" (Low-Rank Adaptation) che insegna al modello base (SDXL) *chi è* esattamente il tuo personaggio.
*   **Risultato**: Quando scrivi "foto di [NOME_TRIGGER] in spiaggia", l'AI userà i tratti specifici che ha imparato.

---

## 2. Di cosa hai bisogno (Dataset)
La qualità del risultato dipende al 100% dalle foto che usi per l'addestramento.

**Requisiti:**
*   **Quantità**: 15-25 foto di alta qualità.
*   **Soggetto**: Deve essere sempre la stessa persona (ovviamente).
*   **Varietà**:
    *   10 primi piani (volto).
    *   5 mezzo busto.
    *   5 corpo intero.
    *   Diverse angolazioni (profilo, frontale, 3/4).
    *   Diversa illuminazione (giorno, studio, notte).
    *   Sfondi neutri o semplici.
*   **Cosa evitare**: Mani in vista (spesso vengono male), altre persone nella foto, accessori che coprono il viso (occhiali da sole grossi).

**Dove prendo le foto?**
1.  **Metodo "Reale"**: Paghi una modella/attrice per un servizio fotografico e usi quelle foto (con i diritti). È il metodo più sicuro legalmente.
2.  **Metodo "Sintetico"**: Generi un volto che ti piace con Midjourney/DALL-E, ne fai tante variazioni mantenendo i tratti simili (difficile), poi usi quelle.
3.  **Metodo "Volto Esistente"**: Usare foto di una persona famosa o esistente senza permesso è illegale e viola i termini di servizio. **Sconsigliato.**

---

## 3. Come Addestrare il Modello (Senza PC Potente)
Non ti serve un PC da gaming. Useremo il cloud (**Replicate** o **Dreambooth**).

### Passo A: Account Replicate
1.  Vai su [replicate.com](https://replicate.com).
2.  Crea un account e aggiungi un metodo di pagamento.

### Passo B: Addestramento (FLUX.1 - Consigliato per Mani/Dettagli)
Per ottenere il massimo realismo (e mani decenti), usa **FLUX.1**.

1.  Cerca su Replicate il trainer: **`ostris/flux-dev-lora-trainer`**.
2.  **Upload Images**: Carica lo zip con le tue 15-20 foto.
3.  **Trigger Word**: Scegli `TOK` (o lascia vuoto se il trainer lo gestisce, ma meglio metterne uno).
4.  **Steps**: Imposta 1000-1500 steps (costa un po' di più ma viene meglio).
5.  **Lancia**: Costo ~$2-4.

Una volta finito, copia l'ID del modello (es. `tuo-nome/tuo-modello-flux:version...`).
FLUX è molto più avanzato di SDXL per pelle e dita.

### Passo C: Ottenere l'ID
Una volta finito, Replicate ti darà un ID del modello (es. `tuo-nome/nome-modella:versione-hash`).
Copia questo ID. Questo è quello che va inserito in `settings.py` -> `REPLICATE_MODEL_VERSION`.

---

## 4. Hardware e Costi
**Domanda: "Mi serve un PC potente per far girare il bot?"**

**Risposta Breve: NO, se usi il Cloud (come configurato ora).**

### Opzione A: Cloud (Consigliata)
Il bot (il codice Python) è leggerissimo. Può girare su un Raspberry Pi, un VPS da 5€/mese o il tuo PC portatile.
*   **Calcolo Pesante**: Lo fa Replicate sui suoi server.
*   **Costo**: Paghi per ogni immagine generata.
    *   Circa $0.04 - $0.08 per immagine SDXL/Flux.
    *   Se generi 10 foto al giorno = ~$15/mese.
*   **Vantaggi**: Nessuna manutenzione hardware, scalabile all'infinito.

### Opzione B: Locale (Solo per Esperti)
Se vuoi generare immagini gratis sul tuo PC:
*   **Hardware Richiesto**: PC con GPU NVIDIA (RTX 3090 / 4090) con almeno 24GB di VRAM. Costo PC: >2000€.
*   **Costo Elettricità**: Alto.
*   **Svantaggi**: Devi gestire driver, installazioni complesse (ComfyUI/Automatic1111) e tenere il PC acceso 24/7.
*   **Integrazione**: Il codice attuale supporta Replicate/OpenAI. Per locale dovresti riscrivere la `pipeline.py` per chiamare le API locali di Automatic1111.

---

## Riassunto Operativo
1.  **Raccogli 20 foto** del soggetto.
2.  Vai su **Replicate**, cerca un trainer SDXL o FLUX LoRA.
3.  Carica foto, paga i **2-3$** di training.
4.  Prendi l'**ID del modello** generato.
5.  Mettilo nel file `.env` o `settings.py` del bot.
6.  Il bot ora userà quel modello via Cloud. Il tuo PC non deve fare nulla di pesante.
