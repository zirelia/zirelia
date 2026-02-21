# Guida Completa: Creare e Addestrare un Avatar FLUX.1 (Da Zero)

Questa guida ti accompagna passo passo nella creazione di **Sienna Fox** usando solo l'AI (metodo sintetico) e addestrando un modello **FLUX.1 LoRA** per rendere il suo volto e corpo consistenti in ogni futura generazione.

---

## FASE 1: Il "Casting" (Fatto ✅)
Obiettivo: Trovare il volto "Base".
Stato: Hai generato 4 candidati e confermato che il volto ti piace ed è consistente.
**Azione**: Salva la tua preferita (o tutte e 4 se uguali) in una cartella sicura. Questa è la "Ground Truth".

---

## FASE 2: Creazione del Dataset Completo (Il "Book Fotografico")
Per insegnare all'AI chi è Sienna, dobbiamo darle foto di lei in diverse pose, non solo primi piani.
**Target Dataset**: 20-30 Immagini totali.

### Cosa Generare (Lista Scatti)
Usa Replicate (FLUX.1 Pro o Dev) con lo stesso prompt di base del viso, ma cambiando l'inizio del prompt per descrivere l'inquadratura.

1.  **Primi Piani (Close-ups) - 10 foto**
    *   Già ne hai 4 (dal casting). Generane altre 6 con luci diverse (alba, tramonto, interno).
    *   *Prompt Key*: `close-up portrait`, `looking at camera`, `smiling`, `serious`.

2.  **Mezzo Busto (Upper Body) - 10 foto**
    *   Sienna vestita casual (t-shirt, camicia) dalla vita in su.
    *   *Prompt Key*: `waist-up shot`, `wearing a white t-shirt`, `casual outfit`, `arms crossed`, `fixing hair`.
    *   *Nota*: Assicurati che il viso sia identico a quello dei primi piani. Se cambia troppo, scarta la foto.

3.  **Corpo Intero (Full Body) - 10 foto**
    *   Sienna in piedi o seduta (visibili gambe e scarpe).
    *   *Prompt Key*: `full body shot`, `standing on a street`, `sitting on a chair`, `wearing jeans and sneakers`, `yoga outfit`.
    *   *Importante*: FLUX è bravo con i corpi, ma controlla che le proporzioni (slim-thick) siano rispettate.

**Consiglio Tecnico**:
Per mantenere il volto uguale, copia-incolla la descrizione fisica del viso ESATTA in ogni prompt:
> "...dirty blonde messy wavy hair, expressive hazel eyes, symmetric face, sun-kissed skin..."

---

## FASE 3: Preparazione dei File
1.  **Rinomina**: Chiama le immagini `sienna_01.jpg`, `sienna_02.jpg`, ..., `sienna_30.jpg`.
2.  **Formato**: Devono essere JPG o PNG. Non servono risoluzioni enormi (1024x1024 o poco più va bene).
3.  **Zip**: Metti tutto in una cartella e crea un file `.zip` (es. `sienna_dataset.zip`).

---

## FASE 4: Addestramento LoRA su Replicate
Ora che hai il dataset, insegniamo a FLUX chi è Sienna.

1.  **Vai su Replicate**: Cerca il modello **`ostris/flux-dev-lora-trainer`**.
    *   Link diretto: https://replicate.com/ostris/flux-dev-lora-trainer

2.  **Configura il Training**:
    *   **input_images**: Carica il tuo file `sienna_dataset.zip`.
    *   **Destination**: Clicca su "Create new model".
        *   **Name**: Scrivi `sienna-flux-lora`.
        *   **Visibility**: Private.
    *   **input_images**: Carica il tuo file `sienna_dataset.zip`.
    *   **trigger_word**: Scrivi **`TOK`** (Tutto maiuscolo).
    *   **autocaption**: Lascia spuntato (True).
    *   **autocaption_prefix**: Scrivi `photo of TOK, `. (Importante! Aiuta l'AI a capire che TOK è il soggetto).
    *   **autocaption_suffix**: Lascia vuoto. (Non serve).
    *   **steps**: Scrivi **`2000`**.
    *   **lora_rank**: Lascia `16`.
    *   **Le altre opzioni (HuggingFace, WandB, etc.)**: IGNORALE. Lascia tutto vuoto.
    
    *   (Il trigger `TOK` è fondamentale perché il bot è programmato per usare questa parola chiave).

3.  **Aggiungi Pagamento**: Qui ti chiederà la carta se non l'hai messa. Il training costerà circa **$2.00 - $4.00**.

4.  **Avvia (Run)**: Clicca "Create training".
    *   Ci vorranno circa 20-30 minuti.

---

## FASE 5: Usare il Tuo Nuovo Modello
Quando finisce, Replicate ti darà un percorso del modello, tipo:
`tuo-username/sienna-flux-lora:versione_hash...`

1.  Copia questo percorso.
2.  Vai nel file `.env` del nostro progetto.
3.  Aggiorna la variabile:
    ```bash
    REPLICATE_MODEL_VERSION=tuo-username/sienna-flux-lora:versione_hash...
    ```

**Fatto!**
D'ora in poi, il bot userà automaticamente il TUO modello personalizzato.
Quando genererà un'immagine, nel prompt metterà automaticamente la parola `TOK` (o quella che configureremo) e uscirà Sienna.

---

## Riferimento Tecnico: Come Funziona Davvero?

### 1. Il Trucco per il Corpo (Costanza del Viso)
Come facciamo ad avere Sienna che corre, sta seduta o balla mantenendo la STESSA faccia, senza usare Photoshop?

**La Tecnica del "Prompt Identico":**
I modelli come FLUX associano le parole a concetti visivi forti. Se usiamo *sempre* lo stesso blocco di testo per descrivere il viso, il modello tenderà a replicarlo anche se l'inquadratura è lontana.

*   **Prompt Sbagliato**: *"Una donna bionda che corre sulla spiaggia."* (Esce una bionda generica).
*   **Prompt Giusto**: *"**Full body shot** of a woman running on the beach. She has **dirty blonde messy wavy hair, expressive hazel eyes, symmetric face, sun-kissed skin texture, natural freckles, and a small scar on her left eyebrow**."*

**Cosa succede:** FLUX legge "Full body shot" e inquadra da lontano, ma legge anche "small scar on eyebrow" e cerca di mantenere quei dettagli del viso anche se piccoli. Questo crea la consistenza necessaria per il dataset.

### 2. L'Integrazione (Il "Trapianto di Cervello")
Una volta addestrato il LoRA, cosa cambia tecnicamente nel bot?

Attualmente il bot dice:
> *Generami una foto con modello **Base FLUX**.*

Dopo l'aggiornamento del file `.env` con il tuo ID modello personalizzato, dirà:
> *Generami una foto con modello **Sienna-LoRA** usando la parola magica **TOK**.*

Il LoRA è come un "filtro" o una lente a contatto permanente che forza qualsiasi immagine generata ad avere le sembianze di Sienna. Non serve cambiare il codice, basta cambiare l'ID del modello nelle impostazioni.

---

## Domande Cruciali: Realismo & Coerenza
Le tue domande sono sacrosante. Ecco la verità su FLUX e LoRA.

### 1. Sienna avrà espressioni facciali coerenti con il contesto?
**Sì, ma rischia di essere "monotona"**.
I LoRA tendono a "congelare" l'espressione che vedono più spesso nel dataset. Se nelle tue 20 foto Sienna sorride sempre, farà fatica a sembrare triste o arrabbiata.
*   **Soluzione**: Nel dataset (Fase 2), metti almeno 3 foto "serie", 3 "sorridenti", 3 "neutre". Così impara che la faccia è flessibile.
*   Il prompt del bot ("Sienna laughing at a joke") farà il resto.

### 2. Sienna avrà sfondi coerenti con il testo?
**Sì, assolutamente.**
Questo è il punto di forza di FLUX. Se il bot scrive "Sono a Parigi", il prompt generato sarà "TOK standing in front of Eiffel Tower". Lo sfondo sarà perfetto.
L'unico rischio è che a volte il LoRA (se sovra-addestrato) si porti dietro "pezzi" dello sfondo originale delle foto di training.
*   **Soluzione**: Nel dataset, usa sfondi **molto vari** (muro bianco, parco, strada, cucina). Se usi sempre lo stesso sfondo grigio, l'AI penserà che lo sfondo grigio faccia parte della sua faccia.

### 3. Sarà scambiabile per una persona reale? (Test di Turing Visivo)
**Sì, al 95%.**
FLUX.1 è lo stato dell'arte. La pelle, i pori, i capelli sono indistinguibili dal reale.
Dove cade l'illusione (l'"Uncanny Valley")?
*   **Occhi**: A volte lo sguardo è "vuoto" o fissa troppo la camera.
*   **Denti**: Se sorride troppo, a volte i denti sono troppi o strani.
*   **Mani**: FLUX è molto meglio di prima, ma ogni tanto sbaglia le dita.
*   **Perfezione**: È *troppo* perfetta. Una foto reale ha difetti, ombre brutte, capelli fuori posto.
*   **Soluzione**: Chiedere nel prompt "raw photo, amateur photo, slightly grainy, motion blur" per renderla meno perfetta e più umana.
