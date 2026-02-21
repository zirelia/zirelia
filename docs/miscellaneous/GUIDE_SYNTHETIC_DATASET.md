# Guida: Creare un Dataset Sintetico (Metodo "Zero Foto Reali")

Se non hai foto reali di una modella, devi creare un "clone digitale" consistente da zero usando l'AI. Ecco come fare.

## Fase 1: Trovare il "Seed" Perfetto (La Base)
Devi generare centinaia di volti finché non ne trovi UNO che dici: "Questa è Sienna Fox".

1.  **Scegli un Prompt Base Molto Dettagliato**:
    Usa sempre lo stesso prompt per il viso. Esempio per FLUX.1:
    > "A hyper-realistic close-up portrait of a 25-year-old woman with dirty blonde messy hair and hazel eyes. She has a symmetric face, sun-kissed skin texture, natural freckles, and a small scar on her left eyebrow. Soft natural lighting, 85mm lens, f/1.8, cinematic depth of field."

2.  **Genera con FLUX.1 (su Replicate)**:
    - Vai sulla demo di `black-forest-labs/flux-1.1-pro` o usa il nostro script.
    - Genera 20-30 immagini variando SOLO il **Seed** (un numero casuale) o lasciandolo random.

3.  **Seleziona la "Faccia Madre"**:
    - Scegli l'immagine che ti colpisce di più.
    - **Salva l'immagine** e, se possibile, il **SEED** che l'ha generata.
    - Questa sarà la tua "Ground Truth" (Verità Assoluta).

## Fase 2: Creare le Variazioni (Il Dataset)
Ora devi generare 15-20 foto di QUELLA donna in posizioni diverse.
Il trucco è usare **Img2Img** (Image-to-Image) o prompt molto specifici con lo stesso Seed (se funziona) per mantenere i tratti.

**Metodo Migliore (Replicate/Fal.ai con ControlNet/IP-Adapter):**
Se usi solo FLUX base, la faccia cambierà un po'.
Per un LoRA perfetto, l'ideale è usare uno strumento che accetta un'immagine di riferimento (IP-Adapter).
Ma se vuoi stare sul semplice con FLUX:
1.  Usa il prompt della Fase 1 come base.
2.  Aggiungi dettagli di scienari diversi, mantenendo la descrizione fisica IDENTICA.
3.  Generane tante e scarta quelle che non le somigliano.
4.  Raccogline **20** dove il viso è PERFETTAMENTE riconoscibile come la stessa persona.

**Lista scatti da generare:**
- 10 Primi Piani (Close-up, viso frontale, profilo, 3/4).
- 5 Mezzo Busto (Half-body, vestita normale).
- 5 Corpo Intero (Full-body, stando in piedi, seduta).

## Fase 3: Preparare lo Zip
1.  Rinomina tutte le foto: `sienna_01.jpg`, `sienna_02.jpg`, ecc.
2.  Mettile in una cartella `dataset`.
3.  Zippa la cartella.

## Fase 4: Addestrare il LoRA
1.  Vai su Replicate: `ostris/flux-dev-lora-trainer`.
2.  Carica lo zip.
3.  **Trigger Word**: Usa `TOK` (o `SiennaFox`).
4.  Lancia il training (~$3).

## Fase 5: Integrare
Una volta finito, riceverai un ID modello (es. `antonio/sienna-fox:12345...`).
Lo useremo nel `pipeline.py` al posto del modello base di FLUX.
Da quel momento, basterà scrivere "photo of TOK eating pasta" e uscirà LEI.
