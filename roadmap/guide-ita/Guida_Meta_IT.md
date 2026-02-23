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

## Parte 1: Creazione della Meta App

1. Vai sul [Meta for Developers Portal](https://developers.facebook.com/) e accedi con il tuo account Facebook.
2. Se è la prima volta, registrati come Meta Developer (è gratuito).
3. Clicca su **My Apps** (Le mie App) in alto a destra, poi su **Create App** (Crea App).
4. Scegli **Other** (Altro) come caso d'uso e vai avanti.
5. Scegli **Business** come tipo di app e vai avanti.
6. Dai un nome alla tua app (es. "Zirelia AutoPoster") e inserisci un'email di contatto. Lascia il Business Account vuoto per ora, a meno che tu non ne abbia già uno pronto. Clicca su **Create App**.

---

## Parte 2: Configurare le API Graph di Instagram

L'API Graph di Instagram ti permette di pubblicare Foto e Video (Reels) sul tuo account Professionale.

1. Nella Dashboard della tua App, scorri in basso fino a **Add products to your app** (Aggiungi prodotti alla tua app).
2. Trova **Instagram Graph API** e clicca su **Set Up** (Configura).
3. Nella barra laterale sinistra, sotto **Instagram Graph API**, clicca su **API Setup**.
4. Vedrai un pulsante **Add Facebook Login for Business**. Cliccalo, poiché è il sistema di autenticazione che Meta usa sotto il cofano.
5. Segui le istruzioni a schermo per aggiungere il prodotto.
6. Ora dobbiamo generare un **Access Token** (Token di Accesso). Il modo più semplice per farlo senza programmare codice OAuth personalizzato è usare il **Graph API Explorer**:
    * Dal menu in alto vai su **Tools > Graph API Explorer**.
    * Nel menu a tendina "Meta App", seleziona la tua nuova app.
    * Sotto "User or Page" (Utente o Pagina), seleziona **Get Page Access Token** (Ottieni Token di Accesso Pagina). Ti verrà chiesto di accedere e autorizzare l'app ad accedere alla tua Pagina Facebook e all'account Instagram collegato.
    * Quando te lo chiede, assicurati di concedere questi permessi:
        * `instagram_basic`
        * `instagram_content_publish`
        * `pages_show_list`
        * `pages_read_engagement`
    * Una volta autorizzato, vedrai un token nel campo "Access Token". **Attenzione: questo token è temporaneo e scade in 1 ora.**

### Ottenere un Token a lunga scadenza (Long-Lived) per Instagram

Per un bot autonomo, ti serve un token che non scada ogni ora.

1. Rimanendo nel Graph API Explorer, clicca sul piccolo punto esclamativo blu (ℹ️) accanto al tuo token temporaneo.
2. Clicca su **Open in Access Token Tool** (Apri nello strumento per i Token).
3. In fondo a quella pagina, clicca su **Extend Access Token** (Estendi Token).
4. Questo ti genererà un token a lunga scadenza (valido per 60 giorni). **Copia questo token**. Questo diventerà la tua variabile `META_ACCESS_TOKEN`.

### Trovare i tuoi ID

Per far funzionare il codice ti servono anche l'ID della Pagina Facebook e l'ID dell'Account Instagram.

1. Nel Graph API Explorer, scrivi `me/accounts` nella barra di query in alto e clicca **Submit** (Invia).
2. Nella risposta JSON (il testo nero a destra), cerca l'ID della Pagina Facebook collegata (sarà un numero lungo). Questo è il tuo `FACEBOOK_PAGE_ID`.
3. Adesso, scrivi `{FACEBOOK_PAGE_ID}?fields=instagram_business_account` nella barra di query (sostituendo col numero che hai appena trovato) e clicca **Submit**.
4. La risposta conterrà un campo `instagram_business_account` con un altro ID. Questo è il tuo `INSTAGRAM_ACCOUNT_ID`.

---

## Parte 3: Configurare le API di Threads

L'API per Threads è separata da quella di Instagram, ma viene gestita sempre dentro la stessa Meta App.

1. Torna alla Dashboard della tua App.
2. Clicca su **Add Product** (Aggiungi Prodotto) nella barra a sinistra.
3. Trova **Threads API** e clicca **Set Up**.
4. Nella barra di sinistra sotto Threads API, vai su **Settings** (Impostazioni).
5. Devi configurare le impostazioni OAuth. Aggiungi `https://localhost` o la tua URL locale di sviluppo sotto i **Valid OAuth Redirect URIs**.
6. Come per Instagram, serve un Token. Meta mette a disposizione un [Threads API Token Generator Tool](https://developers.facebook.com/docs/threads/get-started) apposito per facilitare i test.
    * In alternativa, puoi usare di nuovo il Graph API Explorer, ma stavolta chiedendo i permessi specifici di Threads (`threads_basic`, `threads_content_publish`).
7. Genera un token a lunga scadenza seguendo una procedura molto simile a quella di Instagram (scambiando il token breve con uno lungo tramite l'endpoint `/oauth/access_token`).
    * *Nota: Anche i token di Threads in genere durano 60 giorni e vanno rinfrescati.*

---

## Parte 4: Riepilogo Credenziali

Alla fine del processo, dovresti avere queste 5 credenziali indispensabili per far funzionare lo script in Python:

1. `META_APP_ID`: dalla Dashboard principale dell'app.
2. `META_APP_SECRET`: scorrendo in basso nella Dashboard (devi cliccare un bottone per mostrarla).
3. `META_ACCESS_TOKEN`: il token di 60 giorni che hai generato.
4. `FACEBOOK_PAGE_ID`: trovato tramite Explorer.
5. `INSTAGRAM_ACCOUNT_ID`: trovato tramite Explorer.

*(Più token e ID simili per Threads, se vuoi postare anche lì).*

### Note Finali per la Produzione

*   **Scadenza Token**: I token di 60 giorni **scadranno**. Più avanti nello sviluppo dovremo scrivere uno script automatico che "rinfresca" il token ogni 50 giorni (il processo è gratuito e può essere fatto via codice).
*   **App Review (Revisione App)**: Finché sei l'unica persona ad usare l'app (in qualità di Amministratore), l'app può rimanere in modalità **"Sviluppo" (Development)**. Non c'è bisogno di sottometterla alla lunga revisione di Meta e di farla diventare Pubblica. Rimane privata e funzionante al 100% per i tuoi account.
