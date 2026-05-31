# HOUSE FADE BARBER SHOP - Application Android

Application mobile Android pour la gestion d'un salon de coiffure avec système de cartes NFC.

*Build automatique via GitHub Actions*

## Fonctionnalités

- **Gestion des clients** : Création, modification et recherche de clients
- **Gestion des cartes NFC** : Activation, recharge et débit de cartes
- **Système de points** : 
  - 5 points = 22 500 FCFA (validité 6 mois)
  - 10 points = 40 000 FCFA (validité 1 an)
- **Expiration des points** : Les points expirent automatiquement après la durée de validité
- **Rapports** : Statistiques et rapports de transactions
- **Contrôle d'accès** : Rôles (Administrateur, Caissier, Coiffeur)

## Prérequis

### Pour le développement
- Python 3.8 ou supérieur
- Kivy 2.0.0
- Buildozer (pour la compilation Android)

### Pour l'installation sur Android
- Android 5.0 (API 21) ou supérieur
- Support NFC

## Installation

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Installation de Buildozer (pour la compilation)

```bash
pip install buildozer
```

Sur Linux, vous aurez également besoin de :
```bash
sudo apt-get install build-essential git python3 python3-dev openjdk-8-jdk
sudo apt-get install libc6-dev-i386 lib32z1 lib32ncurses5 libstdc++6
sudo apt-get install zlib1g-dev libncurses5-dev libtinfo5 libbz2-1.0
```

## Compilation pour Android

### Initialisation de Buildozer

```bash
buildozer init
```

### Compilation de l'APK (mode debug)

```bash
buildozer android debug
```

### Compilation de l'APK (mode release)

```bash
buildozer android release
```

L'APK sera généré dans le dossier `bin/`.

## Utilisation

### Première Connexion

Au premier lancement, un compte administrateur par défaut est créé :
- **Login** : admin
- **Mot de passe** : admin123

**Important** : Changez ce mot de passe après la première connexion pour des raisons de sécurité.

### Écran de Connexion

1. Entrez votre login et mot de passe
2. Cliquez sur "Se connecter"

### Tableau de Bord

Le tableau de bord affiche :
- Nombre total de clients
- Nombre de cartes actives
- Nombre de cartes bloquées
- Nombre de cartes avec solde zéro
- Total des recharges du jour
- Total des débits du jour
- Chiffre d'affaires du jour
- Chiffre d'affaires du mois

### Actions disponibles

- **Activer une carte** : Activer une nouvelle carte NFC pour un client
- **Recharger une carte** : Ajouter des points à une carte existante
- **Débiter une coiffure** : Débiter 1 point pour une coiffure
- **Gérer les clients** : Gérer la base de données des clients
- **Rapports** : Voir les statistiques et rapports
- **Gérer les utilisateurs** : Gérer les comptes utilisateurs (administrateur uniquement)

## Structure du Projet

```
SALON COIFURE_ANDROID/
├── main.py              # Point d'entrée de l'application Kivy
├── config.py            # Configuration de l'application
├── models.py            # Modèles de données
├── database.py          # Gestion de la base de données SQLite
├── auth.py              # Authentification et autorisation
├── services.py          # Logique métier
├── requirements.txt     # Dépendances Python
├── buildozer.spec       # Configuration Buildozer pour Android
└── README.md           # Ce fichier
```

## Permissions Android

L'application nécessite les permissions suivantes :
- **INTERNET** : Pour les futures fonctionnalités en ligne
- **WRITE_EXTERNAL_STORAGE** : Pour stocker la base de données
- **READ_EXTERNAL_STORAGE** : Pour lire la base de données
- **NFC** : Pour lire les cartes NFC

## Compatibilité

- **Android** : 5.0 (API 21) et supérieur
- **Architectures** : arm64-v8a, armeabi-v7a

## Notes de Développement

### Test sur Desktop

Pour tester l'application sur desktop avant compilation :
```bash
python main.py
```

### NFC sur Android

Le support NFC est implémenté via l'API Android NFC. Assurez-vous que votre appareil dispose d'un lecteur NFC.

### Base de Données

La base de données SQLite est stockée dans le stockage externe de l'appareil Android.

## Support

Pour toute question ou problème, contactez l'équipe de développement.
