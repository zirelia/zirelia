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
    *(Se vuoi Threads aggiungi anche `threads_basic` e `threads_content_publish`).*
6. Clicca il mega pulsante verde **Genera Token di accesso** e ri-conferma il popup di Facebook.
7. ORA CI SIAMO: Torna sul menu a tendina **Utente o Pagina** e aprilo. Clicca sul **Nome della tua Pagina** (es. "Sienna Fox").
8. La stringa lunghissima al centro dello schermo cambia: **quello è il tuo Token Pagina**! Copiatelo da qualche parte.

### Rendere il Token infinito (Long-Lived)

Per un bot autonomo, ti serve un token che non scada ogni ora.

1. Rimanendo nel Graph API Explorer, clicca sul piccolo punto esclamativo blu (ℹ️) accanto al tuo token temporaneo.
2. Clicca su **Open in Access Token Tool** (Apri nello strumento per i Token).
3. In fondo a quella pagina, clicca su **Extend Access Token** (Estendi Token).
4. Questo ti genererà un token a lunga scadenza (valido per 60 giorni). **Copia questo token**. Questo diventerà la tua variabile `META_ACCESS_TOKEN`.

### Trovare i tuoi ID (Facebook Page ID e Instagram Account ID)

Per far funzionare lo script di posting (e incollarli nel file `.env`), Zirelia ha bisogno di sapere esattamente l'ID della Pagina ponte e l'ID del profilo Instagram. Il Graph API Explorer offre la via più semplice senza impazzire coi JSON:

1. Torna nel **Graph API Explorer** (assicurandoti che il Token della tua Pagina sia ancora caricato nel campo "Token di Accesso").
2. Nel riquadro a sinistra intitolato **Informazioni del Token d'Accesso**, individua la riga azzurra "ID dell'app" cliccabile, o meglio ancora, la riga **ID Pagina** che compare quando generi un Page Token.
3. Se non la vedi, nel campo query in alto (dove c'è scritto `GET v18.0 /`) scrivi semplicemente `me` e clicca **Invia** (Submit).
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

## Parte 3: Configurare le API di Threads

Se vuoi postare anche su Threads, devi aggiungere il relativo prodotto. Nelle App di tipo "Aziendale", Threads potrebbe trovarsi in una sezione diversa rispetto ai riquadri principali.

1. Dal menu a sinistra, clicca su **Casi d'Uso** (se presente) o cerca Threads tra i Prodotti.
2. Se usi i "Casi d'Uso", seleziona l'opzione per personalizzare i permessi e clicca *Aggiungi*. Cerca **Threads API**.
3. Nelle impostazioni specifiche di Threads (se richieste), aggiungi `https://localhost` o la tua URL locale sotto i **Valid OAuth Redirect URIs**.
4. Potrai richiedere il token per Threads direttamente dal Graph API Explorer usando gli stessi passaggi per Instagram, chiedendo però i permessi `threads_basic` e `threads_content_publish`.

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
