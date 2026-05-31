"""
Database module for HOUSE FADE BARBER SHOP Android
Handles SQLite database initialization and operations
"""

import sqlite3
import shutil
from datetime import datetime
from pathlib import Path
import config
import hashlib


class Database:
    """Database manager for the barber shop application"""
    
    def __init__(self, db_path=None):
        """Initialize database connection"""
        self.db_path = db_path or config.DB_PATH
        self.connection = None
        self.connect()
        self.create_tables()
        self.create_default_admin()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            return True
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Execute a SQL query"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            self.connection.rollback()
            return None
    
    def fetch_all(self, query, params=None):
        """Fetch all results from a query"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des données: {e}")
            return []
    
    def fetch_one(self, query, params=None):
        """Fetch one result from a query"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des données: {e}")
            return None
    
    def create_tables(self):
        """Create all database tables"""
        # Table clients
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                telephone TEXT NOT NULL UNIQUE,
                type_piece TEXT,
                numero_piece TEXT,
                adresse TEXT,
                date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table cartes
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS cartes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid_nfc TEXT NOT NULL UNIQUE,
                client_id INTEGER NOT NULL,
                statut TEXT DEFAULT 'active',
                solde_points INTEGER DEFAULT 0,
                date_activation DATETIME DEFAULT CURRENT_TIMESTAMP,
                date_derniere_operation DATETIME DEFAULT CURRENT_TIMESTAMP,
                date_expiration DATETIME,
                FOREIGN KEY (client_id) REFERENCES clients(id)
            )
        """)
        
        # Table transactions_points
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS transactions_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                carte_id INTEGER NOT NULL,
                client_id INTEGER NOT NULL,
                type_operation TEXT NOT NULL,
                points INTEGER DEFAULT 0,
                solde_avant INTEGER DEFAULT 0,
                solde_apres INTEGER DEFAULT 0,
                montant INTEGER DEFAULT 0,
                utilisateur_id INTEGER,
                date_operation DATETIME DEFAULT CURRENT_TIMESTAMP,
                commentaire TEXT,
                FOREIGN KEY (carte_id) REFERENCES cartes(id),
                FOREIGN KEY (client_id) REFERENCES clients(id),
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
            )
        """)
        
        # Table paiements
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS paiements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER NOT NULL,
                montant INTEGER NOT NULL,
                mode_paiement TEXT NOT NULL,
                reference_paiement TEXT,
                date_paiement DATETIME DEFAULT CURRENT_TIMESTAMP,
                utilisateur_id INTEGER,
                FOREIGN KEY (transaction_id) REFERENCES transactions_points(id),
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
            )
        """)
        
        # Table utilisateurs
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                login TEXT NOT NULL UNIQUE,
                mot_de_passe_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                actif INTEGER DEFAULT 1,
                date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table parametres
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS parametres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cle TEXT NOT NULL UNIQUE,
                valeur TEXT NOT NULL,
                date_modification DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for better performance
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_cartes_uid ON cartes(uid_nfc)")
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_cartes_client ON cartes(client_id)")
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_transactions_carte ON transactions_points(carte_id)")
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_transactions_client ON transactions_points(client_id)")
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions_points(date_operation)")
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_paiements_transaction ON paiements(transaction_id)")
        
        # Initialize default parameters
        self.initialize_parameters()
    
    def initialize_parameters(self):
        """Initialize default system parameters"""
        params = [
            ('prix_normal_coiffure', str(config.NORMAL_HAIRCUT_PRICE)),
            ('prix_carte', str(config.CARD_PRICE)),
            ('recharge_5_points', str(config.RECHARGE_5_POINTS)),
            ('recharge_10_points', str(config.RECHARGE_10_POINTS)),
            ('recharge_min', str(config.MIN_RECHARGE_POINTS)),
            ('recharge_max', str(config.MAX_RECHARGE_POINTS)),
            ('nom_salon', config.APP_NAME),
            ('devise', config.CURRENCY)
        ]
        
        for key, value in params:
            existing = self.fetch_one(
                "SELECT id FROM parametres WHERE cle = ?",
                (key,)
            )
            if not existing:
                self.execute_query(
                    "INSERT INTO parametres (cle, valeur) VALUES (?, ?)",
                    (key, value)
                )
    
    def create_default_admin(self):
        """Create default administrator account if none exists"""
        admin = self.fetch_one(
            "SELECT id FROM utilisateurs WHERE role = ?",
            (config.ROLE_ADMIN,)
        )
        
        if not admin:
            # Default admin: admin/admin123
            password_hash = self.hash_password("admin123")
            self.execute_query(
                """INSERT INTO utilisateurs (nom, login, mot_de_passe_hash, role, actif)
                   VALUES (?, ?, ?, ?, 1)""",
                ("Administrateur", "admin", password_hash, config.ROLE_ADMIN)
            )
            print("Compte administrateur par défaut créé (login: admin, mot de passe: admin123)")
    
    @staticmethod
    def hash_password(password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, password_hash):
        """Verify a password against its hash"""
        return self.hash_password(password) == password_hash
    
    def backup_database(self):
        """Create a backup of the database"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{config.BACKUP_DIR}/barber_shop_backup_{timestamp}.db"
            shutil.copy2(self.db_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return None
    
    def get_parameter(self, key):
        """Get a parameter value"""
        result = self.fetch_one(
            "SELECT valeur FROM parametres WHERE cle = ?",
            (key,)
        )
        return result['valeur'] if result else None
    
    def set_parameter(self, key, value):
        """Set a parameter value"""
        existing = self.fetch_one(
            "SELECT id FROM parametres WHERE cle = ?",
            (key,)
        )
        if existing:
            self.execute_query(
                "UPDATE parametres SET valeur = ?, date_modification = CURRENT_TIMESTAMP WHERE cle = ?",
                (value, key)
            )
        else:
            self.execute_query(
                "INSERT INTO parametres (cle, valeur) VALUES (?, ?)",
                (key, value)
            )


# Global database instance
db = Database()
