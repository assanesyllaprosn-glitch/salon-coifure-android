"""
Data models for HOUSE FADE BARBER SHOP Android
Defines data structures for clients, cards, transactions, etc.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Client:
    """Client data model"""
    id: Optional[int] = None
    nom: str = ""
    prenom: str = ""
    telephone: str = ""
    type_piece: str = ""
    numero_piece: str = ""
    adresse: str = ""
    date_creation: Optional[datetime] = None
    
    @property
    def nom_complet(self):
        """Return full name"""
        return f"{self.prenom} {self.nom}"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'telephone': self.telephone,
            'type_piece': self.type_piece,
            'numero_piece': self.numero_piece,
            'adresse': self.adresse,
            'date_creation': self.date_creation
        }


@dataclass
class Carte:
    """Card data model"""
    id: Optional[int] = None
    uid_nfc: str = ""
    client_id: int = 0
    statut: str = "active"
    solde_points: int = 0
    date_activation: Optional[datetime] = None
    date_derniere_operation: Optional[datetime] = None
    date_expiration: Optional[datetime] = None
    
    # Related client (loaded separately)
    client: Optional[Client] = None
    
    @property
    def est_active(self):
        """Check if card is active"""
        return self.statut == "active"
    
    @property
    def peut_etre_debitee(self):
        """Check if card can be debited"""
        return self.est_active and self.solde_points > 0
    
    @property
    def est_expirée(self):
        """Check if card points are expired"""
        if not self.date_expiration:
            return False
        return datetime.now() > self.date_expiration
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'uid_nfc': self.uid_nfc,
            'client_id': self.client_id,
            'statut': self.statut,
            'solde_points': self.solde_points,
            'date_activation': self.date_activation,
            'date_derniere_operation': self.date_derniere_operation,
            'date_expiration': self.date_expiration
        }


@dataclass
class TransactionPoint:
    """Point transaction data model"""
    id: Optional[int] = None
    carte_id: Optional[int] = None
    client_id: Optional[int] = None
    type_operation: str = ""
    points: int = 0
    solde_avant: int = 0
    solde_apres: int = 0
    montant: int = 0
    utilisateur_id: Optional[int] = None
    date_operation: Optional[datetime] = None
    commentaire: str = ""
    
    # Related objects (loaded separately)
    carte: Optional[Carte] = None
    client: Optional[Client] = None
    utilisateur: Optional['Utilisateur'] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'carte_id': self.carte_id,
            'client_id': self.client_id,
            'type_operation': self.type_operation,
            'points': self.points,
            'solde_avant': self.solde_avant,
            'solde_apres': self.solde_apres,
            'montant': self.montant,
            'utilisateur_id': self.utilisateur_id,
            'date_operation': self.date_operation,
            'commentaire': self.commentaire
        }


@dataclass
class Paiement:
    """Payment data model"""
    id: Optional[int] = None
    transaction_id: Optional[int] = None
    montant: int = 0
    mode_paiement: str = ""
    reference_paiement: str = ""
    date_paiement: Optional[datetime] = None
    utilisateur_id: Optional[int] = None
    
    # Related objects (loaded separately)
    transaction: Optional[TransactionPoint] = None
    utilisateur: Optional['Utilisateur'] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'montant': self.montant,
            'mode_paiement': self.mode_paiement,
            'reference_paiement': self.reference_paiement,
            'date_paiement': self.date_paiement,
            'utilisateur_id': self.utilisateur_id
        }


@dataclass
class Utilisateur:
    """User data model"""
    id: Optional[int] = None
    nom: str = ""
    login: str = ""
    mot_de_passe_hash: str = ""
    role: str = ""
    actif: bool = True
    date_creation: Optional[datetime] = None
    
    @property
    def est_admin(self):
        """Check if user is admin"""
        return self.role == "administrateur"
    
    @property
    def est_caissier(self):
        """Check if user is cashier"""
        return self.role == "caissier"
    
    @property
    def est_coiffeur(self):
        """Check if user is barber"""
        return self.role == "coiffeur"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'nom': self.nom,
            'login': self.login,
            'mot_de_passe_hash': self.mot_de_passe_hash,
            'role': self.role,
            'actif': self.actif,
            'date_creation': self.date_creation
        }


@dataclass
class Parametre:
    """Parameter data model"""
    id: Optional[int] = None
    cle: str = ""
    valeur: str = ""
    date_modification: Optional[datetime] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'cle': self.cle,
            'valeur': self.valeur,
            'date_modification': self.date_modification
        }


@dataclass
class DashboardStats:
    """Dashboard statistics data model"""
    total_clients: int = 0
    total_cartes_actives: int = 0
    total_cartes_bloquees: int = 0
    total_cartes_solde_zero: int = 0
    total_recharges_jour: int = 0
    total_debits_jour: int = 0
    chiffre_affaires_jour: int = 0
    chiffre_affaires_mois: int = 0
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'total_clients': self.total_clients,
            'total_cartes_actives': self.total_cartes_actives,
            'total_cartes_bloquees': self.total_cartes_bloquees,
            'total_cartes_solde_zero': self.total_cartes_solde_zero,
            'total_recharges_jour': self.total_recharges_jour,
            'total_debits_jour': self.total_debits_jour,
            'chiffre_affaires_jour': self.chiffre_affaires_jour,
            'chiffre_affaires_mois': self.chiffre_affaires_mois
        }


@dataclass
class Rapport:
    """Report data model"""
    type_rapport: str = ""
    date_debut: Optional[datetime] = None
    date_fin: Optional[datetime] = None
    donnees: dict = None
    
    def __post_init__(self):
        if self.donnees is None:
            self.donnees = {}
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'type_rapport': self.type_rapport,
            'date_debut': self.date_debut,
            'date_fin': self.date_fin,
            'donnees': self.donnees
        }
