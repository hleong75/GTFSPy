# Architecture Technique - GTFSPy

## Vue d'ensemble

GTFSPy est une application mobile de routage de transport en commun utilisant les données GTFS (General Transit Feed Specification). L'application est développée en Python avec le framework Kivy et peut être compilée en APK pour Android via Buildozer.

## Architecture des composants

```
┌─────────────────────────────────────────────────────┐
│                   Interface UI (Kivy)                │
│  ┌───────────────┐  ┌──────────────┐  ┌───────────┐│
│  │  MainScreen   │  │   MapView    │  │  Popups   ││
│  └───────┬───────┘  └──────┬───────┘  └─────┬─────┘│
└──────────┼──────────────────┼────────────────┼──────┘
           │                  │                │
           ▼                  ▼                ▼
┌─────────────────────────────────────────────────────┐
│              Couche Application (GTFSPyApp)          │
│  ┌──────────────────────────────────────────────┐   │
│  │  Gestionnaires principaux                    │   │
│  │  - GTFSManager                               │   │
│  │  - RoutingEngine                             │   │
│  │  - StorageManager                            │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
           │                  │                │
           ▼                  ▼                ▼
┌─────────────────────────────────────────────────────┐
│                  Couche Données                      │
│  ┌──────────┐  ┌──────────┐  ┌─────────────────┐   │
│  │   GTFS   │  │  Routes  │  │  Métadonnées    │   │
│  │   ZIP    │  │  Cache   │  │  (JSON)         │   │
│  └──────────┘  └──────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Modules principaux

### 1. main.py - Application principale

**Responsabilités:**
- Initialisation de l'application Kivy
- Gestion de l'interface utilisateur
- Coordination entre les différents gestionnaires
- Gestion des événements utilisateur

**Classes principales:**
- `GTFSPyApp`: Application Kivy principale
- `MainScreen`: Écran principal avec carte et contrôles

**Fonctionnalités UI:**
- Affichage de carte interactive
- Champs de saisie pour origine/destination
- Boutons d'action (calculer, importer, télécharger)
- Popups pour les messages et sélection de fichiers

### 2. gtfs_manager.py - Gestionnaire GTFS

**Responsabilités:**
- Import et extraction de fichiers GTFS ZIP
- Parsing des fichiers CSV GTFS
- Stockage en mémoire des données GTFS
- Recherche d'arrêts proches

**Structures de données:**
```python
{
    'stops': {
        'S1': {
            'stop_id': 'S1',
            'stop_name': 'Châtelet',
            'stop_lat': '48.8584',
            'stop_lon': '2.3470'
        }
    },
    'routes': { ... },
    'trips': { ... },
    'stop_times': {
        'T1': [
            {
                'trip_id': 'T1',
                'stop_id': 'S1',
                'arrival_time': '08:00:00',
                'departure_time': '08:00:00',
                'stop_sequence': '1'
            }
        ]
    }
}
```

**Algorithmes:**
- Calcul de distance (formule de Haversine)
- Recherche de l'arrêt le plus proche

### 3. routing_engine.py - Moteur de routage

**Responsabilités:**
- Calcul d'itinéraires optimaux
- Implémentation de l'algorithme A*
- Gestion des transferts et correspondances
- Formatage des résultats

**Algorithme A* - Détails:**

1. **Initialisation:**
   - File de priorité avec (coût_total, coût_actuel, arrêt, chemin)
   - Ensemble des arrêts visités

2. **Heuristique:**
   - Distance géographique divisée par vitesse moyenne (30 km/h)
   - Permet d'estimer le temps restant

3. **Fonction de coût:**
   - Temps de trajet entre arrêts
   - Basé sur les horaires GTFS

4. **Recherche de voisins:**
   - Parcours des trajets passant par l'arrêt actuel
   - Identification des arrêts suivants sur chaque trajet

**Complexité:**
- Temps: O((V + E) log V) où V = arrêts, E = connexions
- Espace: O(V)

### 4. storage_manager.py - Gestionnaire de stockage

**Responsabilités:**
- Gestion du stockage persistant
- Sauvegarde des métadonnées
- Organisation des fichiers
- Gestion de l'espace disque

**Structure de stockage:**
```
~/.gtfspy/  (ou ANDROID_STORAGE/GTFSPy/ sur Android)
├── gtfs/
│   ├── sample_gtfs/
│   │   ├── stops.txt
│   │   ├── routes.txt
│   │   └── ...
│   └── autre_gtfs/
├── maps/
│   ├── map_48.85_2.35_11/
│   │   └── info.json
│   └── autre_carte/
└── metadata.json
```

**Format metadata.json:**
```json
{
  "gtfs_imports": [
    {
      "filename": "sample_gtfs.zip",
      "extract_dir": "/path/to/gtfs/sample_gtfs",
      "import_date": "2024-01-15T10:30:00",
      "status": "active"
    }
  ],
  "maps_downloaded": [
    {
      "center_lat": 48.8566,
      "center_lon": 2.3522,
      "zoom": 11,
      "download_date": "2024-01-15T11:00:00",
      "status": "downloaded"
    }
  ]
}
```

## Flux de données

### 1. Import GTFS

```
Utilisateur sélectionne ZIP
        ↓
GTFSManager.import_gtfs()
        ↓
Extraction ZIP → répertoire temporaire
        ↓
Chargement CSV → structures Python
        ↓
StorageManager.save_gtfs_metadata()
        ↓
Sauvegarde metadata.json
```

### 2. Calcul d'itinéraire

```
Utilisateur entre coordonnées A et B
        ↓
MainScreen.calculate_route()
        ↓
RoutingEngine.find_route(origin, destination)
        ↓
GTFSManager.find_nearest_stop() × 2
        ↓
RoutingEngine.a_star_search()
        ↓
Format des résultats
        ↓
MainScreen.display_route()
        ↓
Affichage sur MapView
```

## Optimisations

### Performances

1. **Cache des arrêts proches:**
   - Implémenter un cache spatial (R-tree ou quad-tree)
   - Réduire les recherches de O(n) à O(log n)

2. **Index des stop_times:**
   - Index par stop_id pour recherche rapide
   - Index par trip_id déjà implémenté

3. **Préchargement:**
   - Charger les données GTFS au démarrage
   - Garder en mémoire pour éviter rechargements

### Mémoire

1. **Lazy loading:**
   - Charger uniquement les trajets nécessaires
   - Libérer les données anciennes

2. **Compression:**
   - Garder les fichiers ZIP compressés
   - Extraire à la demande

## Dépendances

### Core
- **Python 3.8+**: Langage de base
- **Kivy 2.2.1**: Framework UI
- **KivyMD 1.1.1**: Material Design pour Kivy

### Carte
- **kivy-garden.mapview 1.0.6**: Affichage de cartes

### Utilitaires
- **requests 2.31.0**: Téléchargements HTTP
- **Pillow 10.1.0**: Traitement d'images

### Build
- **Buildozer**: Compilation Android
- **python-for-android**: Backend Android
- **Cython**: Compilation Python → C

## Configuration Android

### Permissions (AndroidManifest.xml)
```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
```

### Configuration Buildozer
- **API Target**: 31 (Android 12)
- **API Minimum**: 21 (Android 5.0)
- **Architectures**: arm64-v8a, armeabi-v7a
- **Bootstrap**: SDL2

## Tests

### test_core.py
Tests unitaires pour les modules sans dépendances Kivy:
- Test du GTFSManager
- Test du RoutingEngine
- Test du StorageManager

### Tests à ajouter
- Tests d'intégration UI
- Tests de performance
- Tests sur Android réel

## Extensions futures

### Fonctionnalités
- ✅ Import GTFS ZIP
- ✅ Routage A*
- ✅ Carte interactive
- ⬜ Recherche par adresse (géocodage)
- ⬜ Mode hors ligne complet
- ⬜ Favoris et historique
- ⬜ Notifications de départ
- ⬜ Partage d'itinéraire
- ⬜ Support multimodal (vélo, marche)
- ⬜ Accessibilité PMR

### Technique
- ⬜ Base de données SQLite
- ⬜ Index spatial
- ⬜ Cache intelligent
- ⬜ Synchronisation cloud
- ⬜ Support iOS

## Références

- [GTFS Reference](https://gtfs.org/reference/static)
- [Kivy Documentation](https://kivy.org/doc/stable/)
- [A* Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Haversine Formula](https://en.wikipedia.org/wiki/Haversine_formula)
- [Buildozer](https://buildozer.readthedocs.io/)
