# Corrections des Erreurs du Log Buildozer

## Date
19 janvier 2026

## Problème Principal

Le log de compilation Buildozer montre une erreur critique lors de la compilation de la bibliothèque libffi pour Android :

```
configure.ac:41: error: possibly undefined macro: AC_PROG_LIBTOOL
configure:8578: error: possibly undefined macro: AC_PROG_LD
autoreconf: error: /usr/bin/autoconf failed with exit status: 1
```

Cette erreur se produit aux lignes 3981, 3984-3985, 4092, 4095-4096, 4217, 4220-4221 du fichier Log.

## Cause de l'Erreur

L'erreur est causée par :

1. **Absence de libtool** : La bibliothèque libffi utilise des macros autoconf (`AC_PROG_LIBTOOL` et `AC_PROG_LD`) qui sont fournies par le paquet `libtool`. Si libtool n'est pas installé dans l'environnement de build, autoconf ne peut pas trouver ces macros.

2. **Version de libffi** : Certaines versions anciennes de libffi ont des problèmes de compatibilité avec les versions récentes d'autoconf.

3. **Configuration python-for-android** : La recette libffi par défaut dans python-for-android peut ne pas gérer correctement l'installation préalable de libtool.

## Solutions Appliquées

### 1. Hook p4a personnalisé (`p4a_hook.py`)

Création d'un hook python-for-android qui :
- S'exécute avant le début du build
- Vérifie si libtool est installé
- Installe libtool si nécessaire
- Vérifie la version de libtool installée

**Fichier** : `p4a_hook.py`

**Fonctionnalités** :
```python
def prebuild_hook(ctx):
    - Vérifie la présence de libtool
    - Installe libtool et libtool-bin si absent
    - Affiche la version installée
    - Gère les erreurs gracieusement
```

### 2. Recette libffi personnalisée

Création d'une recette personnalisée pour libffi qui :
- Utilise une version stable de libffi (3.4.6)
- Installe automatiquement libtool avant la compilation
- Configure correctement les options de build pour Android

**Fichier** : `p4a_recipes/libffi/__init__.py`

**Avantages** :
- Version stable et testée de libffi
- Installation automatique des dépendances
- Gestion appropriée des erreurs
- Configuration optimisée pour Android

### 3. Mise à jour de buildozer.spec

Modifications apportées au fichier `buildozer.spec` :

```ini
# Ligne 174 - Activation du répertoire de recettes locales
p4a.local_recipes = p4a_recipes

# Ligne 177 - Activation du hook personnalisé
p4a.hook = p4a_hook.py

# Ligne 168 - Utilisation de la branche develop (plus récente)
p4a.branch = develop
```

## Installation Manuelle de libtool

Si les corrections automatiques ne fonctionnent pas, installez manuellement libtool avant de lancer buildozer :

### Sur Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y libtool libtool-bin automake autoconf
```

### Sur Fedora/RHEL
```bash
sudo dnf install -y libtool automake autoconf
```

### Sur macOS
```bash
brew install libtool automake autoconf
```

## Vérification

Pour vérifier que libtool est correctement installé :

```bash
which libtool
libtool --version
```

Sortie attendue :
```
/usr/bin/libtool
libtool (GNU libtool) 2.4.7
```

## Tests de Compilation

Après avoir appliqué ces corrections, testez la compilation :

```bash
# Nettoyer le cache buildozer
buildozer android clean

# Lancer la compilation avec logs détaillés
buildozer -v android debug
```

## Autres Erreurs Corrigées

### Warnings autoconf (non bloquants)

Le log montre également des warnings autoconf qui ne bloquent pas la compilation mais sont notés :

- `AC_CANONICAL_SYSTEM is obsolete` (lignes 3904-3907, etc.)
- `AC_TRY_COMPILE is obsolete` (lignes 3908-3910, etc.)
- `AC_HEADER_STDC is obsolete` (lignes 3917-3920, etc.)
- `AC_TRY_LINK is obsolete` (lignes 3930-3933, etc.)
- `AC_TRY_RUN is obsolete` (lignes 3970-3973, etc.)
- `AC_HELP_STRING is obsolete` (lignes 3957-3960, etc.)

Ces warnings proviennent du fichier configure.ac de libffi qui utilise des macros obsolètes. Ils ne bloquent pas la compilation et sont résolus en utilisant une version plus récente de libffi (3.4.6) dans notre recette personnalisée.

## Erreur Réseau (Non liée au code)

Le log montre aussi une erreur réseau à la fin :

```
OSError: [Errno socket error] [Errno -5] No address associated with hostname
```

Cette erreur n'est **PAS** liée au code ou à la configuration, mais à l'environnement de build qui n'a pas d'accès réseau. Cette erreur apparaît lors de la tentative de téléchargement d'Apache ANT depuis archive.apache.org.

**Solution** : Compiler sur une machine locale avec accès Internet ou utiliser un service de CI/CD avec accès réseau (GitHub Actions, etc.).

## Résumé des Corrections

| Problème | Solution | Fichier |
|----------|----------|---------|
| AC_PROG_LIBTOOL undefined | Hook d'installation de libtool | `p4a_hook.py` |
| Version libffi obsolète | Recette personnalisée avec libffi 3.4.6 | `p4a_recipes/libffi/__init__.py` |
| Configuration p4a | Activation des recettes locales et hook | `buildozer.spec` |
| Warnings autoconf | Version récente de libffi | `p4a_recipes/libffi/__init__.py` |
| Accès réseau | Documentation pour build local | Ce fichier |

## Résultats Attendus

Après application de ces corrections :

✅ Installation automatique de libtool avant la compilation de libffi  
✅ Utilisation d'une version stable et récente de libffi (3.4.6)  
✅ Disparition de l'erreur "AC_PROG_LIBTOOL undefined"  
✅ Build libffi réussi  
✅ Compilation complète de l'APK possible (avec accès réseau)  

## Prochaines Étapes

1. **Tester sur machine locale** avec accès Internet
2. **Vérifier** que libtool est installé (ou qu'il s'installe automatiquement)
3. **Lancer** `buildozer android debug`
4. **Vérifier** les logs pour confirmer que libffi se compile sans erreur
5. **Installer** l'APK sur un appareil Android de test

## Références

- [Python-for-Android Documentation](https://python-for-android.readthedocs.io/)
- [Buildozer Documentation](https://buildozer.readthedocs.io/)
- [libffi GitHub](https://github.com/libffi/libffi)
- [autoconf/libtool Issues](https://www.gnu.org/software/libtool/manual/html_node/Libtool-and-autoconf.html)

## Support

Si vous rencontrez toujours des problèmes après avoir appliqué ces corrections :

1. Vérifiez que libtool est installé : `which libtool`
2. Nettoyez le cache buildozer : `buildozer android clean`
3. Consultez les logs détaillés : `buildozer -v android debug`
4. Vérifiez votre connexion Internet pour le téléchargement des dépendances
5. Ouvrez une issue sur le repository avec les logs complets
