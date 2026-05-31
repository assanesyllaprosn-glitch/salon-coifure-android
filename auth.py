"""
Authentication module for HOUSE FADE BARBER SHOP Android
Handles user authentication and authorization
"""

from datetime import datetime
from typing import Optional
import database
import models
import config


class AuthService:
    """Authentication service"""
    
    def __init__(self, db: database.Database):
        self.db = db
        self.current_user: Optional[models.Utilisateur] = None
    
    def login(self, login: str, password: str) -> tuple[bool, str, Optional[models.Utilisateur]]:
        """
        Authenticate user with login and password
        Returns (success, message, user)
        """
        # Get user from database
        result = self.db.fetch_one(
            "SELECT * FROM utilisateurs WHERE login = ? AND actif = 1",
            (login,)
        )
        
        if not result:
            return False, "Login ou mot de passe incorrect", None
        
        # Verify password
        if not self.db.verify_password(password, result['mot_de_passe_hash']):
            return False, "Login ou mot de passe incorrect", None
        
        # Create user object
        user = models.Utilisateur(
            id=result['id'],
            nom=result['nom'],
            login=result['login'],
            mot_de_passe_hash=result['mot_de_passe_hash'],
            role=result['role'],
            actif=bool(result['actif']),
            date_creation=datetime.fromisoformat(result['date_creation']) if result['date_creation'] else None
        )
        
        self.current_user = user
        return True, "Connexion réussie", user
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[models.Utilisateur]:
        """Get current logged in user"""
        return self.current_user
    
    def has_permission(self, required_role: str) -> bool:
        """
        Check if current user has required permission
        Admin has all permissions
        """
        if not self.current_user:
            return False
        
        if self.current_user.est_admin:
            return True
        
        return self.current_user.role == required_role
    
    def can_manage_clients(self) -> bool:
        """Check if user can manage clients"""
        return self.has_permission(config.ROLE_CASHIER) or self.has_permission(config.ROLE_ADMIN)
    
    def can_activate_cards(self) -> bool:
        """Check if user can activate cards"""
        return self.has_permission(config.ROLE_CASHIER) or self.has_permission(config.ROLE_ADMIN)
    
    def can_recharge_cards(self) -> bool:
        """Check if user can recharge cards"""
        return self.has_permission(config.ROLE_CASHIER) or self.has_permission(config.ROLE_ADMIN)
    
    def can_debit_cards(self) -> bool:
        """Check if user can debit cards"""
        return self.has_permission(config.ROLE_BARBER) or self.has_permission(config.ROLE_ADMIN)
    
    def can_block_cards(self) -> bool:
        """Check if user can block cards"""
        return self.has_permission(config.ROLE_ADMIN)
    
    def can_replace_cards(self) -> bool:
        """Check if user can replace cards"""
        return self.has_permission(config.ROLE_ADMIN)
    
    def can_cancel_transactions(self) -> bool:
        """Check if user can cancel transactions"""
        return self.has_permission(config.ROLE_ADMIN)
    
    def can_manage_users(self) -> bool:
        """Check if user can manage users"""
        return self.has_permission(config.ROLE_ADMIN)
    
    def can_view_reports(self) -> bool:
        """Check if user can view reports"""
        return self.has_permission(config.ROLE_ADMIN)
    
    def can_change_settings(self) -> bool:
        """Check if user can change settings"""
        return self.has_permission(config.ROLE_ADMIN)
    
    def create_user(self, nom: str, login: str, password: str, role: str) -> tuple[bool, str]:
        """
        Create a new user (admin only)
        Returns (success, message)
        """
        if not self.can_manage_users():
            return False, "Permission refusée"
        
        # Check if login already exists
        existing = self.db.fetch_one(
            "SELECT id FROM utilisateurs WHERE login = ?",
            (login,)
        )
        if existing:
            return False, "Ce login existe déjà"
        
        # Hash password
        password_hash = self.db.hash_password(password)
        
        # Insert user
        self.db.execute_query(
            """INSERT INTO utilisateurs (nom, login, mot_de_passe_hash, role, actif)
               VALUES (?, ?, ?, ?, 1)""",
            (nom, login, password_hash, role)
        )
        
        return True, "Utilisateur créé avec succès"
    
    def update_user(self, user_id: int, nom: str = None, login: str = None, 
                   role: str = None, actif: bool = None) -> tuple[bool, str]:
        """
        Update user information (admin only)
        Returns (success, message)
        """
        if not self.can_manage_users():
            return False, "Permission refusée"
        
        # Build update query dynamically
        updates = []
        params = []
        
        if nom:
            updates.append("nom = ?")
            params.append(nom)
        
        if login:
            # Check if login already exists for another user
            existing = self.db.fetch_one(
                "SELECT id FROM utilisateurs WHERE login = ? AND id != ?",
                (login, user_id)
            )
            if existing:
                return False, "Ce login existe déjà"
            updates.append("login = ?")
            params.append(login)
        
        if role:
            updates.append("role = ?")
            params.append(role)
        
        if actif is not None:
            updates.append("actif = ?")
            params.append(1 if actif else 0)
        
        if not updates:
            return False, "Aucune modification à effectuer"
        
        params.append(user_id)
        query = f"UPDATE utilisateurs SET {', '.join(updates)} WHERE id = ?"
        
        self.db.execute_query(query, params)
        
        return True, "Utilisateur mis à jour avec succès"
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> tuple[bool, str]:
        """
        Change user password
        Returns (success, message)
        """
        # Get user
        result = self.db.fetch_one(
            "SELECT * FROM utilisateurs WHERE id = ?",
            (user_id,)
        )
        
        if not result:
            return False, "Utilisateur non trouvé"
        
        # Verify old password (unless admin changing another user's password)
        if self.current_user and self.current_user.id != user_id and not self.current_user.est_admin:
            if not self.db.verify_password(old_password, result['mot_de_passe_hash']):
                return False, "Ancien mot de passe incorrect"
        
        # Hash new password
        new_password_hash = self.db.hash_password(new_password)
        
        # Update password
        self.db.execute_query(
            "UPDATE utilisateurs SET mot_de_passe_hash = ? WHERE id = ?",
            (new_password_hash, user_id)
        )
        
        return True, "Mot de passe changé avec succès"
    
    def get_all_users(self) -> list[models.Utilisateur]:
        """Get all users (admin only)"""
        if not self.can_manage_users():
            return []
        
        results = self.db.fetch_all("SELECT * FROM utilisateurs ORDER BY nom")
        
        users = []
        for result in results:
            user = models.Utilisateur(
                id=result['id'],
                nom=result['nom'],
                login=result['login'],
                mot_de_passe_hash=result['mot_de_passe_hash'],
                role=result['role'],
                actif=bool(result['actif']),
                date_creation=datetime.fromisoformat(result['date_creation']) if result['date_creation'] else None
            )
            users.append(user)
        
        return users
    
    def get_user_by_id(self, user_id: int) -> Optional[models.Utilisateur]:
        """Get user by ID"""
        result = self.db.fetch_one(
            "SELECT * FROM utilisateurs WHERE id = ?",
            (user_id,)
        )
        
        if not result:
            return None
        
        return models.Utilisateur(
            id=result['id'],
            nom=result['nom'],
            login=result['login'],
            mot_de_passe_hash=result['mot_de_passe_hash'],
            role=result['role'],
            actif=bool(result['actif']),
            date_creation=datetime.fromisoformat(result['date_creation']) if result['date_creation'] else None
        )


# Global auth service instance
auth_service = AuthService(database.db)
