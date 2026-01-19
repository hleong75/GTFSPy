"""
Gestionnaire GTFS - Gère l'importation et le traitement des fichiers GTFS
"""

import os
import zipfile
import csv
from datetime import datetime, timedelta


class GTFSManager:
    """Gère les données GTFS (General Transit Feed Specification)"""
    
    def __init__(self, storage_manager):
        self.storage_manager = storage_manager
        self.stops = {}
        self.routes = {}
        self.trips = {}
        self.stop_times = {}
        self.calendar = {}
        self.shapes = {}
        self.stop_to_trips_index = {}  # Index pour accélérer la recherche de trajets par arrêt
        
    def import_gtfs(self, zip_path):
        """Importe un fichier GTFS depuis un fichier ZIP"""
        try:
            # Créer le répertoire de données GTFS si nécessaire
            gtfs_dir = self.storage_manager.get_gtfs_dir()
            
            # Extraire le fichier ZIP
            extract_dir = os.path.join(gtfs_dir, os.path.basename(zip_path).replace('.zip', ''))
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Charger les données GTFS
            self.load_gtfs_data(extract_dir)
            
            # Sauvegarder les métadonnées
            self.storage_manager.save_gtfs_metadata(
                os.path.basename(zip_path),
                extract_dir,
                datetime.now()
            )
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'importation GTFS: {e}")
            return False
    
    def load_gtfs_data(self, gtfs_dir):
        """Charge les données GTFS depuis un répertoire extrait"""
        # Charger les arrêts
        stops_file = os.path.join(gtfs_dir, 'stops.txt')
        if os.path.exists(stops_file):
            self.stops = self.load_csv_to_dict(stops_file, 'stop_id')
        
        # Charger les routes
        routes_file = os.path.join(gtfs_dir, 'routes.txt')
        if os.path.exists(routes_file):
            self.routes = self.load_csv_to_dict(routes_file, 'route_id')
        
        # Charger les trajets
        trips_file = os.path.join(gtfs_dir, 'trips.txt')
        if os.path.exists(trips_file):
            self.trips = self.load_csv_to_dict(trips_file, 'trip_id')
        
        # Charger les horaires d'arrêt
        stop_times_file = os.path.join(gtfs_dir, 'stop_times.txt')
        if os.path.exists(stop_times_file):
            self.stop_times = self.load_stop_times(stop_times_file)
        
        # Charger le calendrier
        calendar_file = os.path.join(gtfs_dir, 'calendar.txt')
        if os.path.exists(calendar_file):
            self.calendar = self.load_csv_to_dict(calendar_file, 'service_id')
        
        # Charger les formes (shapes)
        shapes_file = os.path.join(gtfs_dir, 'shapes.txt')
        if os.path.exists(shapes_file):
            self.shapes = self.load_shapes(shapes_file)
        
        # Construire l'index stop_id -> trips
        self.build_stop_to_trips_index()
    
    def load_csv_to_dict(self, file_path, key_field):
        """Charge un fichier CSV GTFS dans un dictionnaire"""
        data = {}
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    key = row.get(key_field)
                    if key:
                        data[key] = row
        except Exception as e:
            print(f"Erreur lors du chargement de {file_path}: {e}")
        return data
    
    def load_stop_times(self, file_path):
        """Charge les horaires d'arrêt, organisés par trip_id"""
        stop_times = {}
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    trip_id = row.get('trip_id')
                    if trip_id:
                        if trip_id not in stop_times:
                            stop_times[trip_id] = []
                        stop_times[trip_id].append(row)
            
            # Trier par séquence
            for trip_id in stop_times:
                stop_times[trip_id].sort(
                    key=lambda x: int(x.get('stop_sequence', 0))
                )
        except Exception as e:
            print(f"Erreur lors du chargement des stop_times: {e}")
        return stop_times
    
    def load_shapes(self, file_path):
        """Charge les formes géographiques, organisées par shape_id"""
        shapes = {}
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    shape_id = row.get('shape_id')
                    if shape_id:
                        if shape_id not in shapes:
                            shapes[shape_id] = []
                        shapes[shape_id].append(row)
            
            # Trier par séquence
            for shape_id in shapes:
                shapes[shape_id].sort(
                    key=lambda x: int(x.get('shape_pt_sequence', 0))
                )
        except Exception as e:
            print(f"Erreur lors du chargement des shapes: {e}")
        return shapes
    
    def build_stop_to_trips_index(self):
        """Construit un index pour accélérer la recherche de trajets par arrêt"""
        self.stop_to_trips_index = {}
        
        for trip_id, stop_time_list in self.stop_times.items():
            for i, stop_time in enumerate(stop_time_list):
                stop_id = stop_time.get('stop_id')
                if stop_id:
                    if stop_id not in self.stop_to_trips_index:
                        self.stop_to_trips_index[stop_id] = []
                    
                    # Stocker trip_id, position dans le trajet, et l'arrêt suivant s'il existe
                    trip_info = {
                        'trip_id': trip_id,
                        'position': i,
                        'arrival_time': stop_time.get('arrival_time'),
                        'departure_time': stop_time.get('departure_time')
                    }
                    
                    # Ajouter l'arrêt suivant si disponible
                    if i + 1 < len(stop_time_list):
                        trip_info['next_stop_id'] = stop_time_list[i + 1].get('stop_id')
                        trip_info['next_arrival_time'] = stop_time_list[i + 1].get('arrival_time')
                    
                    self.stop_to_trips_index[stop_id].append(trip_info)
    
    def find_nearest_stop(self, lat, lon, max_distance=1000):
        """Trouve l'arrêt le plus proche d'une coordonnée donnée"""
        nearest_stop = None
        min_distance = float('inf')
        
        for stop_id, stop in self.stops.items():
            try:
                stop_lat = float(stop['stop_lat'])
                stop_lon = float(stop['stop_lon'])
                
                # Calcul de la distance approximative (formule simple)
                distance = self.calculate_distance(lat, lon, stop_lat, stop_lon)
                
                if distance < min_distance and distance < max_distance:
                    min_distance = distance
                    nearest_stop = stop
            except (ValueError, KeyError):
                continue
        
        return nearest_stop, min_distance
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calcule la distance entre deux points (formule de Haversine)"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371000  # Rayon de la Terre en mètres
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lon = radians(lon2 - lon1)
        
        a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        return distance
    
    def get_trips_for_stop(self, stop_id):
        """Récupère tous les trajets passant par un arrêt donné (utilise l'index pour performance)"""
        if stop_id in self.stop_to_trips_index:
            trips = []
            for trip_info in self.stop_to_trips_index[stop_id]:
                trips.append({
                    'trip_id': trip_info['trip_id'],
                    'arrival_time': trip_info['arrival_time'],
                    'departure_time': trip_info['departure_time']
                })
            return trips
        return []
    
    def is_gtfs_loaded(self):
        """Vérifie si des données GTFS sont chargées"""
        return len(self.stops) > 0
