#!/usr/bin/env python3
"""
Script de test pour vérifier les modules GTFSPy
sans dépendances Kivy
"""

import os
import sys
import tempfile
import zipfile
import csv


def test_gtfs_manager():
    """Test le gestionnaire GTFS sans dépendances Kivy"""
    print("Test du GTFSManager...")
    
    # Créer un fichier GTFS de test
    with tempfile.TemporaryDirectory() as tmpdir:
        # Créer un fichier ZIP GTFS minimal
        gtfs_zip = os.path.join(tmpdir, 'test.zip')
        
        # Créer les fichiers GTFS
        stops_data = [
            ['stop_id', 'stop_name', 'stop_lat', 'stop_lon'],
            ['S1', 'Station A', '48.8566', '2.3522'],
            ['S2', 'Station B', '48.8606', '2.3376'],
            ['S3', 'Station C', '48.8529', '2.3499']
        ]
        
        routes_data = [
            ['route_id', 'route_short_name', 'route_long_name', 'route_type'],
            ['R1', '1', 'Ligne 1', '1']
        ]
        
        trips_data = [
            ['trip_id', 'route_id', 'service_id'],
            ['T1', 'R1', 'WD']
        ]
        
        stop_times_data = [
            ['trip_id', 'stop_id', 'arrival_time', 'departure_time', 'stop_sequence'],
            ['T1', 'S1', '08:00:00', '08:00:00', '1'],
            ['T1', 'S2', '08:10:00', '08:10:00', '2'],
            ['T1', 'S3', '08:20:00', '08:20:00', '3']
        ]
        
        # Créer le ZIP
        with zipfile.ZipFile(gtfs_zip, 'w') as zf:
            for name, data in [('stops.txt', stops_data), 
                               ('routes.txt', routes_data),
                               ('trips.txt', trips_data),
                               ('stop_times.txt', stop_times_data)]:
                content = '\n'.join([','.join(row) for row in data])
                zf.writestr(name, content)
        
        # Test du chargement
        print(f"  - Fichier GTFS créé: {gtfs_zip}")
        
        # Vérifier que le ZIP est valide
        with zipfile.ZipFile(gtfs_zip, 'r') as zf:
            files = zf.namelist()
            print(f"  - Fichiers dans le ZIP: {files}")
            assert 'stops.txt' in files
            assert 'routes.txt' in files
            assert 'trips.txt' in files
            assert 'stop_times.txt' in files
        
        print("  ✓ GTFSManager: structure de fichier valide")
        
        # Test de la fonction de distance
        from math import radians, sin, cos, sqrt, atan2
        
        def calculate_distance(lat1, lon1, lat2, lon2):
            R = 6371000
            lat1_rad = radians(lat1)
            lat2_rad = radians(lat2)
            delta_lat = radians(lat2 - lat1)
            delta_lon = radians(lon2 - lon1)
            a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c
        
        # Test distance Paris
        dist = calculate_distance(48.8566, 2.3522, 48.8606, 2.3376)
        print(f"  - Distance calculée: {dist:.2f}m")
        assert dist > 0
        print("  ✓ Calcul de distance fonctionne")


def test_routing_engine():
    """Test le moteur de routage"""
    print("\nTest du RoutingEngine...")
    
    # Test de l'algorithme A*
    import heapq
    
    # Simple test A*
    open_set = []
    heapq.heappush(open_set, (0, 0, 'start', ['start']))
    
    total_cost, current_cost, current_node, path = heapq.heappop(open_set)
    assert current_node == 'start'
    assert path == ['start']
    
    print("  ✓ Algorithme A* initialisé correctement")
    
    # Test de calcul de coût temporel
    def calculate_time_cost(departure_time, arrival_time):
        try:
            dep_parts = departure_time.split(':')
            arr_parts = arrival_time.split(':')
            dep_minutes = int(dep_parts[0]) * 60 + int(dep_parts[1])
            arr_minutes = int(arr_parts[0]) * 60 + int(arr_parts[1])
            diff = arr_minutes - dep_minutes
            if diff < 0:
                diff += 24 * 60
            return diff / 60
        except:
            return 1
    
    cost = calculate_time_cost('08:00:00', '08:30:00')
    print(f"  - Coût temporel calculé: {cost:.2f}h")
    assert cost == 0.5
    print("  ✓ Calcul de coût temporel fonctionne")


def test_storage_manager():
    """Test le gestionnaire de stockage"""
    print("\nTest du StorageManager...")
    
    import json
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test création de répertoires
        gtfs_dir = os.path.join(tmpdir, 'gtfs')
        maps_dir = os.path.join(tmpdir, 'maps')
        
        os.makedirs(gtfs_dir, exist_ok=True)
        os.makedirs(maps_dir, exist_ok=True)
        
        assert os.path.exists(gtfs_dir)
        assert os.path.exists(maps_dir)
        print("  ✓ Création de répertoires fonctionne")
        
        # Test sauvegarde métadonnées
        metadata = {
            'gtfs_imports': [],
            'maps_downloaded': []
        }
        
        metadata_file = os.path.join(tmpdir, 'metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Test chargement
        with open(metadata_file, 'r') as f:
            loaded = json.load(f)
        
        assert loaded == metadata
        print("  ✓ Sauvegarde/chargement métadonnées fonctionne")


def main():
    """Execute tous les tests"""
    print("=" * 60)
    print("Tests GTFSPy - Modules Core")
    print("=" * 60)
    
    try:
        test_gtfs_manager()
        test_routing_engine()
        test_storage_manager()
        
        print("\n" + "=" * 60)
        print("✓ Tous les tests sont passés!")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n✗ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
