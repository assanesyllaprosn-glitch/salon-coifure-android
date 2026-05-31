# Instructions pour construire l'APK

## Problème
La construction d'un APK sur Windows est très complexe car Buildozer est conçu pour Linux/macOS.

## Solutions disponibles

### Option 1 : Utiliser GitHub Actions (Recommandée - Gratuit)

Cette méthode utilise les serveurs gratuits de GitHub pour construire l'APK.

**Étapes :**

1. **Créer un compte GitHub** (si vous n'en avez pas déjà un)
   - Allez sur https://github.com et créez un compte

2. **Créer un nouveau dépôt**
   - Cliquez sur "New repository"
   - Nommez-le "salon-coifure-android"
   - Cochez "Public" ou "Private" selon votre préférence
   - Cliquez sur "Create repository"

3. **Installer Git sur Windows** (si pas déjà installé)
   - Téléchargez depuis https://git-scm.com/download/win
   - Installez avec les options par défaut

4. **Pousser le code vers GitHub**
   - Ouvrez un terminal PowerShell dans le dossier du projet
   - Exécutez les commandes suivantes :
   ```bash
   cd "c:/Users/Assane SYLLA/Documents/LOCIGIEL 2026/SALON COIFURE_ANDROID"
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/VOTRE_NOM_UTILISATEUR/salon-coifure-android.git
   git push -u origin main
   ```

5. **Activer GitHub Actions**
   - Allez sur votre dépôt GitHub
   - Cliquez sur l'onglet "Actions"
   - Cliquez sur "Build Android APK"
   - Cliquez sur "Run workflow"
   - Cliquez sur le bouton vert "Run workflow"

6. **Télécharger l'APK**
   - Attendez que le build soit terminé (environ 10-15 minutes)
   - Une fois terminé, cliquez sur le workflow
   - Scrollez vers le bas et cliquez sur "salon-coifure-apk"
   - Téléchargez le fichier APK

7. **Copier l'APK dans le dossier apk**
   - Copiez le fichier APK téléchargé dans le dossier `apk/` du projet

### Option 2 : Utiliser un service de build en ligne

Il existe des services en ligne gratuits qui peuvent construire des APKs :

- **Replit** : https://replit.com (gratuit pour les petits projets)
- **GitLab CI** : Similaire à GitHub Actions
- **Codemagic** : https://codemagic.io (gratuit pour les projets open source)

### Option 3 : Utiliser une machine Linux

Si vous avez accès à une machine Linux (virtuelle ou physique) :

1. Copiez le dossier du projet sur la machine Linux
2. Installez les dépendances :
   ```bash
   sudo apt update
   sudo apt install -y build-essential git python3 python3-dev openjdk-8-jdk
   sudo apt install -y libc6-dev-i386 lib32z1 lib32ncurses5 libstdc++6
   sudo apt install -y zlib1g-dev libncurses5-dev libtinfo5 libbz2-1.0
   sudo apt install -y automake libtool pkg-config libffi-dev
   pip3 install buildozer cython
   ```
3. Compilez l'APK :
   ```bash
   cd /chemin/vers/SALON_COIFURE_ANDROID
   buildozer android debug
   ```
4. Copiez l'APK depuis le dossier `bin/` vers le dossier `apk/`

### Option 4 : Réessayer WSL (si vous changez d'avis)

Si vous décidez d'utiliser WSL après tout :

1. Redémarrez votre ordinateur (WSL a déjà été installé)
2. Ouvrez WSL Ubuntu
3. Suivez les instructions de l'Option 3 ci-dessus

## Recommandation

**L'Option 1 (GitHub Actions) est la plus simple** car :
- Pas besoin d'installer de logiciel complexe
- Utilise les serveurs gratuits de GitHub
- Fonctionne sur n'importe quel ordinateur avec un navigateur web
- Le processus est entièrement automatisé

Une fois l'APK construit, vous pourrez le copier directement dans le dossier `apk/` et l'installer sur votre appareil Android.
