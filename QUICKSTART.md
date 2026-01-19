# Guide de Démarrage Rapide - GTFSPy

## En bref

GTFSPy est votre application mobile de routage de transport en commun. Elle utilise les données GTFS pour calculer l'itinéraire optimal entre deux points.

## Installation rapide

### Sur Desktop (pour tester)

```bash
# 1. Cloner le projet
git clone https://github.com/hleong75/GTFSPy.git
cd GTFSPy

# 2. Installer les dépendances
pip install -r requirements.txt
pip install kivy[base] kivymd
garden install mapview

# 3. Créer des données de test
python create_sample_data.py

# 4. Lancer l'application
python main.py
```

### Sur Android (pour production)

```bash
# Prérequis: Linux ou WSL2 avec Java 11
sudo apt install -y git zip unzip openjdk-11-jdk

# 1. Installer Buildozer
pip install buildozer cython==0.29.33

# 2. Compiler l'APK
buildozer android debug

# L'APK sera dans: bin/gtfspy-1.0.0-arm64-v8a-debug.apk
```

## Utilisation

### Étape 1: Importer des données GTFS

1. Télécharger un fichier GTFS depuis:
   - France: https://transport.data.gouv.fr/
   - International: https://transitfeeds.com/

2. Dans l'app, cliquer sur **"Importer GTFS"**

3. Sélectionner le fichier ZIP

### Étape 2: Calculer un itinéraire

1. Entrer les coordonnées de départ:
   ```
   48.8584, 2.3470
   ```

2. Entrer les coordonnées d'arrivée:
   ```
   48.8484, 2.3960
   ```

3. Cliquer sur **"Calculer itinéraire"**

### Étape 3: Voir le résultat

L'itinéraire s'affiche sur la carte avec:
- 🟢 Marqueur de départ
- 🔴 Marqueur d'arrivée
- 📍 Tous les arrêts intermédiaires

## Obtenir des coordonnées

### Méthode 1: Google Maps
1. Ouvrir Google Maps
2. Clic droit sur un point
3. Les coordonnées s'affichent (ex: 48.8584, 2.3470)

### Méthode 2: OpenStreetMap
1. Ouvrir https://www.openstreetmap.org/
2. Clic droit → "Afficher l'adresse"
3. Coordonnées affichées en haut

### Méthode 3: GPS de votre téléphone
- Activer la localisation
- Utiliser une app GPS pour obtenir vos coordonnées

## Exemples de coordonnées

### Paris
- Châtelet: `48.8584, 2.3470`
- Gare du Nord: `48.8809, 2.3553`
- République: `48.8676, 2.3633`
- Bastille: `48.8532, 2.3692`
- Nation: `48.8484, 2.3960`

### Lyon
- Part-Dieu: `45.7604, 4.8590`
- Bellecour: `45.7578, 4.8320`

### Marseille
- Vieux-Port: `43.2951, 5.3749`
- Saint-Charles: `43.3026, 5.3806`

## Données GTFS de test

Le projet inclut un générateur de données de test:

```bash
python create_sample_data.py
```

Cela crée `sample_gtfs.zip` avec:
- 8 arrêts à Paris
- 3 lignes de métro
- 4 trajets
- Horaires réalistes

## Fonctionnalités

### ✅ Import GTFS
Importer des fichiers ZIP contenant les données de transport

### ✅ Routage intelligent
Algorithme A* pour trouver le chemin optimal

### ✅ Carte interactive
Visualiser votre itinéraire sur une carte

### ✅ Téléchargement carte
Sauvegarder des cartes pour utilisation hors ligne

### ✅ Stockage persistant
Garder vos GTFS et cartes téléchargées

## Structure du projet

```
GTFSPy/
├── main.py                    # 🎯 Application principale
├── gtfs_manager.py            # 📊 Gestion des données GTFS
├── routing_engine.py          # 🚀 Calcul d'itinéraire (A*)
├── storage_manager.py         # 💾 Stockage persistant
├── buildozer.spec             # 📱 Configuration Android
├── requirements.txt           # 📦 Dépendances
├── test_core.py               # ✅ Tests
├── create_sample_data.py      # 🎲 Générateur de données
├── README.md                  # 📖 Documentation
├── INSTALLATION.md            # 🔧 Guide installation
├── ARCHITECTURE.md            # 🏗️ Documentation technique
└── SUMMARY.md                 # 📋 Résumé du projet
```

## Dépannage rapide

### Problème: "Module kivy not found"
```bash
pip install kivy[base] kivymd
```

### Problème: "MapView not found"
```bash
garden install mapview
```

### Problème: "Aucun itinéraire trouvé"
- Vérifier que le fichier GTFS est importé
- Vérifier que les coordonnées sont correctes (format: lat, lon)
- Vérifier que les points sont proches d'arrêts GTFS

### Problème: Buildozer échoue
```bash
# Nettoyer et recommencer
buildozer android clean
buildozer android debug
```

## Performance

L'application est optimisée avec:
- Index O(1) pour recherche de trajets
- Cache des données GTFS
- Algorithme A* efficace

**Temps de calcul typiques:**
- Petit réseau (< 100 arrêts): < 1 seconde
- Réseau moyen (100-1000 arrêts): 1-3 secondes
- Grand réseau (> 1000 arrêts): 3-10 secondes

## Support

### Documentation complète
- **README.md**: Vue d'ensemble
- **INSTALLATION.md**: Installation détaillée
- **ARCHITECTURE.md**: Détails techniques
- **SUMMARY.md**: Résumé complet

### Code source
GitHub: https://github.com/hleong75/GTFSPy

### Issues
Pour signaler un bug ou demander une fonctionnalité:
https://github.com/hleong75/GTFSPy/issues

## Ressources GTFS

### France
- **Transport.data.gouv.fr**: Toutes les régions françaises
- **IDFM**: Île-de-France
- **TCL**: Lyon
- **RTM**: Marseille

### International
- **TransitFeeds.com**: Base mondiale
- **OpenMobilityData.org**: Données ouvertes
- **GTFS.org**: Spécification officielle

## Licence

MIT License - Libre d'utilisation et modification

## Développé avec

- 🐍 Python 3.8+
- 📱 Kivy 2.2.1
- 🎨 KivyMD 1.1.1
- 🗺️ MapView 1.0.6
- 🔨 Buildozer

---

**Bon routage! 🚇🚌🚊**
