# Shopper! - Piattaforma E-commerce

* **Titolo Progetto:** Shopper!
* **Studente:** Giada Schicchi (Matricola: 7137452)
* **Data di fine progetto:** 02/06/2026
* **Tipologia di Progetto:** Full-Stack Web Application
* **Framework Utilizzato:** Django 6.0.6

**Shopper!** è un'applicazione web e-commerce sviluppata in Python 3.14. Il progetto soddisfa completamente tutti i requisiti previsti e richiesti nel pdf di istruzione fornito per la **Traccia 1**.

---

## Funzionalità Principali (richieste nella traccia):

### Autenticazione e Gestione Ruoli
Il sistema prevede una separazione dei permessi basata sul tipo di utente loggato:
* **Cliente Standard:** Può navigare nel catalogo, visualizzare i dettagli dei prodotti, gestire il proprio carrello, procedere al checkout e consultare il proprio storico degli ordini.
* **Store Manager (Amministratore):** Oltre alle funzionalità del cliente, ha accesso esclusivo agli strumenti di gestione del negozio (CRUD dei prodotti) direttamente dal frontend e può monitorare tutti gli ordini effettuati sulla piattaforma.
* **Superadmin:** Ha accesso completo a tutte le funzionalità del sistema, inclusa la gestione degli utenti e dei permessi tramite il pannello di amministrazione di Django.

### Catalogo Prodotti e Ricerca Avanzata
* **Filtri e Query:** Barra di ricerca combinata con filtri per categoria (barra laterale).
* **Scheda Dettaglio:** Pagina dedicata per ciascun articolo con descrizione, prezzo e disponibilità.
* **Gestione Stock:** Se un prodotto ha uno stock pari a `0`, il pulsante di acquisto viene disabilitato (diventa grigio, mostra la scritta **ESAURITO** ed un simbolo di divieto).

### Carrello della Spesa
* **Aggiunta al carrello:** Permette di incrementare le quantità direttamente dalla home solo se loggati. Il sistema impedisce di inserire nel carrello una quantità superiore allo stock disponibile nel database.
* **Modifica dei prodotti:** Ogni riga del carrello ha un pulsante a forma di cestino per eliminare completamente il prodotto, e due simboli (+ e -) per incrementare o decrementare la quantità, sempre rispettando i limiti di stock.
* **Calcolo automatico:** Conteggio in tempo reale dei costi per singolo prodotto (se selezionato più volte) e del totale complessivo nel carrello.

### Checkout e Flusso degli Ordini
* **Transazione:** Al momento della conferma dell'ordine, i prodotti che erano presenti nel carrello dell'utente vengono rimossi anche dal database.
* **Aggiornamento Inventario:** Il sistema decrementa automaticamente le quantità acquistate dallo stock dei rispettivi prodotti nel database (`product.stock -= item.quantity`).
* **Storico degli Ordini:**   * I clienti vedono solo i propri acquisti ordinati dal più recente al più vecchio;
                              * Il manager ha una dashboard globale per supervisionare le vendite di tutto l'e-commerce.

---

## Tecnologie Utilizzate

* **Backend:** Python 3.14, Django Framework 6.0.6 (MVT Architecture).
* **Database:** SQLite (predefinito in Django).
* **Frontend:** HTML5, CSS3 (Palette Rosa Pastello e Shopper Theme), Bootstrap 5.3, FontAwesome 6.0 (per icone).

---

## Istruzioni per l'Installazione in Locale

Seguire questi passaggi per avviare il progetto sul proprio computer locale:

1.  **Clonare la repository o estrarre la cartella del progetto e posizionarsi al suo interno:**
    ```bash
    cd percorso/della/cartella/del/progetto
    ```

2.  **Creare e attivare un ambiente virtuale:**
    ```bash
    python -m venv .venv
    #su Windows:
    .venv\Scripts\activate
    #su macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Installare le dipendenze richieste dal progetto:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Eseguire le migrazioni (se necessario):**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Avviare il server di sviluppo:**
    ```bash
    python manage.py runserver
    ```
6. **Aprire il browser e navigare all'indirizzo:** `http://127.0.0.1:8000/`

---

## Database e Dati Demo
Il file del database incluso nel progetto si chiama **`db.sqlite3`**. 
Si conferma che il database contiene già dei dati demo pre-caricati (categorie, prodotti con scorte diversificate, utenti e ordini passati) per permettere una valutazione immediata di tutte le funzionalità.

## Online Deployment Link
* [Se hai caricato il sito online, incolla il link qui. Altrimenti scrivi: "Progetto sviluppato e testato per l'esecuzione in locale."]

---

## Credenziali Demo

Sono stati creati tre tipologie di profili nel database:

### 1. Superuser (Django Admin)
* **Username:** `admingiada`
* **Password:** `nessunapassword`
* *Permessi:* Active, Staff status, Superuser status.


### 2. Store Manager (Amministratore)
* **Username:** `casual_manager`
* **Password:** `storeadmin`
* *Permessi:* Active, Staff status

### 3. Utente Standard (Cliente)
* **Username:** `user123456`
* **Password:** `clienterandom`
* *Permessi:* Active.

---

## Test personalmente eseguiti

Per verificare il corretto funzionamento di tutte le componenti del progetto, ho eseguito con successo i seguenti test:

1.  **1. Navigazione anonima:** Provo ad aggiungere un prodotto al carrello e il sistema mi reindirizza automaticamente alla pagina di Login per sicurezza.
2.  **2. Acquisto (lato Cliente):** Effettuo il login come `cliente`, poi aggiungo alcuni prodotti al carrello. Vado alla pagina dedicata al checkout, clicco su "Procedi all'acquisto", compilo il form e confermo. Verifico subito lo svuotamento del carrello e la comparsa dell'ordine nello storico.
3.  **3. Controllo Stock:** Vado nel pannello di amministrazione (`/admin`), imposto lo stock di un prodotto a `0', poi, sulla vetrina del sito, il pulsante sarà diventato grigio fisso con la scritta **ESAURITO** e il cursore bloccato. Verifico anche acquistando il massimo dello stock disponibile di un prodotto e (dopo l'acquisto confermato) apparirà subito come esaurito.
4.  **4. Gestione Manager:** Effettuo il logout e accedo con l'utente `manager`. Si nota immediatamente la comparsa dei pulsanti di amministrazione nella vetrina. Cliccando su "Modifica" su un prodotto potrò aggiornarne il prezzo, o usarne il pannello ordini manager per visionare il flusso di acquisti effettuati dai clienti.