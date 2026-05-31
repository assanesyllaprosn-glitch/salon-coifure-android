"""
Business logic services for HOUSE FADE BARBER SHOP Android
Handles all core operations: clients, cards, transactions, etc.
"""

from datetime import datetime, date
from typing import Optional, List, Tuple
import database
import models
import config
import auth


class ClientService:
    """Service for client management"""
    
    def __init__(self, db: database.Database):
        self.db = db
    
    def create_client(self, nom: str, prenom: str, telephone: str, 
                     type_piece: str = "", numero_piece: str = "", 
                     adresse: str = "") -> Tuple[bool, str, Optional[models.Client]]:
        """
        Create a new client
        Returns (success, message, client)
        """
        # Check if phone number already exists
        existing = self.db.fetch_one(
            "SELECT id FROM clients WHERE telephone = ?",
            (telephone,)
        )
        if existing:
            return False, "Ce numéro de téléphone existe déjà", None
        
        # Insert client
        cursor = self.db.execute_query(
            """INSERT INTO clients (nom, prenom, telephone, type_piece, numero_piece, adresse)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (nom, prenom, telephone, type_piece, numero_piece, adresse)
        )
        
        if cursor:
            client_id = cursor.lastrowid
            client = self.get_client_by_id(client_id)
            return True, "Client créé avec succès", client
        
        return False, "Erreur lors de la création du client", None
    
    def update_client(self, client_id: int, nom: str = None, prenom: str = None,
                    telephone: str = None, type_piece: str = None, 
                    numero_piece: str = None, adresse: str = None) -> Tuple[bool, str]:
        """
        Update client information
        Returns (success, message)
        """
        # Build update query dynamically
        updates = []
        params = []
        
        if nom:
            updates.append("nom = ?")
            params.append(nom)
        
        if prenom:
            updates.append("prenom = ?")
            params.append(prenom)
        
        if telephone:
            # Check if phone number already exists for another client
            existing = self.db.fetch_one(
                "SELECT id FROM clients WHERE telephone = ? AND id != ?",
                (telephone, client_id)
            )
            if existing:
                return False, "Ce numéro de téléphone existe déjà"
            updates.append("telephone = ?")
            params.append(telephone)
        
        if type_piece is not None:
            updates.append("type_piece = ?")
            params.append(type_piece)
        
        if numero_piece is not None:
            updates.append("numero_piece = ?")
            params.append(numero_piece)
        
        if adresse is not None:
            updates.append("adresse = ?")
            params.append(adresse)
        
        if not updates:
            return False, "Aucune modification à effectuer"
        
        params.append(client_id)
        query = f"UPDATE clients SET {', '.join(updates)} WHERE id = ?"
        
        self.db.execute_query(query, params)
        
        return True, "Client mis à jour avec succès"
    
    def get_client_by_id(self, client_id: int) -> Optional[models.Client]:
        """Get client by ID"""
        result = self.db.fetch_one(
            "SELECT * FROM clients WHERE id = ?",
            (client_id,)
        )
        
        if not result:
            return None
        
        return models.Client(
            id=result['id'],
            nom=result['nom'],
            prenom=result['prenom'],
            telephone=result['telephone'],
            type_piece=result['type_piece'],
            numero_piece=result['numero_piece'],
            adresse=result['adresse'],
            date_creation=datetime.fromisoformat(result['date_creation']) if result['date_creation'] else None
        )
    
    def search_clients(self, search_term: str) -> List[models.Client]:
        """Search clients by name, phone, or ID number"""
        search_pattern = f"%{search_term}%"
        results = self.db.fetch_all(
            """SELECT * FROM clients 
               WHERE nom LIKE ? OR prenom LIKE ? OR telephone LIKE ? OR numero_piece LIKE ?
               ORDER BY nom, prenom""",
            (search_pattern, search_pattern, search_pattern, search_pattern)
        )
        
        clients = []
        for result in results:
            client = models.Client(
                id=result['id'],
                nom=result['nom'],
                prenom=result['prenom'],
                telephone=result['telephone'],
                type_piece=result['type_piece'],
                numero_piece=result['numero_piece'],
                adresse=result['adresse'],
                date_creation=datetime.fromisoformat(result['date_creation']) if result['date_creation'] else None
            )
            clients.append(client)
        
        return clients
    
    def get_all_clients(self) -> List[models.Client]:
        """Get all clients"""
        results = self.db.fetch_all("SELECT * FROM clients ORDER BY nom, prenom")
        
        clients = []
        for result in results:
            client = models.Client(
                id=result['id'],
                nom=result['nom'],
                prenom=result['prenom'],
                telephone=result['telephone'],
                type_piece=result['type_piece'],
                numero_piece=result['numero_piece'],
                adresse=result['adresse'],
                date_creation=datetime.fromisoformat(result['date_creation']) if result['date_creation'] else None
            )
            clients.append(client)
        
        return clients
    
    def get_client_cards(self, client_id: int) -> List[models.Carte]:
        """Get all cards for a client"""
        results = self.db.fetch_all(
            "SELECT * FROM cartes WHERE client_id = ? ORDER BY date_activation DESC",
            (client_id,)
        )
        
        cards = []
        for result in results:
            card = models.Carte(
                id=result['id'],
                uid_nfc=result['uid_nfc'],
                client_id=result['client_id'],
                statut=result['statut'],
                solde_points=result['solde_points'],
                date_activation=datetime.fromisoformat(result['date_activation']) if result['date_activation'] else None,
                date_derniere_operation=datetime.fromisoformat(result['date_derniere_operation']) if result['date_derniere_operation'] else None,
                date_expiration=datetime.fromisoformat(result['date_expiration']) if result['date_expiration'] else None
            )
            cards.append(card)
        
        return cards


class CardService:
    """Service for card management"""
    
    def __init__(self, db: database.Database):
        self.db = db
    
    def get_card_by_uid(self, uid_nfc: str) -> Optional[models.Carte]:
        """Get card by UID"""
        result = self.db.fetch_one(
            "SELECT * FROM cartes WHERE uid_nfc = ?",
            (uid_nfc,)
        )
        
        if not result:
            return None
        
        return models.Carte(
            id=result['id'],
            uid_nfc=result['uid_nfc'],
            client_id=result['client_id'],
            statut=result['statut'],
            solde_points=result['solde_points'],
            date_activation=datetime.fromisoformat(result['date_activation']) if result['date_activation'] else None,
            date_derniere_operation=datetime.fromisoformat(result['date_derniere_operation']) if result['date_derniere_operation'] else None,
            date_expiration=datetime.fromisoformat(result['date_expiration']) if result['date_expiration'] else None
        )
    
    def activate_card(self, uid_nfc: str, client_id: int, initial_points: int,
                     utilisateur_id: int, mode_paiement: str, 
                     reference_paiement: str = "", montant: int = 0) -> Tuple[bool, str, Optional[models.Carte]]:
        """
        Activate a new card
        Returns (success, message, card)
        """
        # Check if card already exists
        existing = self.get_card_by_uid(uid_nfc)
        if existing:
            return False, "Cette carte est déjà enregistrée", None
        
        # Validate initial points
        if initial_points not in [config.MIN_RECHARGE_POINTS, config.MAX_RECHARGE_POINTS]:
            return False, f"Le nombre de points doit être {config.MIN_RECHARGE_POINTS} ou {config.MAX_RECHARGE_POINTS}", None
        
        # Calculate expiration date based on points
        if initial_points == config.MIN_RECHARGE_POINTS:
            validity_months = config.VALIDITY_5_POINTS
        elif initial_points == config.MAX_RECHARGE_POINTS:
            validity_months = config.VALIDITY_10_POINTS
        else:
            validity_months = 0
        
        from dateutil.relativedelta import relativedelta
        date_expiration = datetime.now() + relativedelta(months=validity_months) if validity_months > 0 else None
        
        # Insert card
        cursor = self.db.execute_query(
            """INSERT INTO cartes (uid_nfc, client_id, statut, solde_points, date_activation, date_derniere_operation, date_expiration)
               VALUES (?, ?, 'active', ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)""",
            (uid_nfc, client_id, initial_points, date_expiration.isoformat() if date_expiration else None)
        )
        
        if not cursor:
            return False, "Erreur lors de l'activation de la carte", None
        
        carte_id = cursor.lastrowid
        
        # Create transaction
        cursor_trans = self.db.execute_query(
            """INSERT INTO transactions_points (carte_id, client_id, type_operation, points, solde_avant, solde_apres, montant, utilisateur_id, commentaire)
               VALUES (?, ?, 'activation', ?, 0, ?, ?, ?, 'Activation de carte')""",
            (carte_id, client_id, initial_points, initial_points, montant, utilisateur_id)
        )
        
        if not cursor_trans:
            return False, "Erreur lors de l'enregistrement de la transaction", None
        
        transaction_id = cursor_trans.lastrowid
        
        # Record payment
        self.db.execute_query(
            """INSERT INTO paiements (transaction_id, montant, mode_paiement, reference_paiement, utilisateur_id)
               VALUES (?, ?, ?, ?, ?)""",
            (transaction_id, montant, mode_paiement, reference_paiement, utilisateur_id)
        )
        
        card = self.get_card_by_id(carte_id)
        return True, "Carte activée avec succès", card
    
    def recharge_card(self, carte_id: int, points: int, utilisateur_id: int,
                     mode_paiement: str, reference_paiement: str = "", montant: int = 0) -> Tuple[bool, str, Optional[models.Carte]]:
        """
        Recharge a card
        Returns (success, message, card)
        """
        # Get card
        card = self.get_card_by_id(carte_id)
        if not card:
            return False, "Carte non trouvée", None
        
        # Validate points
        if points < config.MIN_RECHARGE_POINTS:
            return False, f"La recharge minimale est de {config.MIN_RECHARGE_POINTS} points", None
        
        if points > config.MAX_RECHARGE_POINTS:
            return False, f"La recharge maximale est de {config.MAX_RECHARGE_POINTS} points", None
        
        # Check card status
        if card.statut != config.CARD_STATUS_ACTIVE:
            return False, "Cette carte ne peut pas être rechargée", None
        
        # Calculate expiration date based on points
        if points == config.MIN_RECHARGE_POINTS:
            validity_months = config.VALIDITY_5_POINTS
        elif points == config.MAX_RECHARGE_POINTS:
            validity_months = config.VALIDITY_10_POINTS
        else:
            validity_months = 0
        
        from dateutil.relativedelta import relativedelta
        date_expiration = datetime.now() + relativedelta(months=validity_months) if validity_months > 0 else None
        
        solde_avant = card.solde_points
        solde_apres = solde_avant + points
        
        # Update card balance and expiration date
        self.db.execute_query(
            """UPDATE cartes SET solde_points = ?, date_derniere_operation = CURRENT_TIMESTAMP, date_expiration = ?
               WHERE id = ?""",
            (solde_apres, date_expiration.isoformat() if date_expiration else None, carte_id)
        )
        
        # Create transaction
        cursor = self.db.execute_query(
            """INSERT INTO transactions_points (carte_id, client_id, type_operation, points, solde_avant, solde_apres, montant, utilisateur_id, commentaire)
               VALUES (?, ?, 'recharge', ?, ?, ?, ?, ?, 'Recharge de carte')""",
            (carte_id, card.client_id, points, solde_avant, solde_apres, montant, utilisateur_id)
        )
        
        if not cursor:
            return False, "Erreur lors de l'enregistrement de la transaction", None
        
        transaction_id = cursor.lastrowid
        
        # Record payment
        self.db.execute_query(
            """INSERT INTO paiements (transaction_id, montant, mode_paiement, reference_paiement, utilisateur_id)
               VALUES (?, ?, ?, ?, ?)""",
            (transaction_id, montant, mode_paiement, reference_paiement, utilisateur_id)
        )
        
        updated_card = self.get_card_by_id(carte_id)
        return True, "Recharge effectuée avec succès", updated_card
    
    def debit_card(self, carte_id: int, utilisateur_id: int) -> Tuple[bool, str, Optional[models.Carte]]:
        """
        Debit 1 point from card
        Returns (success, message, card)
        """
        # Get card
        card = self.get_card_by_id(carte_id)
        if not card:
            return False, "Carte non trouvée", None
        
        # Check card status
        if card.statut != config.CARD_STATUS_ACTIVE:
            return False, "Cette carte ne peut pas être débitée", None
        
        # Check if points are expired
        if card.est_expirée:
            # Reset points to 0 if expired
            self.db.execute_query(
                """UPDATE cartes SET solde_points = 0, date_derniere_operation = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (carte_id,)
            )
            return False, "Les points de cette carte ont expiré. Veuillez recharger la carte.", None
        
        # Check balance
        if card.solde_points <= 0:
            return False, "Solde insuffisant. Veuillez recharger la carte.", None
        
        # Debit 1 point
        solde_avant = card.solde_points
        solde_apres = solde_avant - 1
        
        # Update card balance
        self.db.execute_query(
            """UPDATE cartes SET solde_points = ?, date_derniere_operation = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (solde_apres, carte_id)
        )
        
        # Create transaction
        self.db.execute_query(
            """INSERT INTO transactions_points (carte_id, client_id, type_operation, points, solde_avant, solde_apres, montant, utilisateur_id, commentaire)
               VALUES (?, ?, 'debit', -1, ?, ?, 0, ?, 'Débit pour coiffure')""",
            (carte_id, card.client_id, solde_avant, solde_apres, utilisateur_id)
        )
        
        updated_card = self.get_card_by_id(carte_id)
        return True, "Débit effectué avec succès", updated_card
    
    def block_card(self, carte_id: int, utilisateur_id: int, commentaire: str = "") -> Tuple[bool, str]:
        """
        Block a card (admin only)
        Returns (success, message)
        """
        # Get card
        card = self.get_card_by_id(carte_id)
        if not card:
            return False, "Carte non trouvée"
        
        # Update card status
        self.db.execute_query(
            """UPDATE cartes SET statut = 'bloquée', date_derniere_operation = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (carte_id,)
        )
        
        # Create transaction
        self.db.execute_query(
            """INSERT INTO transactions_points (carte_id, client_id, type_operation, points, solde_avant, solde_apres, montant, utilisateur_id, commentaire)
               VALUES (?, ?, 'blocage', 0, ?, ?, 0, ?, ?)""",
            (carte_id, card.client_id, card.solde_points, card.solde_points, utilisateur_id, commentaire or "Carte bloquée")
        )
        
        return True, "Carte bloquée avec succès"
    
    def replace_card(self, old_carte_id: int, new_uid_nfc: str, utilisateur_id: int) -> Tuple[bool, str, Optional[models.Carte]]:
        """
        Replace a card (admin only)
        Returns (success, message, new_card)
        """
        # Get old card
        old_card = self.get_card_by_id(old_carte_id)
        if not old_card:
            return False, "Carte non trouvée", None
        
        # Check if new UID already exists
        existing = self.get_card_by_uid(new_uid_nfc)
        if existing:
            return False, "Cette nouvelle carte est déjà enregistrée", None
        
        # Mark old card as replaced
        self.db.execute_query(
            """UPDATE cartes SET statut = 'remplacée', date_derniere_operation = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (old_carte_id,)
        )
        
        # Create transaction for old card
        self.db.execute_query(
            """INSERT INTO transactions_points (carte_id, client_id, type_operation, points, solde_avant, solde_apres, montant, utilisateur_id, commentaire)
               VALUES (?, ?, 'remplacement', 0, ?, ?, 0, ?, 'Carte remplacée')""",
            (old_carte_id, old_card.client_id, old_card.solde_points, old_card.solde_points, utilisateur_id)
        )
        
        # Create new card with same balance and expiration date
        cursor = self.db.execute_query(
            """INSERT INTO cartes (uid_nfc, client_id, statut, solde_points, date_activation, date_derniere_operation, date_expiration)
               VALUES (?, ?, 'active', ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)""",
            (new_uid_nfc, old_card.client_id, old_card.solde_points, old_card.date_expiration.isoformat() if old_card.date_expiration else None)
        )
        
        if not cursor:
            return False, "Erreur lors de la création de la nouvelle carte", None
        
        new_carte_id = cursor.lastrowid
        
        # Create transaction for new card
        self.db.execute_query(
            """INSERT INTO transactions_points (carte_id, client_id, type_operation, points, solde_avant, solde_apres, montant, utilisateur_id, commentaire)
               VALUES (?, ?, 'activation', ?, 0, ?, 0, ?, 'Remplacement de carte')""",
            (new_carte_id, old_card.client_id, old_card.solde_points, old_card.solde_points, utilisateur_id)
        )
        
        new_card = self.get_card_by_id(new_carte_id)
        return True, "Carte remplacée avec succès", new_card
    
    def get_card_by_id(self, carte_id: int) -> Optional[models.Carte]:
        """Get card by ID"""
        result = self.db.fetch_one(
            "SELECT * FROM cartes WHERE id = ?",
            (carte_id,)
        )
        
        if not result:
            return None
        
        return models.Carte(
            id=result['id'],
            uid_nfc=result['uid_nfc'],
            client_id=result['client_id'],
            statut=result['statut'],
            solde_points=result['solde_points'],
            date_activation=datetime.fromisoformat(result['date_activation']) if result['date_activation'] else None,
            date_derniere_operation=datetime.fromisoformat(result['date_derniere_operation']) if result['date_derniere_operation'] else None,
            date_expiration=datetime.fromisoformat(result['date_expiration']) if result['date_expiration'] else None
        )
    
    def get_all_cards(self) -> List[models.Carte]:
        """Get all cards"""
        results = self.db.fetch_all("SELECT * FROM cartes ORDER BY date_activation DESC")
        
        cards = []
        for result in results:
            card = models.Carte(
                id=result['id'],
                uid_nfc=result['uid_nfc'],
                client_id=result['client_id'],
                statut=result['statut'],
                solde_points=result['solde_points'],
                date_activation=datetime.fromisoformat(result['date_activation']) if result['date_activation'] else None,
                date_derniere_operation=datetime.fromisoformat(result['date_derniere_operation']) if result['date_derniere_operation'] else None,
                date_expiration=datetime.fromisoformat(result['date_expiration']) if result['date_expiration'] else None
            )
            cards.append(card)
        
        return cards
    
    def get_cards_with_low_balance(self, threshold: int = 2) -> List[models.Carte]:
        """Get cards with balance below threshold"""
        results = self.db.fetch_all(
            """SELECT * FROM cartes 
               WHERE statut = 'active' AND solde_points > 0 AND solde_points <= ?
               ORDER BY solde_points ASC""",
            (threshold,)
        )
        
        cards = []
        for result in results:
            card = models.Carte(
                id=result['id'],
                uid_nfc=result['uid_nfc'],
                client_id=result['client_id'],
                statut=result['statut'],
                solde_points=result['solde_points'],
                date_activation=datetime.fromisoformat(result['date_activation']) if result['date_activation'] else None,
                date_derniere_operation=datetime.fromisoformat(result['date_derniere_operation']) if result['date_derniere_operation'] else None,
                date_expiration=datetime.fromisoformat(result['date_expiration']) if result['date_expiration'] else None
            )
            cards.append(card)
        
        return cards
    
    def get_cards_with_zero_balance(self) -> List[models.Carte]:
        """Get cards with zero balance"""
        results = self.db.fetch_all(
            """SELECT * FROM cartes 
               WHERE statut = 'active' AND solde_points = 0
               ORDER BY date_derniere_operation DESC"""
        )
        
        cards = []
        for result in results:
            card = models.Carte(
                id=result['id'],
                uid_nfc=result['uid_nfc'],
                client_id=result['client_id'],
                statut=result['statut'],
                solde_points=result['solde_points'],
                date_activation=datetime.fromisoformat(result['date_activation']) if result['date_activation'] else None,
                date_derniere_operation=datetime.fromisoformat(result['date_derniere_operation']) if result['date_derniere_operation'] else None,
                date_expiration=datetime.fromisoformat(result['date_expiration']) if result['date_expiration'] else None
            )
            cards.append(card)
        
        return cards


class TransactionService:
    """Service for transaction management"""
    
    def __init__(self, db: database.Database):
        self.db = db
    
    def get_transaction_history(self, client_id: int = None, carte_id: int = None,
                               date_debut: date = None, date_fin: date = None,
                               type_operation: str = None, utilisateur_id: int = None) -> List[models.TransactionPoint]:
        """Get transaction history with filters"""
        query = "SELECT * FROM transactions_points WHERE 1=1"
        params = []
        
        if client_id:
            query += " AND client_id = ?"
            params.append(client_id)
        
        if carte_id:
            query += " AND carte_id = ?"
            params.append(carte_id)
        
        if date_debut:
            query += " AND date_operation >= ?"
            params.append(date_debut.isoformat())
        
        if date_fin:
            query += " AND date_operation <= ?"
            params.append(date_fin.isoformat())
        
        if type_operation:
            query += " AND type_operation = ?"
            params.append(type_operation)
        
        if utilisateur_id:
            query += " AND utilisateur_id = ?"
            params.append(utilisateur_id)
        
        query += " ORDER BY date_operation DESC"
        
        results = self.db.fetch_all(query, params)
        
        transactions = []
        for result in results:
            transaction = models.TransactionPoint(
                id=result['id'],
                carte_id=result['carte_id'],
                client_id=result['client_id'],
                type_operation=result['type_operation'],
                points=result['points'],
                solde_avant=result['solde_avant'],
                solde_apres=result['solde_apres'],
                montant=result['montant'],
                utilisateur_id=result['utilisateur_id'],
                date_operation=datetime.fromisoformat(result['date_operation']) if result['date_operation'] else None,
                commentaire=result['commentaire']
            )
            transactions.append(transaction)
        
        return transactions
    
    def cancel_transaction(self, transaction_id: int, utilisateur_id: int, commentaire: str = "") -> Tuple[bool, str]:
        """
        Cancel a transaction (admin only)
        Returns (success, message)
        """
        # Get original transaction
        result = self.db.fetch_one(
            "SELECT * FROM transactions_points WHERE id = ?",
            (transaction_id,)
        )
        
        if not result:
            return False, "Transaction non trouvée"
        
        # Only allow cancellation of debit transactions
        if result['type_operation'] != config.TRANSACTION_DEBIT:
            return False, "Seuls les débits peuvent être annulés"
        
        carte_id = result['carte_id']
        client_id = result['client_id']
        points = abs(result['points'])  # Get absolute value
        solde_actuel = result['solde_apres']
        nouveau_solde = solde_actuel + points
        
        # Update card balance
        self.db.execute_query(
            """UPDATE cartes SET solde_points = ?, date_derniere_operation = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (nouveau_solde, carte_id)
        )
        
        # Create cancellation transaction
        self.db.execute_query(
            """INSERT INTO transactions_points (carte_id, client_id, type_operation, points, solde_avant, solde_apres, montant, utilisateur_id, commentaire)
               VALUES (?, ?, 'annulation', ?, ?, ?, 0, ?, ?)""",
            (carte_id, client_id, points, solde_actuel, nouveau_solde, utilisateur_id, commentaire or f"Annulation de la transaction #{transaction_id}")
        )
        
        return True, "Transaction annulée avec succès"
    
    def get_payments(self, date_debut: date = None, date_fin: date = None,
                    mode_paiement: str = None) -> List[models.Paiement]:
        """Get payments with filters"""
        query = """SELECT p.*, t.client_id, t.carte_id 
                   FROM paiements p
                   JOIN transactions_points t ON p.transaction_id = t.id
                   WHERE 1=1"""
        params = []
        
        if date_debut:
            query += " AND p.date_paiement >= ?"
            params.append(date_debut.isoformat())
        
        if date_fin:
            query += " AND p.date_paiement <= ?"
            params.append(date_fin.isoformat())
        
        if mode_paiement:
            query += " AND p.mode_paiement = ?"
            params.append(mode_paiement)
        
        query += " ORDER BY p.date_paiement DESC"
        
        results = self.db.fetch_all(query, params)
        
        payments = []
        for result in results:
            payment = models.Paiement(
                id=result['id'],
                transaction_id=result['transaction_id'],
                montant=result['montant'],
                mode_paiement=result['mode_paiement'],
                reference_paiement=result['reference_paiement'],
                date_paiement=datetime.fromisoformat(result['date_paiement']) if result['date_paiement'] else None,
                utilisateur_id=result['utilisateur_id']
            )
            payments.append(payment)
        
        return payments


class ReportService:
    """Service for generating reports"""
    
    def __init__(self, db: database.Database):
        self.db = db
    
    def get_dashboard_stats(self) -> models.DashboardStats:
        """Get dashboard statistics"""
        stats = models.DashboardStats()
        
        # Total clients
        result = self.db.fetch_one("SELECT COUNT(*) as count FROM clients")
        stats.total_clients = result['count'] if result else 0
        
        # Total active cards
        result = self.db.fetch_one("SELECT COUNT(*) as count FROM cartes WHERE statut = 'active'")
        stats.total_cartes_actives = result['count'] if result else 0
        
        # Total blocked cards
        result = self.db.fetch_one("SELECT COUNT(*) as count FROM cartes WHERE statut = 'bloquée'")
        stats.total_cartes_bloquees = result['count'] if result else 0
        
        # Total cards with zero balance
        result = self.db.fetch_one("SELECT COUNT(*) as count FROM cartes WHERE statut = 'active' AND solde_points = 0")
        stats.total_cartes_solde_zero = result['count'] if result else 0
        
        # Today's stats
        today = date.today()
        today_str = today.isoformat()
        
        # Total recharges today
        result = self.db.fetch_one(
            """SELECT COUNT(*) as count FROM transactions_points 
               WHERE type_operation = 'recharge' AND DATE(date_operation) = ?""",
            (today_str,)
        )
        stats.total_recharges_jour = result['count'] if result else 0
        
        # Total debits today
        result = self.db.fetch_one(
            """SELECT COUNT(*) as count FROM transactions_points 
               WHERE type_operation = 'debit' AND DATE(date_operation) = ?""",
            (today_str,)
        )
        stats.total_debits_jour = result['count'] if result else 0
        
        # Today's revenue
        result = self.db.fetch_one(
            """SELECT COALESCE(SUM(montant), 0) as total FROM paiements 
               WHERE DATE(date_paiement) = ?""",
            (today_str,)
        )
        stats.chiffre_affaires_jour = result['total'] if result else 0
        
        # Month's revenue
        first_day_of_month = date(today.year, today.month, 1)
        result = self.db.fetch_one(
            """SELECT COALESCE(SUM(montant), 0) as total FROM paiements 
               WHERE DATE(date_paiement) >= ?""",
            (first_day_of_month.isoformat(),)
        )
        stats.chiffre_affaires_mois = result['total'] if result else 0
        
        return stats
    
    def get_daily_revenue(self, date_target: date) -> int:
        """Get revenue for a specific day"""
        result = self.db.fetch_one(
            """SELECT COALESCE(SUM(montant), 0) as total FROM paiements 
               WHERE DATE(date_paiement) = ?""",
            (date_target.isoformat(),)
        )
        return result['total'] if result else 0
    
    def get_monthly_revenue(self, year: int, month: int) -> int:
        """Get revenue for a specific month"""
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1)
        else:
            last_day = date(year, month + 1, 1)
        
        result = self.db.fetch_one(
            """SELECT COALESCE(SUM(montant), 0) as total FROM paiements 
               WHERE DATE(date_paiement) >= ? AND DATE(date_paiement) < ?""",
            (first_day.isoformat(), last_day.isoformat())
        )
        return result['total'] if result else 0
    
    def get_most_loyal_clients(self, limit: int = 10) -> List[Tuple[models.Client, int]]:
        """Get most loyal clients (most haircuts)"""
        results = self.db.fetch_all(
            """SELECT c.*, COUNT(t.id) as haircut_count 
               FROM clients c
               JOIN cartes ca ON c.id = ca.client_id
               JOIN transactions_points t ON ca.id = t.carte_id AND t.type_operation = 'debit'
               GROUP BY c.id
               ORDER BY haircut_count DESC
               LIMIT ?""",
            (limit,)
        )
        
        loyal_clients = []
        for result in results:
            client = models.Client(
                id=result['id'],
                nom=result['nom'],
                prenom=result['prenom'],
                telephone=result['telephone'],
                type_piece=result['type_piece'],
                numero_piece=result['numero_piece'],
                adresse=result['adresse'],
                date_creation=datetime.fromisoformat(result['date_creation']) if result['date_creation'] else None
            )
            loyal_clients.append((client, result['haircut_count']))
        
        return loyal_clients
    
    def get_recharge_stats(self, date_debut: date = None, date_fin: date = None) -> dict:
        """Get recharge statistics"""
        query = """SELECT COUNT(*) as count, COALESCE(SUM(points), 0) as total_points, COALESCE(SUM(montant), 0) as total_amount
                   FROM transactions_points
                   WHERE type_operation = 'recharge'"""
        params = []
        
        if date_debut:
            query += " AND DATE(date_operation) >= ?"
            params.append(date_debut.isoformat())
        
        if date_fin:
            query += " AND DATE(date_operation) <= ?"
            params.append(date_fin.isoformat())
        
        result = self.db.fetch_one(query, params)
        
        return {
            'count': result['count'] if result else 0,
            'total_points': result['total_points'] if result else 0,
            'total_amount': result['total_amount'] if result else 0
        }
    
    def get_haircut_stats(self, date_debut: date = None, date_fin: date = None) -> dict:
        """Get haircut statistics"""
        query = """SELECT COUNT(*) as count
                   FROM transactions_points
                   WHERE type_operation = 'debit'"""
        params = []
        
        if date_debut:
            query += " AND DATE(date_operation) >= ?"
            params.append(date_debut.isoformat())
        
        if date_fin:
            query += " AND DATE(date_operation) <= ?"
            params.append(date_fin.isoformat())
        
        result = self.db.fetch_one(query, params)
        
        return {
            'count': result['count'] if result else 0
        }


class SettingsService:
    """Service for application settings"""
    
    def __init__(self, db: database.Database):
        self.db = db
    
    def get_setting(self, key: str) -> str:
        """Get a setting value"""
        return self.db.get_parameter(key)
    
    def set_setting(self, key: str, value: str) -> bool:
        """Set a setting value"""
        try:
            self.db.set_parameter(key, value)
            return True
        except Exception:
            return False
    
    def get_all_settings(self) -> dict:
        """Get all settings"""
        results = self.db.fetch_all("SELECT * FROM parametres")
        settings = {}
        for result in results:
            settings[result['cle']] = result['valeur']
        return settings
    
    def update_business_settings(self, prix_normal: int, prix_point: int, 
                                 recharge_min: int, recharge_max: int,
                                 nom_salon: str, devise: str) -> Tuple[bool, str]:
        """Update business settings"""
        try:
            self.set_setting('prix_normal_coiffure', str(prix_normal))
            self.set_setting('prix_point', str(prix_point))
            self.set_setting('recharge_min', str(recharge_min))
            self.set_setting('recharge_max', str(recharge_max))
            self.set_setting('nom_salon', nom_salon)
            self.set_setting('devise', devise)
            return True, "Paramètres mis à jour avec succès"
        except Exception as e:
            return False, f"Erreur lors de la mise à jour: {str(e)}"


# Global service instances
client_service = ClientService(database.db)
card_service = CardService(database.db)
transaction_service = TransactionService(database.db)
report_service = ReportService(database.db)
settings_service = SettingsService(database.db)
