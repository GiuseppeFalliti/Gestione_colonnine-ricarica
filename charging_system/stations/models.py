from django.db import models
from django.utils import timezone # timezone è un modulo di django che fornisce funzionalità per gestire le date e le ore 


class Stazione_ricarica(models.Model):
    # 4 tipi di stati possibili della stazione
    STATUS=[
        ('available', 'Disponibile'), # (1_valore è il valore salvato nel db, 2_valore è l'etichetta da mostrare all'utente)
        ('occupied', 'Occupata'),
        ('faulted', 'Guasta'),
        ('unavailable', 'Non disponibile'),
    ]
     
    station_id = models.CharField(max_length=50, unique=True)
    name= models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS, default='available') 
    power_capacity = models.FloatField()  # kW
    is_online = models.BooleanField(default=False) #  Boolean per verificare se la stazione è accesa/spenta (default false)
    ultimo_segnale = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # Data/ora di creazione (impostata automaticamente alla creazione)
    updated_at = models.DateTimeField(auto_now=True) # Data/ora ultimo aggiornamento (aggiornata automaticamente ad ogni modifica)

    # Definiamo che il modello viene rappresentato come una stringa che contine il nome e l'id della stazione di ricarica
    def __str__(self):
        return f"{self.name} ({self.station_id})"


class Sessione_ricarica(models.Model):
    session_id = models.CharField(max_length=50, unique=True) #Primary key
    station= models.ForeignKey(Stazione_ricarica, on_delete=models.CASCADE) #Foreign Key
    user_id= models.CharField(max_length=50)
    start_time= models.DateTimeField() # l'ora di inizio di una sessione di ricarica
    end_time= models.DateTimeField(null=True, blank=True) #  l'ora in cui finisce una sessione di ricarica
    energy_consumed= models.FloatField(default=0.0) # kWh
    transaction_id = models.CharField(max_length=50, null=True, blank=True) # id del pagamento della sessione di ricarica es paypal_txn_ABC123XYZ

    def __str__(self):
        return f"Sessione: {self.session_id} - {self.station.name}"


class OCPP_Messaggio(models.Model):
    MESSAGGIO =[
        ('call', 'Call'),
        ('callresult', 'CallResult'),
        ('callerror', 'CallError'),
    ]

    station=models.ForeignKey(Stazione_ricarica, on_delete=models.CASCADE)
    message_type=models.CharField(max_length=50, choices=MESSAGGIO)
    action = models.CharField(max_length=50)
    message_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.station.station_id} - {self.timestamp}"






