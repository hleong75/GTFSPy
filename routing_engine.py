"""
Moteur de routage - Calcule les itinéraires optimaux entre deux points
en utilisant les données GTFS
"""

import heapq
from datetime import datetime, timedelta


class RoutingEngine:
    """Moteur de routage pour calculer les itinéraires de transport en commun"""
    
    def __init__(self, gtfs_manager):
        self.gtfs_manager = gtfs_manager
    
    def find_route(self, origin, destination, departure_time=None):
        """
        Trouve l'itinéraire optimal entre deux points
        
        Args:
            origin: tuple (lat, lon) du point de départ
            destination: tuple (lat, lon) du point d'arrivée
            departure_time: datetime optionnel pour le départ
        
        Returns:
            Liste des étapes de l'itinéraire ou None si aucun itinéraire trouvé
        """
        if not self.gtfs_manager.is_gtfs_loaded():
            print("Aucune donnée GTFS chargée")
            return None
        
        # Trouver les arrêts les plus proches
        origin_stop, origin_dist = self.gtfs_manager.find_nearest_stop(
            origin[0], origin[1]
        )
        destination_stop, dest_dist = self.gtfs_manager.find_nearest_stop(
            destination[0], destination[1]
        )
        
        if not origin_stop or not destination_stop:
            print("Impossible de trouver des arrêts à proximité")
            return None
        
        # Utiliser l'algorithme A* pour trouver le meilleur itinéraire
        route = self.a_star_search(
            origin_stop['stop_id'],
            destination_stop['stop_id'],
            departure_time or datetime.now()
        )
        
        if route:
            # Convertir l'itinéraire en format utilisable
            return self.format_route(route, origin, destination)
        
        return None
    
    def a_star_search(self, start_stop_id, end_stop_id, departure_time):
        """
        Algorithme A* pour trouver le meilleur chemin entre deux arrêts
        
        Args:
            start_stop_id: ID de l'arrêt de départ
            end_stop_id: ID de l'arrêt d'arrivée
            departure_time: Heure de départ
        
        Returns:
            Liste des arrêts formant l'itinéraire
        """
        # File de priorité: (coût_total, coût_actuel, arrêt_actuel, chemin)
        open_set = []
        heapq.heappush(open_set, (0, 0, start_stop_id, [start_stop_id]))
        
        # Ensemble des arrêts visités
        visited = set()
        
        while open_set:
            total_cost, current_cost, current_stop, path = heapq.heappop(open_set)
            
            # Si on a atteint la destination
            if current_stop == end_stop_id:
                return path
            
            # Si déjà visité, passer
            if current_stop in visited:
                continue
            
            visited.add(current_stop)
            
            # Trouver les arrêts voisins (arrêts connectés par des trajets)
            neighbors = self.get_connected_stops(current_stop)
            
            for next_stop_id, transfer_cost in neighbors:
                if next_stop_id not in visited:
                    new_cost = current_cost + transfer_cost
                    heuristic = self.calculate_heuristic(next_stop_id, end_stop_id)
                    total = new_cost + heuristic
                    
                    new_path = path + [next_stop_id]
                    heapq.heappush(open_set, (total, new_cost, next_stop_id, new_path))
        
        return None
    
    def get_connected_stops(self, stop_id):
        """
        Récupère les arrêts connectés à un arrêt donné via des trajets
        Utilise l'index stop_to_trips pour des performances optimales
        
        Returns:
            Liste de tuples (stop_id, coût)
        """
        connected = []
        
        # Utiliser l'index pour trouver rapidement les trajets
        if stop_id in self.gtfs_manager.stop_to_trips_index:
            for trip_info in self.gtfs_manager.stop_to_trips_index[stop_id]:
                # Si un arrêt suivant existe
                if 'next_stop_id' in trip_info:
                    next_stop_id = trip_info['next_stop_id']
                    # Coût basé sur le temps de trajet
                    cost = self.calculate_time_cost(
                        trip_info['departure_time'],
                        trip_info['next_arrival_time']
                    )
                    connected.append((next_stop_id, cost))
        
        return connected
    
    def calculate_time_cost(self, departure_time, arrival_time):
        """Calcule le coût en temps entre deux horaires"""
        if not departure_time or not arrival_time:
            return 1  # Coût par défaut
        
        try:
            # Format GTFS: HH:MM:SS
            dep_parts = departure_time.split(':')
            arr_parts = arrival_time.split(':')
            
            dep_minutes = int(dep_parts[0]) * 60 + int(dep_parts[1])
            arr_minutes = int(arr_parts[0]) * 60 + int(arr_parts[1])
            
            # Différence en minutes
            diff = arr_minutes - dep_minutes
            if diff < 0:
                diff += 24 * 60  # Passage minuit
            
            return diff / 60  # Convertir en heures
        except:
            return 1
    
    def calculate_heuristic(self, stop_id1, stop_id2):
        """
        Calcule l'heuristique (distance estimée) entre deux arrêts
        pour l'algorithme A*
        """
        try:
            stop1 = self.gtfs_manager.stops.get(stop_id1)
            stop2 = self.gtfs_manager.stops.get(stop_id2)
            
            if not stop1 or not stop2:
                return 0
            
            lat1 = float(stop1['stop_lat'])
            lon1 = float(stop1['stop_lon'])
            lat2 = float(stop2['stop_lat'])
            lon2 = float(stop2['stop_lon'])
            
            # Distance en mètres divisée par vitesse moyenne (30 km/h)
            distance = self.gtfs_manager.calculate_distance(lat1, lon1, lat2, lon2)
            return distance / (30000 / 60)  # Temps estimé en heures
        except:
            return 0
    
    def format_route(self, stop_ids, origin, destination):
        """
        Formate l'itinéraire pour l'affichage
        
        Args:
            stop_ids: Liste des IDs d'arrêts
            origin: Coordonnées d'origine
            destination: Coordonnées de destination
        
        Returns:
            Liste des étapes de l'itinéraire avec coordonnées
        """
        route = []
        
        # Ajouter le point de départ
        route.append({
            'type': 'origin',
            'lat': origin[0],
            'lon': origin[1],
            'name': 'Départ'
        })
        
        # Ajouter les arrêts
        for stop_id in stop_ids:
            stop = self.gtfs_manager.stops.get(stop_id)
            if stop:
                route.append({
                    'type': 'stop',
                    'lat': float(stop['stop_lat']),
                    'lon': float(stop['stop_lon']),
                    'name': stop.get('stop_name', 'Arrêt'),
                    'stop_id': stop_id
                })
        
        # Ajouter le point d'arrivée
        route.append({
            'type': 'destination',
            'lat': destination[0],
            'lon': destination[1],
            'name': 'Arrivée'
        })
        
        return route
