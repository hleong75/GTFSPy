# GTFSPy

Application mobile de routage de transport en commun basée sur les données GTFS (General Transit Feed Specification).

## Fonctionnalités

- **Calcul d'itinéraire optimal** : Trouve le meilleur chemin entre deux points en utilisant les données GTFS
- **Import de fichiers GTFS** : Importe et traite les fichiers GTFS au format ZIP
- **Carte interactive** : Affiche l'itinéraire sur une carte interactive
- **Téléchargement de cartes** : Permet de télécharger des données de carte pour une utilisation hors ligne
- **Stockage persistant** : Conserve les données GTFS importées et les cartes téléchargées
- **Interface intuitive** : Interface utilisateur simple et efficace pour Android

## Fonctionnalités inspirées de Transito

Cette application intègre les fonctionnalités suivantes inspirées de Transito:
- Routage de transport en commun
- Affichage des horaires et arrêts
- Support des formats GTFS standard
- Carte interactive avec marqueurs
- Gestion des données hors ligne

## Installation

### Prérequis

- Python 3.8 ou supérieur
- Buildozer (pour la compilation Android)

### Installation pour développement

```bash
pip install -r requirements.txt
```

### Compilation pour Android

**Notes importantes** : 
- Des corrections ont été appliquées pour résoudre l'erreur libffi (AC_PROG_LIBTOOL). Voir [LOG_FIXES.md](LOG_FIXES.md) pour les détails.
- L'erreur `aidl` manquante avec build-tools 36.x a été corrigée en spécifiant la version 35.0.1 dans buildozer.spec. Voir [BUILD_NOTE.md](BUILD_NOTE.md) pour plus de détails.

Sur Ubuntu/Debian, installez d'abord les dépendances système :

```bash
sudo apt-get update
sudo apt-get install -y git zip unzip openjdk-17-jdk \
    libtool libtool-bin automake autoconf \
    zlib1g-dev libffi-dev libssl-dev cmake
```

Puis compilez l'application :

```bash
buildozer android debug
```

Pour compiler et déployer directement sur un appareil:

```bash
buildozer android debug deploy run
```

## Utilisation

### Sur Desktop (pour le développement)

```bash
python main.py
```

### Sur Android

1. Installer l'APK généré par Buildozer
2. Accorder les permissions nécessaires (localisation, stockage)
3. Importer un fichier GTFS (format ZIP)
4. Entrer les coordonnées de départ et d'arrivée
5. Calculer l'itinéraire

## Format GTFS

L'application supporte les fichiers GTFS standard contenant au minimum:
- `stops.txt` - Liste des arrêts
- `routes.txt` - Liste des lignes
- `trips.txt` - Liste des trajets
- `stop_times.txt` - Horaires aux arrêts

Fichiers optionnels supportés:
- `calendar.txt` - Calendrier de service
- `shapes.txt` - Formes géographiques des trajets

## Structure du projet

```
GTFSPy/
├── main.py              # Application principale
├── gtfs_manager.py      # Gestion des fichiers GTFS
├── routing_engine.py    # Moteur de routage
├── storage_manager.py   # Gestion du stockage persistant
├── buildozer.spec       # Configuration Buildozer
├── requirements.txt     # Dépendances Python
└── README.md           # Ce fichier
```

## Algorithme de routage

L'application utilise l'algorithme A* pour trouver le chemin optimal entre deux points:
1. Trouve les arrêts les plus proches des points de départ et d'arrivée
2. Utilise A* avec une heuristique basée sur la distance géographique
3. Prend en compte les temps de trajet et les correspondances
4. Retourne l'itinéraire complet avec tous les arrêts intermédiaires

## Stockage des données

Les données sont stockées dans:
- Desktop: `~/.gtfspy/`
- Android: Stockage interne de l'application

Structure de stockage:
```
.gtfspy/
├── gtfs/           # Fichiers GTFS extraits
├── maps/           # Données de cartes téléchargées
└── metadata.json   # Métadonnées des imports et téléchargements
```

## Permissions Android

L'application requiert les permissions suivantes:
- `INTERNET` - Pour télécharger les cartes
- `ACCESS_FINE_LOCATION` - Pour la localisation précise
- `ACCESS_COARSE_LOCATION` - Pour la localisation approximative
- `WRITE_EXTERNAL_STORAGE` - Pour sauvegarder les données
- `READ_EXTERNAL_STORAGE` - Pour lire les fichiers GTFS

## Contribution

Les contributions sont les bienvenues! N'hésitez pas à ouvrir des issues ou des pull requests.

## Licence

Ce projet est distribué sous licence MIT.

## Auteurs

Développé pour faciliter l'utilisation des transports en commun à travers le monde.