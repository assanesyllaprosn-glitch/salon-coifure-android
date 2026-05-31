"""
Configuration file for HOUSE FADE BARBER SHOP Android
Contains all application settings and constants
"""

import os
from pathlib import Path

# Application Information
APP_NAME = "HOUSE FADE BARBER SHOP"
APP_VERSION = "1.0.0"

# Database Configuration
DB_NAME = "barber_shop.db"
# Android uses a different path for app data
if os.name == 'nt':
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_NAME)
    BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")
else:
    # For Android, use the app's data directory
    from kivy.utils import platform
    if platform == 'android':
        from android.storage import primary_external_storage_path
        DB_PATH = os.path.join(primary_external_storage_path(), DB_NAME)
        BACKUP_DIR = os.path.join(primary_external_storage_path(), "backups")
    else:
        DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_NAME)
        BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")

# Business Rules
NORMAL_HAIRCUT_PRICE = 5000  # FCFA per haircut
CARD_PRICE = 5000  # FCFA for card (can be free)
CARD_FREE = 0  # FCFA for free card

# Recharge pricing (tiered pricing)
RECHARGE_5_POINTS = 22500  # FCFA for 5 points (4,500 per point)
RECHARGE_10_POINTS = 40000  # FCFA for 10 points (4,000 per point)

MIN_RECHARGE_POINTS = 5
MAX_RECHARGE_POINTS = 10

# Point validity duration (in months)
VALIDITY_5_POINTS = 6  # 6 months for 5 points
VALIDITY_10_POINTS = 12  # 1 year for 10 points

# Card Status
CARD_STATUS_ACTIVE = "active"
CARD_STATUS_BLOCKED = "bloquée"
CARD_STATUS_LOST = "perdue"
CARD_STATUS_REPLACED = "remplacée"
CARD_STATUS_INACTIVE = "inactive"

CARD_STATUSES = [
    CARD_STATUS_ACTIVE,
    CARD_STATUS_BLOCKED,
    CARD_STATUS_LOST,
    CARD_STATUS_REPLACED,
    CARD_STATUS_INACTIVE
]

# Transaction Types
TRANSACTION_ACTIVATION = "activation"
TRANSACTION_RECHARGE = "recharge"
TRANSACTION_DEBIT = "debit"
TRANSACTION_CANCELLATION = "annulation"
TRANSACTION_BLOCK = "blocage"
TRANSACTION_REPLACEMENT = "remplacement"

TRANSACTION_TYPES = [
    TRANSACTION_ACTIVATION,
    TRANSACTION_RECHARGE,
    TRANSACTION_DEBIT,
    TRANSACTION_CANCELLATION,
    TRANSACTION_BLOCK,
    TRANSACTION_REPLACEMENT
]

# Payment Methods
PAYMENT_CASH = "espèces"
PAYMENT_WAVE = "Wave"
PAYMENT_ORANGE_MONEY = "Orange Money"
PAYMENT_CARD = "carte bancaire"
PAYMENT_OTHER = "autre"

PAYMENT_METHODS = [
    PAYMENT_CASH,
    PAYMENT_WAVE,
    PAYMENT_ORANGE_MONEY,
    PAYMENT_CARD,
    PAYMENT_OTHER
]

# User Roles
ROLE_ADMIN = "administrateur"
ROLE_CASHIER = "caissier"
ROLE_BARBER = "coiffeur"

USER_ROLES = [
    ROLE_ADMIN,
    ROLE_CASHIER,
    ROLE_BARBER
]

# Currency
CURRENCY = "FCFA"
CURRENCY_SYMBOL = "FCFA"

# NFC Configuration
NFC_READER_TIMEOUT = 30  # seconds
NFC_RETRY_ATTEMPTS = 3
NFC_RETRY_DELAY = 1  # second

# UI Configuration (not used in Kivy, kept for compatibility)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Colors (for Kivy UI)
COLOR_PRIMARY = [0.172, 0.243, 0.313, 1]  # #2C3E50
COLOR_SECONDARY = [0.2, 0.6, 0.86, 1]  # #3498DB
COLOR_SUCCESS = [0.153, 0.682, 0.376, 1]  # #27AE60
COLOR_WARNING = [0.953, 0.612, 0.071, 1]  # #F39C12
COLOR_DANGER = [0.906, 0.298, 0.235, 1]  # #E74C3C
COLOR_LIGHT = [0.925, 0.941, 0.945, 1]  # #ECF0F1
COLOR_DARK = [0.204, 0.286, 0.369, 1]  # #34495E

# Create necessary directories
def ensure_directories():
    """Create necessary directories if they don't exist"""
    Path(BACKUP_DIR).mkdir(parents=True, exist_ok=True)

# Initialize directories
ensure_directories()
