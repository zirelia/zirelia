# Guida Completa: Configurazione Twitter (X) per Zirelia

Questa guida ti accompagna passo dopo passo nella creazione di un account Twitter, nell'ottenimento delle chiavi API e nella configurazione del bot per postare **solo testo**.

## Parte 1: Creare l'Account X (Twitter)
Se hai già un account dedicato al tuo Virtual Influencer, salta al passaggio 2.

1.  Vai su [twitter.com/signup](https://twitter.com/signup).
2.  Registrati con una email dedicata (es. `Zirelia.ai@gmail.com`).
3.  Completa il profilo (Foto, Bio, Header) per evitare che venga flaggato come spam.
4.  **Importante**: Verifica il numero di telefono. Senza telefono verificato, non puoi creare le App Developer.

> **NOTA: Hai già usato il tuo numero?**
> Twitter non permette di usare lo stesso numero su più account developer.
> *   **Soluzione A (Test Veloce)**: Usa il tuo account personale esistente per creare l'App. Il bot posterà a nome tuo (utile per testare il codice).
    *   **Importante**: X ti vedrà inizialmente in Italia (dal tuo IP). È normale.
    *   **Link Diretto Cambio Lingua**: [x.com/settings/languages](https://x.com/settings/languages)
    *   In alternativa, il percorso in Italiano è: **Altro -> Impostazioni e supporto -> Impostazioni e privacy -> Accessibilità, aspetto e lingue -> Lingue**. Imposta **English**.
    *   **Cambio Paese Contenuti**: Vai su [x.com/settings/explore](https://x.com/settings/explore), togli la spunta a "Mostra contenuti in questa posizione" e metti **United States**.
    *   Nel profilo pubblico, metti come Location: **Los Angeles, CA**.
    *   **NO Automated Label**: X ti chiederà se vuoi l'etichetta "Automated Account". **Rifiuta/Salta**. Sienna è un personaggio, non un bot del meteo. L'etichetta rovina il realismo.

> **🆘 SOS Verifica Telefono Non Funziona?**
> Se l'SMS non arriva sulla nuova SIM (Iliad/Ho/ecc):
> 1.  **Dall'App**: Prova a fare la verifica dall'App ufficiale di Twitter sul telefono (invece che da PC). Spesso funziona meglio.
> 2.  **Prefisso**: Assicurati di aver messo `+39` davanti.
> 3.  **Carrier Block**: Alcuni operatori virtuali bloccano gli SMS "premium" dall'estero. Chiama l'operatore per sbloccarli o prova a inviare un SMS TU al numero che ti dicono (verifica inversa), se te lo propongono.
> 4.  **Troppi Tentativi**: Se hai cliccato "Invia" 5 volte, ti bloccano per 24h. Aspetta domani.

> **🐛 "Something went wrong" (Qualcosa è andato storto)?**
> Se il tuo profilo nuovo ti dà questo errore o non carica i tweet:
> 1.  **È Normale**: Twitter sta facendo i controlli anti-bot iniziali.
> 2.  **Test Manuale**: Prova a scrivere un tweet a mano ("Hello world"). Se te lo fa inviare, l'account è attivo e il problema è solo grafico.
> 3.  **Completa il Profilo**: Metti una foto profilo e una bio ORA. Gli account senza foto vengono spesso limitati temporaneamente.

---

## Parte 2: Ottenere le API (Developer Portal)
Per far postare il bot, devi registrare una "App" su X.

1.  Vai su [developer.twitter.com](https://developer.twitter.com/en/portal/dashboard).
2.  Accedi con l'account creato sopra.
3.  Iscriviti al **Free Plan** (o Basic se vuoi più limiti).
    *   Il *Free Plan* permette di postare 1.500 tweet al mese (gratis).
    *   Descrivi l'uso: *"Automation for a virtual influencer art project posting daily updates."*

### Creare la App
1.  Nel Dashboard, clicca **"Create App"**.
2.  Dai un nome alla App (es. `ZireliaBot`).
3.  Copia subito **API Key** e **API Key Secret**. (Salvale in un blocco note, non le vedrai più).

### PASSAGGIO CHIAVE: "User Authentication Settings" (Fondamentale)
Se non fai questo, le chiavi che generi saranno "Read Only" e il bot fallirà.

1.  Nel menu di sinistra, vai sul tuo **Project** e clicca sulla **App** appena creata (icona ingranaggio ⚙️).
2.  Scorri fino a trovare la sezione **"User authentication settings"**.
3.  Clicca su **Set up**.

### Configurazione Permessi (Copia Esattamente Questo)
1.  **App permissions**: Seleziona **Read and Write** (o "Read and Write and Direct Message").
2.  **Type of App**: Seleziona **Web App, Automated App or Bot**.
3.  **App info** (X richiede questi URL anche se non servono, metti questi valori dummy):
    *   **Callback URI / Redirect URL**: Scrivi esattamente `http://localhost:8000/callback`
    *   **Website URL**: Scrivi esattamente `https://example.com`
4.  Clicca **Save** in fondo.
5.  Ti mostrerà "Client ID e Client Secret" -> **Ignorali**, non ci servono per questo bot (noi usiamo OAuth 1.0a).

---

### Generare le Chiavi Finali (Access Token)
ORA che hai salvato i permessi di scrittura, devi rigenerare i token (se li avevi presi prima, erano sbagliati/read-only).

1.  Torna nella scheda **Keys and Tokens** (in alto nella pagina della App).
2.  Cerca la sezione **Authentication Tokens** -> **Access Token and Secret**.
3.  Clicca **Generate** (o Regenerate).
4.  Copia:
    *   **Access Token** (Incolla in `.env` -> `TWITTER_ACCESS_TOKEN`)
    *   **Access Token Secret** (Incolla in `.env` -> `TWITTER_ACCESS_TOKEN_SECRET`)

Se avevi già generato l'API Key e Secret all'inizio, quelle restano uguali. Se le hai perse, rigenerale sotto "Consumer Keys".

---

## Parte 3: Configurare il Bot
Ora hai le 4 chiavi sacre. Inseriscile nel bot.

1.  Apri il file `.env` nel tuo progetto `Zirelia`.
2.  Cerca la sezione Twitter e incollale:

```env
# Twitter (X) Configuration
TWITTER_API_KEY=incolla_qui_api_key
TWITTER_API_SECRET=incolla_qui_api_secret

TWITTER_ACCESS_TOKEN=incolla_qui_access_token
TWITTER_ACCESS_TOKEN_SECRET=incolla_qui_access_token_secret

# Il Bearer Token spesso non serve per postare (usa OAuth1), ma se ce l'hai, mettilo.
TWITTER_BEARER_TOKEN=opzionale
```

---

## Parte 4: Testare (Solo Testo)
Vogliamo verificare che funzioni senza rischiare ban e senza generare immagini.

1.  Apri il terminale nella cartella del progetto.
2.  Attiva l'ambiente virtuale (se ne usi uno).
3.  Lancia il comando di test specifico:

```bash
python -m virtual_influencer_engine.main --platform twitter --mode text --topic "Hello World! This is my first AI generated tweet."
```

### Cosa succederà?
1.  Il bot si avvia.
2.  Il "Cervello" (LangChain) genera un tweet basato sul topic "Hello World...".
3.  Il tweet viene inviato a X usando le chiavi nel `.env`.
4.  Vedrai nel terminale: `Result: {'id': '12345...', 'text': '...'}`.
5.  Vai sul tuo profilo X e controlla se il tweet è apparso!
