```markdown
# Sistema di Gestione Colonnine di Ricarica
Un sistema completo per la gestione e il monitoraggio di stazioni di ricarica per veicoli elettrici, sviluppato con Django e compatibile con il protocollo OCPP (Open Charge Point Protocol).

## Indice
- [Caratteristiche](#caratteristiche)
- [Architettura](#architettura)
- [Installazione](#installazione)
- [Configurazione](#configurazione)
- [API Endpoints](#api-endpoints)
- [Modelli di Dati](#modelli-di-dati)
- [Utilizzo](#utilizzo)
- [Testing](#testing)
- [Contribuire](#contribuire)
- [Licenza](#licenza)

## Caratteristiche

### Funzionalità Principali
- **Gestione Stazioni**: Monitoraggio completo delle colonnine di ricarica
- **Tracking Sessioni**: Registrazione e gestione delle sessioni di ricarica
- **Protocollo OCPP**: Supporto per messaggi OCPP standard
- **API REST**: Interfacce JSON per integrazione con sistemi esterni
- **Monitoraggio Real-time**: ultimo segnale e status delle stazioni
- **Dashboard Ready**: Endpoint ottimizzati per dashboard e applicazioni mobile

### Caratteristiche Tecniche
- **Framework**: Django 4.2+
- **Database**: PostgreSQL
- **API**: REST JSON
- **Protocollo**: OCPP compatibile
- **Architettura**: Modulare e scalabile

## Architettura

```
charging_system/
├── charging_system/          # Configurazione principale Django
│   ├── settings.py          # Impostazioni del progetto
│   ├── urls.py             # URL routing principale
│   └── wsgi.py             # WSGI configuration
├── stations/               # App principale per le stazioni
│   ├── models.py           # Modelli di dati
│   ├── views.py            # Logica delle API
│   ├── urls.py             # URL routing dell'app
│   └── admin.py            # Configurazione admin
└── manage.py               # Script di gestione Django
```

## Installazione

### Prerequisiti
- Python 3.8+
- pip (Python package manager)
- Virtualenv (raccomandato)

### Setup del Progetto
1. **Clona il repository**
    ```bash
    git clone <repository-url>
    cd charging_system
    ```

2. **Crea ambiente virtuale**
    ```bash
    python -m venv charging_station_env
    # Windows
    charging_station_env\Scripts\activate
    # Linux/Mac
    source charging_station_env/bin/activate
    ```

3. **Installa dipendenze**
    ```bash
    pip install django==4.2.16
    pip install djangorestframework  # Se necessario per future estensioni
    ```

4. **Configura il database**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Crea superuser (opzionale)**
    ```bash
    python manage.py createsuperuser
    ```

6. **Avvia il server**
    ```bash
    python manage.py runserver
    ```

Il server sarà disponibile su `http://127.0.0.1:8000/`

## Configurazione

### Impostazioni Database
Il progetto è configurato per SQLite di default. Per ambienti di produzione, modifica `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'charging_system_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Variabili d'Ambiente
Crea un file `.env` per le configurazioni sensibili:
```
SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

## API Endpoints

### Base URL: `/api/`

| Endpoint                          | Metodo | Descrizione                    | Parametri                       |
|------------------------------------|--------|--------------------------------|---------------------------------|
| `/api/stations/`                  | GET    | Lista tutte le stazioni        | -                               |
| `/api/stations/{station_id}/`      | GET    | Dettagli stazione specifica    | `station_id`: ID della stazione |
| `/api/stations/{station_id}/status/` | POST | Aggiorna status stazione       | `station_id`: ID della stazione |

### Esempi di Risposta

#### GET `/api/stations/`
```json
{
  "stations": [
    {
      "id": 1,
      "station_id": "CS001",
      "name": "Stazione Centro",
      "status": "available",
      "is_online": true,
      "ultimo_segnale": "2025-07-23T16:09:26.881337+00:00"
    }
  ]
}
```

#### GET `/api/stations/CS001/`
```json
{
  "station_id": "CS001",
  "name": "Stazione Centro",
  "power_capacity": 22.0,
  "is_online": true,
  "active_sessions": 0,
  "recent_messages": [
    {
      "action": "StatusNotification",
      "timestamp": "2025-07-23T16:09:26.881337+00:00",
      "data": {"status": "available"}
    }
  ]
}
```

#### POST `/api/stations/CS001/status/`
**Request Body**
```json
{
  "status": "occupied",
  "connector_id": 1
}
```
**Response**
```json
{
  "success": true,
  "message": "Status updated"
}
```

## Modelli di Dati

### Stazione_ricarica
Rappresenta una colonnina di ricarica fisica.

| Campo            | Tipo         | Descrizione                                 |
|------------------|--------------|---------------------------------------------|
| `station_id`     | CharField    | ID univoco della stazione                   |
| `name`           | CharField    | Nome descrittivo                            |
| `location`       | CharField    | Posizione geografica                        |
| `power_capacity` | FloatField   | Capacità in kW                              |
| `status`         | CharField    | Stato attuale (available, occupied, faulted, unavailable) |
| `is_online`      | BooleanField | Connessione attiva                          |
| `ultimo_segnale` | DateTimeField| Ultimo heartbeat ricevuto                   |

### Sessione_ricarica
Traccia le sessioni di ricarica individuali.

| Campo             | Tipo         | Descrizione                  |
|-------------------|--------------|------------------------------|
| `session_id`      | CharField    | ID univoco sessione          |
| `station`         | ForeignKey   | Riferimento alla stazione    |
| `start_time`      | DateTimeField| Inizio ricarica              |
| `end_time`        | DateTimeField| Fine ricarica (null se attiva)|
| `energy_delivered`| FloatField   | Energia erogata in kWh       |
| `user_id`         | CharField    | Identificativo utente        |

### OCPP_Messaggio
Registra i messaggi del protocollo OCPP.

| Campo         | Tipo         | Descrizione                      |
|---------------|--------------|----------------------------------|
| `station`     | ForeignKey   | Stazione mittente                |
| `message_type`| CharField    | Tipo messaggio (call, callresult, callerror)|
| `action`      | CharField    | Azione OCPP                      |
| `message_data`| JSONField    | Payload del messaggio            |
| `timestamp`   | DateTimeField| Timestamp ricezione              |

## Utilizzo

### Monitoraggio Stazioni
```python
# Ottenere tutte le stazioni online
from stations.models import Stazione_ricarica
online_stations = Stazione_ricarica.objects.filter(is_online=True)

# Stazioni disponibili per ricarica
available_stations = Stazione_ricarica.objects.filter(
    status='available', 
    is_online=True
)
```

### Gestione Sessioni
```python
# Sessioni attive
from stations.models import Sessione_ricarica
active_sessions = Sessione_ricarica.objects.filter(end_time__isnull=True)

# Energia totale erogata oggi
from django.utils import timezone
today = timezone.now().date()
total_energy = Sessione_ricarica.objects.filter(
    start_time__date=today
).aggregate(total=models.Sum('energy_delivered'))
```

## Testing

### Test delle API
```bash
# Test endpoint lista stazioni
curl http://127.0.0.1:8000/api/stations/

# Test dettagli stazione
curl http://127.0.0.1:8000/api/stations/CS001/

# Test aggiornamento status
curl -X POST http://127.0.0.1:8000/api/stations/CS001/status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "occupied"}'
```

### Unit Tests
```bash
python manage.py test stations
```

## Sviluppo

### Struttura del Codice
- **Models**: Definizione dei dati in `stations/models.py`
- **Views**: Logica API in `stations/views.py`
- **URLs**: Routing in `stations/urls.py`
- **Admin**: Interfaccia admin in `stations/admin.py`

### Debug Mode
Per abilitare il debug dettagliato, le view includono print statements che mostrano:
- Numero di stazioni trovate
- Processamento di ogni stazione
- Dati JSON generati

### Estensioni Future
- [ ] Autenticazione JWT
- [ ] WebSocket per aggiornamenti real-time
- [ ] Dashboard web integrata
- [ ] Integrazione con sistemi di pagamento
- [ ] Notifiche push
- [ ] Analytics avanzate

## Licenza
Questo progetto è distribuito sotto licenza MIT.
```
