# Guide d'Installation et d'Utilisation - GTFSPy

## Table des matières

1. [Installation pour développement](#installation-pour-développement)
2. [Compilation pour Android](#compilation-pour-android)
3. [Utilisation de l'application](#utilisation-de-lapplication)
4. [Format des données GTFS](#format-des-données-gtfs)
5. [Dépannage](#dépannage)

## Installation pour développement

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

### Étapes d'installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/hleong75/GTFSPy.git
   cd GTFSPy
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Linux/Mac
   # ou
   venv\Scripts\activate  # Sur Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Installer Kivy Garden pour MapView**
   ```bash
   garden install mapview
   ```

5. **Tester l'installation**
   ```bash
   python test_core.py
   ```

## Compilation pour Android

### Prérequis pour Android

- Linux (Ubuntu 20.04+ recommandé) ou WSL2 sur Windows
- Au moins 4 GB de RAM
- Au moins 10 GB d'espace disque libre
- Java JDK 11
- Android SDK et NDK (seront installés automatiquement par Buildozer)

### Installation de Buildozer

1. **Installer les dépendances système (Ubuntu/Debian)**
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   ```

2. **Installer Buildozer**
   ```bash
   pip install buildozer
   pip install cython==0.29.33
   ```

3. **Installer python-for-android**
   ```bash
   pip install python-for-android
   ```

### Compiler l'APK

1. **Initialiser Buildozer (première fois uniquement)**
   ```bash
   buildozer init
   ```
   Note: Un fichier `buildozer.spec` est déjà fourni, cette étape n'est nécessaire que si vous voulez repartir de zéro.

2. **Compiler en mode debug**
   ```bash
   buildozer android debug
   ```
   
   Cette commande va:
   - Télécharger Android SDK et NDK
   - Compiler Python pour Android
   - Compiler toutes les dépendances
   - Créer l'APK dans `bin/`
   
   ⚠️ La première compilation peut prendre 30-60 minutes.

3. **Compiler et installer sur un appareil**
   ```bash
   # Activer le débogage USB sur votre appareil Android
   # Connecter l'appareil via USB
   buildozer android debug deploy run
   ```

4. **Créer un APK release (pour distribution)**
   ```bash
   buildozer android release
   ```

### Localiser l'APK compilé

L'APK sera dans le dossier `bin/`:
```
bin/gtfspy-1.0.0-arm64-v8a-debug.apk
```

## Utilisation de l'application

### Sur Desktop (développement)

1. **Lancer l'application**
   ```bash
   python main.py
   ```

2. **Créer des données GTFS de test**
   ```bash
   python create_sample_data.py
   ```
   Cela crée un fichier `sample_gtfs.zip` avec des données d'exemple.

### Sur Android

1. **Installer l'APK**
   - Transférer l'APK sur votre appareil
   - Activer l'installation depuis des sources inconnues
   - Installer l'APK

2. **Accorder les permissions**
   - Localisation (pour trouver votre position)
   - Stockage (pour importer des fichiers GTFS)

### Utilisation de base

1. **Importer un fichier GTFS**
   - Cliquer sur "Importer GTFS"
   - Sélectionner un fichier ZIP GTFS
   - Attendre la fin de l'importation

2. **Calculer un itinéraire**
   - Entrer les coordonnées de départ (format: lat, lon)
     Exemple: `48.8584, 2.3470`
   - Entrer les coordonnées d'arrivée
     Exemple: `48.8484, 2.3960`
   - Cliquer sur "Calculer itinéraire"
   - L'itinéraire s'affiche sur la carte

3. **Télécharger une carte**
   - Naviguer vers la zone souhaitée sur la carte
   - Cliquer sur "Télécharger carte"
   - La carte est sauvegardée pour utilisation hors ligne

## Format des données GTFS

### Fichiers requis

L'application nécessite au minimum ces fichiers dans le ZIP GTFS:

1. **stops.txt** - Liste des arrêts
   ```
   stop_id,stop_name,stop_lat,stop_lon
   S1,Châtelet,48.8584,2.3470
   ```

2. **routes.txt** - Liste des lignes
   ```
   route_id,route_short_name,route_long_name,route_type
   R1,1,Ligne 1,1
   ```

3. **trips.txt** - Liste des trajets
   ```
   trip_id,route_id,service_id
   T1,R1,WD
   ```

4. **stop_times.txt** - Horaires aux arrêts
   ```
   trip_id,stop_id,arrival_time,departure_time,stop_sequence
   T1,S1,08:00:00,08:00:00,1
   ```

### Fichiers optionnels

- **calendar.txt** - Calendrier de service
- **shapes.txt** - Formes géographiques des trajets
- **agency.txt** - Informations sur les agences

### Où trouver des données GTFS

- **France**: https://transport.data.gouv.fr/
- **International**: https://transitfeeds.com/
- **OpenMobilityData**: https://transitfeeds.com/

## Dépannage

### Problème: Module Kivy non trouvé

**Solution**:
```bash
pip install kivy[base]
pip install kivymd
```

### Problème: Buildozer échoue lors de la compilation

**Solutions**:
1. Vérifier que vous avez assez d'espace disque (10+ GB)
2. Vérifier que vous avez assez de RAM (4+ GB)
3. Nettoyer et recommencer:
   ```bash
   buildozer android clean
   buildozer android debug
   ```

### Problème: L'application crash au démarrage sur Android

**Solutions**:
1. Vérifier les logs:
   ```bash
   buildozer android logcat
   ```
2. Vérifier que toutes les permissions sont accordées
3. Recompiler en mode release

### Problème: Impossible d'importer un fichier GTFS

**Solutions**:
1. Vérifier que le fichier est bien un ZIP
2. Vérifier que le ZIP contient au minimum:
   - stops.txt
   - routes.txt
   - trips.txt
   - stop_times.txt
3. Vérifier les permissions de stockage sur Android

### Problème: Aucun itinéraire trouvé

**Solutions**:
1. Vérifier que les coordonnées sont correctes
2. Vérifier qu'un fichier GTFS est importé
3. Vérifier que les coordonnées sont proches d'arrêts GTFS
4. Réduire la distance entre départ et arrivée

## Support

Pour signaler des bugs ou demander de l'aide:
1. Créer une issue sur GitHub
2. Inclure les informations:
   - Version de Python
   - Système d'exploitation
   - Logs d'erreur
   - Étapes pour reproduire le problème

## Ressources supplémentaires

- [Documentation GTFS](https://gtfs.org/)
- [Documentation Kivy](https://kivy.org/doc/stable/)
- [Documentation Buildozer](https://buildozer.readthedocs.io/)
- [Documentation KivyMD](https://kivymd.readthedocs.io/)
