from django.shortcuts import render, get_object_or_404 # Funzioni di Django per renderizzare template e gestire oggetti non trovati
from django.http import JsonResponse #  Classe per restituire risposte JSON dalle view
from django.views.decorators.csrf import csrf_exempt # Decoratore per disabilitare la protezione CSRF
from django.utils import timezone # timezone è un modulo che gestisce le date e le ore 
import json 
from .models import Stazione_ricarica, Sessione_ricarica, OCPP_Messaggio 

# view function per ottenere la lista delle stazioni di ricarica.
def station_list(request):
    """Lista tutte le colonnine"""
    print("DEBUG: Iniziando station_list")  # Debug
    stations= Stazione_ricarica.objects.all() # variabile che contiene tutte le righe della tabella Stazione_ricarica (QuerySet)
    print(f"DEBUG: Trovate {stations.count()} colonnine")  # Debug
    stations_data = [] # lista inizialmente vuota

    for station in stations:
        print(f"DEBUG: Processando stazione {station.station_id}")  # Debug
        stations_data.append({
            'id': station.id,
            'station_id': station.station_id,
            'name': station.name,
            'status': station.status,
            'is_online': station.is_online,
            'ultimo_segnale': station.ultimo_segnale.isoformat() if station.ultimo_segnale else None
        })

    print(f"DEBUG: stations_data creato: {stations_data}")  # Debug
    return JsonResponse({'stations': stations_data}) # restituisce in formato JSON la lista delle stazioni



def station_detail(request,station_id):
    """Dettagli di una specifica colonnina"""
    station = get_object_or_404(Stazione_ricarica, station_id=station_id) # restituisce la stazione con il specifico id passato

    # Sessioni attive(cerca tutte le sessione di ricarica associata a quella determiata stazione)
    sessione_attiva= Sessione_ricarica.objects.filter(
        station=station,
        end_time__isnull=True #filtra solo le sessioni attive non ancora concluse
   )

    # Ultimi Messaggi OCPP
    recent_message= OCPP_Messaggio.objects.filter(
        station=station,
   ).order_by('-timestamp')[:10] # prende solo i primi 10 messaggi in ordine descrescente

    station_data={
    'station_id': station.station_id,
    'name': station.name,
    'power_capacity': station.power_capacity,
    'is_online': station.is_online,
    'status': len(station.status),
    'recent_messages': [
        {
          'action': msg.action,
          'timestamp': msg.timestamp.isoformat(),
          'data': msg.message_data
        } for msg in recent_message
    ]
    }

    return JsonResponse(station_data)

@csrf_exempt
def update_station_status(request, station_id):
    """Aggiorna lo status di una colonnina (simulazione OCPP)"""
    if request.method == 'POST':
        station = get_object_or_404(Stazione_ricarica, station_id=station_id)
        data = json.loads(request.body)
        
        # Aggiorna status
        if 'status' in data:
            station.status = data['status']
        
        # Aggiorna l'ultimo segnale
        station.ultimo_segnale = timezone.now()
        station.is_online = True
        station.save()
        
        # Salva messaggio OCPP
        OCPP_Messaggio.objects.create(
            station=station,
            message_type='call',
            action='StatusNotification',
            message_data=data
        )
        
        return JsonResponse({'success': True, 'message': 'Status updated'})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)












