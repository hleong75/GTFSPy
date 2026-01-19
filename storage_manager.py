"""
Gestionnaire de stockage - Gère la persistance des données GTFS et des cartes
"""

import os
import json
from datetime import datetime


class StorageManager:
    """Gère le stockage persistant des données GTFS et des cartes"""
    
    def __init__(self):
        # Déterminer le répertoire de stockage
        if os.environ.get('ANDROID_STORAGE'):
            # Sur Android
            self.base_dir = os.path.join(
                os.environ.get('ANDROID_STORAGE'),
                'GTFSPy'
            )
        else:
            # Sur desktop
            self.base_dir = os.path.join(
                os.path.expanduser('~'),
                '.gtfspy'
            )
        
        self.gtfs_dir = os.path.join(self.base_dir, 'gtfs')
        self.maps_dir = os.path.join(self.base_dir, 'maps')
        self.metadata_file = os.path.join(self.base_dir, 'metadata.json')
        
        # Créer les répertoires si nécessaire
        self.ensure_directories()
        
        # Charger les métadonnées
        self.metadata = self.load_metadata()
    
    def ensure_directories(self):
        """Crée les répertoires de stockage s'ils n'existent pas"""
        os.makedirs(self.gtfs_dir, exist_ok=True)
        os.makedirs(self.maps_dir, exist_ok=True)
    
    def get_gtfs_dir(self):
        """Retourne le répertoire de stockage GTFS"""
        return self.gtfs_dir
    
    def get_maps_dir(self):
        """Retourne le répertoire de stockage des cartes"""
        return self.maps_dir
    
    def load_metadata(self):
        """Charge les métadonnées depuis le fichier JSON"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement des métadonnées: {e}")
        
        return {
            'gtfs_imports': [],
            'maps_downloaded': []
        }
    
    def save_metadata(self):
        """Sauvegarde les métadonnées dans le fichier JSON"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des métadonnées: {e}")
            return False
    
    def save_gtfs_metadata(self, filename, extract_dir, import_date):
        """Enregistre les métadonnées d'un import GTFS"""
        gtfs_info = {
            'filename': filename,
            'extract_dir': extract_dir,
            'import_date': import_date.isoformat(),
            'status': 'active'
        }
        
        self.metadata['gtfs_imports'].append(gtfs_info)
        return self.save_metadata()
    
    def get_gtfs_imports(self):
        """Retourne la liste des imports GTFS"""
        return self.metadata.get('gtfs_imports', [])
    
    def download_map_data(self, lat, lon, zoom):
        """
        Télécharge les données de carte pour une zone donnée
        
        Note: Cette fonction est un placeholder. L'implémentation complète
        nécessiterait l'intégration avec un service de tuiles de carte
        (comme OpenStreetMap, Mapbox, etc.)
        """
        try:
            map_info = {
                'center_lat': lat,
                'center_lon': lon,
                'zoom': zoom,
                'download_date': datetime.now().isoformat(),
                'status': 'downloaded'
            }
            
            # Créer un répertoire pour cette zone
            map_id = f"map_{lat}_{lon}_{zoom}"
            map_dir = os.path.join(self.maps_dir, map_id)
            os.makedirs(map_dir, exist_ok=True)
            
            # Sauvegarder les informations de la carte
            map_info_file = os.path.join(map_dir, 'info.json')
            with open(map_info_file, 'w') as f:
                json.dump(map_info, f, indent=2)
            
            # Ajouter aux métadonnées
            self.metadata['maps_downloaded'].append(map_info)
            self.save_metadata()
            
            return True
        except Exception as e:
            print(f"Erreur lors du téléchargement de la carte: {e}")
            return False
    
    def get_downloaded_maps(self):
        """Retourne la liste des cartes téléchargées"""
        return self.metadata.get('maps_downloaded', [])
    
    def clear_old_data(self, days=30):
        """Supprime les données anciennes pour libérer de l'espace"""
        # Cette fonction pourrait être implémentée pour nettoyer
        # les imports GTFS et cartes trop anciens
        pass
