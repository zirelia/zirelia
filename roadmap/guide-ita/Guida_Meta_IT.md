# Configurazione Meta Developer (Instagram & Threads)

Questa guida spiega passo-passo come configurare gli account Sviluppatore, creare le App e ottenere i Token necessari per permettere a Zirelia di pubblicare automaticamente su **Instagram** e **Threads**.

> 💡 **Nota sui Costi**: Le API di Instagram e Threads, così come gli Account Sviluppatore e i Profili Business, sono **completamente gratuiti**. A differenza di Twitter, Meta non fa pagare per l'accesso base o automatizzato alle sue piattaforme.

---

### Prerequisiti prima di iniziare:
1. Un normale **account Facebook** (serve per accedere al portale sviluppatori).
2. Un **Account Instagram Professionale** (Creator o Business). Entrambi sono gratuiti.
3. Un **account Threads** collegato allo stesso profilo Instagram.
4. Una **Pagina Facebook** collegata all'account Instagram (le API Meta lo richiedono obbligatoriamente per autorizzare Instagram).

---

## Parte 0: Strategia di Creazione Account (Anti-Ban)

Gli algoritmi di sicurezza di Meta sono spietati contro i nuovi account che cercano subito di usare le API. **NON creare un profilo Facebook "falso" per la tua IA.** Verresti bannato nel giro di 24 ore richiedendo un documento d'identità.

Segui questa sequenza esatta per stabilire "fiducia" (Trust) con Meta:

1. **L'E-mail**: Usa la **stessa e-mail** (es. Gmail) della tua AI che hai usato per Twitter/X. La coerenza tra le piattaforme aumenta il Trust.
2. **Instagram & Threads**:
   * Crea l'account Instagram **da uno smartphone** (tramite l'app mobile, non da un browser su PC).
   * Installa l'app Threads e fai login usando le credenziali Instagram appena create.
   * Dalle impostazioni dell'app Instagram, passa a un **Account Professionale** (Creator o Business).
3. **Il Collegamento a Facebook (FONDAMENTALE)**:
   * Fai login con il tuo conto Facebook **PERSONALE e REALE** (quello che usi tutti i giorni).
   * Crea una nuova **Pagina Facebook** per la tua AI (es. "Sienna Fox"). Non ti serve pubblicarci sopra; funge solo da "ponte" tecnico e legale.
   * Nelle Impostazioni di questa nuova Pagina Facebook, vai su "Account Collegati" e **collega l'Instagram della tua AI**.
   * Poiché il tuo account personale ha un "Trust Score" molto alto, Meta permette alla Pagina (e all'Instagram collegato) di usare le API in totale sicurezza senza far scattare i sistemi anti-bot.

---

## Parte 1: Creazione della Meta App (Metodo "Azienda")

> ⚠️ **IMPORTANTE: Ignora la Verifica dell'Azienda (Business Verification)**
> Sulla dashboard potresti vedere un avviso che ti chiede di "Verificare l'Azienda" in quanto "Non verificata". **IGNORALO COMPLETAMENTE.** Non devi caricare documenti. Dal momento che l'app serve solo per te, può rimanere in stato "Sviluppo" o "Non verificata" per sempre.

Meta cambia spesso interfaccia, nascondendo le opzioni per gli sviluppatori indipendenti. Per avere accesso a Instagram senza blocchi, segui **esattamente** questi step per forzare la creazione di un'app "Aziendale":

1. Vai sul [Meta for Developers Portal](https://developers.facebook.com/) e accedi con il tuo account Facebook personale.
2. Clicca su **My Apps** (Le mie App) in alto a destra, poi sul pulsante verde **Create App** (Crea App).
3. Nella schermata *"Che cosa vuoi far fare alla tua app?"*, **IGNORA tutte le opzioni principali**. Scorri fino in fondo alla pagina, seleziona **Altro** (Other) e clicca su Avanti.
4. Alla schermata *"Seleziona un tipo di app"*, scegli **Azienda** (Business) e clicca su Avanti.
5. Dai un nome all'app (es. "Zirelia AutoPoster"). Sotto "Account Business", lascia **Nessun account selezionato**. Clicca su **Crea App**.

---

## Parte 2: Aggiungere i Prodotti (Instagram e Login)

Una volta creata l'App di tipo Azienda, atterrerai su una Dashboard con dei grandi riquadri chiamati "Prodotti". Devi aggiungerne due per far funzionare tutto senza errori:

1. Scorri la pagina "Aggiungi prodotti alla tua app".
2. Trova il riquadro **Instagram** (o *Instagram Graph API*) e clicca su **Configura** (Set Up). Il menu laterale si aggiornerà, ignoralo e torna alla Dashboard (o clicca *Aggiungi Prodotto*).
3. Trova il riquadro **Facebook Login for Business** e clicca su **Configura**. *(Questo passaggio è FONDAMENTALE per far aprire la finestra di login successivamente, senza ricevere l'errore "Funzione non disponibile").*

### 2.1 Inserire il link Privacy Obbligatorio
Meta blocca la finestra di login se manca una URL Privacy fittizia:
1. Dal menu a sinistra della tua App, vai su **Impostazioni (Settings) > Di base (Basic)**.
2. Trova il campo **URL della Normativa sulla privacy** (Privacy Policy URL). Inserisci un link qualsiasi (es. `https://google.com` o il tuo GitHub). Scorri in fondo e clicca **Salva modifiche**.

---

## Parte 3: Generare il Token (Il Graph API Explorer)

Dimentica l'interfaccia caotica dell'app e vai dritto allo strumento ufficiale per sviluppatori. Questo è l'unico modo sicuro per non impazzire:

1. Apri questo link diretto: 👉 **[Graph API Explorer](https://developers.facebook.com/tools/explorer/)**
2. Nel menu a destra "App Meta", seleziona la tua app (se non è già lì).
3. Sotto **"Utente o Pagina"** (User or Page), clicca il menu a tendina e scegli **Ottieni token di accesso dell'utente** (Get User Access Token).
4. Si aprirà un popup di Facebook: fai il login personale e **seleziona tutte le tue Pagine e Instagram**. Dai l'ok. Se prima non ti faceva andare avanti con "Errore", ora col link Privacy e il Facebook Login funzionerà.
5. Sotto la voce **Autorizzazioni** (sempre a destra), usa la barra di ricerca o i menu a tendina per **aggiungere queste 5 voci**:
    * `instagram_basic`
    * `instagram_content_publish`
    * `pages_show_list`
    * `pages_read_engagement`
    * `pages_manage_posts` (Rigorosamente necessario per pubblicare sulla Pagina FB)
    > ⚠️ **NON aggiungere permessi Threads qui!** Threads richiede un'app Meta **completamente separata** con il proprio flusso OAuth. Vedi la **Parte 4** di questa guida.
6. Clicca il mega pulsante verde **Genera Token di accesso** e ri-conferma il popup di Facebook.
7. ORA CI SIAMO: Torna sul menu a tendina **Utente o Pagina** e aprilo. Clicca sul **Nome della tua Pagina** (es. "Sienna Fox").
8. La stringa lunghissima al centro dello schermo cambia: **quello è il tuo Token Pagina**! Copiatelo da qualche parte.

### Rendere il Token TEMPORANEO -> PERMANENTE (Che non scade mai)

Il token di default scade dopo 1 ora. Estenderlo normalmente lo fa durare 60 giorni. Ma per un bot autonomo devi generare un **Page Access Token Permanente**:

1. Rimanendo nel Graph API Explorer (con il tuo Token *Utente* scovato in precedenza già selezionato), clicca sul piccolo punto esclamativo blu (ℹ️) accanto alla stringa del token.
2. Clicca su **Open in Access Token Tool** (Apri nello strumento per i Token).
3. In fondo a quella pagina, clicca su **Extend Access Token** (Estendi Token).
4. Questo ti genera e ti fa copiare un token "User" valido 60 giorni. **Copia questo token di 60 giorni.**
5. Ora ritorna alla pagina principale del Graph API Explorer.
6. **Incolla il token di 60 giorni** all'interno della barra "Token di accesso" (cancellando quello vecchio).
7. Nella barra dell'URL API (dove c'è scritto `GET v26.0 /`), cancella tutto e scrivi: `me/accounts`
8. Clicca **Invia** (Submit).
9. Nel box nero a destra apparirà la lista delle tue Pagine. Sotto il nome della tua Pagina (es. Sienna Fox), vedrai una riga `access_token` con una stringa lunghissima.
10. **QUEL TOKEN È PERMANENTE!** Puoi verificarlo incollandolo nell'Access Token Debugger: alla voce Scadenza ci sarà scritto "Mai" (Never).

**Copia quest'ultimo token**. Questo diventerà la tua variabile `META_ACCESS_TOKEN` nel file `.env`, e il tuo bot non smetterà mai di funzionare.

### Trovare i tuoi ID (Facebook Page ID e Instagram Account ID)

Per far funzionare lo script di posting (e incollarli nel file `.env`), Zirelia ha bisogno di sapere esattamente l'ID della Pagina ponte e l'ID del profilo Instagram. Il Graph API Explorer offre la via più semplice senza impazzire coi JSON:

1. Torna nel **Graph API Explorer** (assicurandoti che il Token della tua Pagina sia ancora caricato nel campo "Token di Accesso").
2. Nel riquadro a sinistra intitolato **Informazioni del Token d'Accesso**, individua la riga azzurra "ID dell'app" cliccabile, o meglio ancora, la riga **ID Pagina** che compare quando generi un Page Token.
3. Se non la vedi, nel campo query in alto (dove c'è scritto `GET v26.0 /`) scrivi semplicemente `me` e clicca **Invia** (Submit).
4. La risposta JSON a destra sarà tipo:
   ```json
   {
     "name": "Nome Tua Pagina",
     "id": "123456789012345"
   }
   ```
5. Quel numero `123456789012345` è il tuo **`FACEBOOK_PAGE_ID`**. Copialo e mettilo nel file `.env`.
6. Ora cambia la query in alto scrivendo: `{IL_TUO_PAGE_ID}?fields=instagram_business_account` (sostituisci la parte tra parentesi col numero copiato prima) e clicca di nuovo **Invia**.
7. La risposta diventerà:
   ```json
   {
     "instagram_business_account": {
       "id": "987654321098765"
     },
     "id": "123456789012345"
   }
   ```
8. Quel nuovo numero sotto `instagram_business_account` (es. `987654321098765`) è il tuo **`INSTAGRAM_ACCOUNT_ID`**. Copialo e salvalo nel `.env`.

---

## Parte 4: Configurare le API di Threads (App Separata!)

> ⚠️ **ATTENZIONE**: Threads **NON** è un "prodotto" che puoi aggiungere alla tua app Business esistente (quella usata per Facebook e Instagram). Threads richiede la creazione di una **nuova app separata** con un Use Case dedicato. Anche il token e l'endpoint API sono completamente diversi.

> ⚠️ **DUE ACCOUNT DIVERSI — NON CONFONDERLI!**
> In tutto questo processo userai **due account** diversi:
> - **Account Admin** (es. `lantoniotrento`): il tuo account Facebook personale che gestisce le app sul Developer Portal.
> - **Account Target** (es. `itssiennafox`): l'account Threads della tua AI, dove verranno pubblicati i contenuti.
>
> Ogni passaggio specifica quale account usare.

### 4.1 Creare l'App per Threads

*👤 Usa il tuo **account Admin** sul Developer Portal.*

1. Vai su [developers.facebook.com/apps/](https://developers.facebook.com/apps/).
2. Clicca su **Create App** (Crea App).
3. Nella schermata dei **Use Cases** (Casi d'Uso), seleziona **"Access the Threads API"** e clicca Avanti.
4. Dai un nome all'app (es. "Zirelia Threads"). Clicca **Crea App**.

### 4.2 Configurare l'App (URL + Permessi)

*👤 Usa il tuo **account Admin** sul Developer Portal.*

Vai su **Casi d'uso → Accedi all'API Threads → Customize** (Personalizza). Questa pagina contiene tutto: credenziali, URL e permessi.

**① Annota le credenziali** (nella sezione in alto della pagina):

| Campo nella pagina Customize | Cosa è | Dove serve |
|---|---|---|
| **ID dell'app di Threads** | Il `client_id` per l'OAuth | Link OAuth e comandi curl |
| **Chiave segreta di Threads** | Il `client_secret` | Comandi curl e `.env` come `THREADS_APP_SECRET` |

> ⚠️ **L'"ID dell'app di Threads" sulla pagina Customize è DIVERSO dall'App ID in Impostazioni > Di base!** Per il link OAuth devi usare quello della pagina **Customize**.

**② Compila TUTTI i campi URL obbligatori** con lo stesso URL HTTPS:

> ⚠️ **`https://localhost/` NON FUNZIONA!** Meta rifiuta `localhost` come redirect URI per le app Threads. Usa un URL HTTPS reale.

> ⚠️ **ATTENZIONE AI REDIRECT AUTOMATICI**: Se il tuo sito ha un redirect automatico (es. da `/` a `/it/`), il parametro `code` verrà perso! Usa un percorso che **non fa redirect** (es. `https://tuo-sito.github.io/callback`) — la pagina 404 non è un problema, l'importante è che l'URL resti visibile nella barra degli indirizzi col `?code=`.

| Campo | Valore |
|---|---|
| **URL di callback di reindirizzamento** | `https://tuo-sito.github.io/callback` |
| **Disinstalla URL di callback** | `https://tuo-sito.github.io/callback` |
| **Elimina URL di callback** | `https://tuo-sito.github.io/callback` |

**③ Abilita i permessi obbligatori** (nella sezione "Autorizzazioni e funzioni"):
- `threads_basic` (obbligatorio)
- `threads_content_publish` (obbligatorio)
- Opzionali: `threads_manage_replies`, `threads_read_replies`, `threads_manage_insights`

Clicca **Salva**.

### 4.3 Aggiungere l'Account Target come Tester

*👤 Passo 1-3 con **account Admin**, passo 4-6 con **account Target**.*

Finché l'app è in modalità Sviluppo (indicata da "Non pubblicata" nel menu laterale), solo gli utenti aggiunti come "Tester" possono autorizzare l'app.

**Dal Developer Portal (account Admin):**
1. Nel menu laterale, vai su **Ruoli dell'app (App Roles) → Ruoli (Roles)**.
2. Clicca **Aggiungi persone (Add People)** e seleziona **Tester di Threads (Threads Tester)**.
3. Inserisci lo **username Threads dell'account Target** (es. `itssiennafox` — senza la @).

**Dall'app Threads sul telefono (account Target):**
4. Fai login sull'app **Threads** sul telefono con l'**account Target**.
5. Vai su **☰ → Impostazioni e privacy → Account → Autorizzazioni del sito web → Inviti**.
6. Accetta l'invito dalla tua app.

> ⚠️ Se non trovi "Autorizzazioni del sito web", prova: **Impostazioni → Privacy → Inviti alle app**. L'interfaccia cambia spesso. Se il profilo Target è privato, rendilo **pubblico** prima.

### 4.4 Generare il Token di Threads

Ci sono **due metodi**. Prova prima il Metodo A (più semplice).

#### Metodo A: Generatore Token dalla Dashboard (Raccomandato)

*👤 Usa il tuo **account Admin** sul Developer Portal.*

1. Vai su **Casi d'uso → Accedi all'API Threads → Customize**.
2. Scorri fino alla sezione **"Generatore di token utente"** in fondo alla pagina.
3. Accanto al nome del tuo tester (es. itssiennafox) dovrebbe esserci un pulsante **"Genera token"**.
4. Clicca per generare direttamente un **token di lunga durata** senza bisogno del flusso OAuth manuale.
5. Copia il token e mettilo nel `.env` come `THREADS_ACCESS_TOKEN`.

> 💡 Se il pulsante non compare o dà errore, usa il Metodo B.

#### Metodo B: Flusso OAuth Manuale

> ⚠️ **Devi essere loggato su Threads come l'account TARGET, NON come l'account admin!**

**Passo 1** — Apri questo URL nel browser (sostituisci i valori con quelli dalla pagina Customize del passo 4.2):

```
https://threads.net/oauth/authorize?client_id={ID_APP_THREADS}&redirect_uri={IL_TUO_REDIRECT_URI}&scope=threads_basic,threads_content_publish&response_type=code
```

**Passo 2** — Autorizza l'app (loggato come l'account Target).

**Passo 3** — Il browser ti porterà al tuo redirect URI con `?code=ABC123...#_` nella barra. **Copia la parte dopo `?code=` e prima di `#_`**.

**Passo 4** — Scambia il codice con un token di breve durata (da PowerShell):

```bash
curl -X POST "https://graph.threads.net/oauth/access_token" \
  -d "client_id={ID_APP_THREADS}" \
  -d "client_secret={CHIAVE_SEGRETA_THREADS}" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri={IL_TUO_REDIRECT_URI}" \
  -d "code={IL_CODICE_COPIATO}"
```

> ⚠️ Il `redirect_uri` deve essere **identico** a quello impostato al passo 4.2 (inclusa la barra finale `/`).

**Passo 5** — Dalla risposta otterrai `access_token` e `user_id`. Salva entrambi! Il `user_id` è il tuo `THREADS_USER_ID`.

**Passo 6** — Scambia il token di breve durata con uno di **lunga durata** (60 giorni):

```bash
curl -s "https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret={CHIAVE_SEGRETA_THREADS}&access_token={TOKEN_BREVE_DURATA}"
```

**Passo 7** — Il token restituito è il tuo **`THREADS_ACCESS_TOKEN`**. Copialo nel `.env`.

### 4.5 Rinnovo del Token (60 giorni)

> ⚠️ **Il token Threads NON è permanente!** Dura **60 giorni** e va rinnovato. Per rinnovarlo prima della scadenza:
> ```bash
> curl -s "https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token={IL_TUO_TOKEN_ATTUALE}"
> ```
> Un buon approccio è creare un cron job che rinnova il token ogni 50 giorni.

### 4.6 Trovare il Threads User ID

Se non lo hai annotato durante la creazione del token, puoi recuperarlo così:

```bash
curl -s "https://graph.threads.net/v1.0/me?access_token={THREADS_ACCESS_TOKEN}"
```

La risposta conterrà `"id": "123456789"` — quello è il tuo `THREADS_USER_ID`.

---

## Parte 5: Riepilogo Credenziali

Alla fine del processo, dovresti avere queste credenziali nel tuo file `.env`:

**Per Facebook & Instagram** (dalla tua app Business):
1. `META_APP_ID`: dalla Dashboard principale dell'app.
2. `META_APP_SECRET`: scorrendo in basso nella Dashboard (devi cliccare un bottone per mostrarla).
3. `META_ACCESS_TOKEN`: il Page Access Token **permanente** generato tramite il Graph API Explorer.
4. `FACEBOOK_PAGE_ID`: trovato tramite Explorer.
5. `INSTAGRAM_ACCOUNT_ID`: trovato tramite Explorer.

**Per Threads** (dalla tua app separata con Use Case "Access the Threads API"):
6. `THREADS_APP_SECRET`: la Chiave segreta di Threads dalla pagina **Customize** (serve per il refresh del token).
7. `THREADS_ACCESS_TOKEN`: il token di lunga durata (60 giorni) ottenuto dal Generatore Token o dal flusso OAuth.
8. `THREADS_USER_ID`: il tuo ID utente Threads, ottenuto durante lo scambio del codice o tramite l'endpoint `me`.

### Note Finali per la Produzione

*   **Scadenza Token Facebook/Instagram**: Se hai seguito correttamente il passaggio per ottenere il **Page Access Token Permanente**, questo **non scadrà mai**. Funzionerà a tempo indeterminato a meno che tu non cambi la password di Facebook o revochi manualmente l'accesso all'App dalle impostazioni.
*   **Scadenza Token Threads**: Il token Threads dura **60 giorni** e va rinnovato. Puoi usare l'endpoint `refresh_access_token` per estenderlo di altri 60 giorni. Se scade, dovrai ripetere il flusso OAuth. Un buon approccio è creare un cron job che rinnova il token ogni 50 giorni.
*   **App Review (Revisione App)**: Finché sei l'unica persona ad usare l'app (in qualità di Amministratore/Tester), entrambe le app possono rimanere in modalità **"Sviluppo" (Development)**. Non c'è bisogno di sottometterle alla lunga revisione di Meta.
