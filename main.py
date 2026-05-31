"""
Main application entry point for HOUSE FADE BARBER SHOP Android
Kivy-based mobile application
"""

import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp

import config
import auth
import services

# Set window size for desktop testing
Window.size = (400, 700)


class LoginScreen(Screen):
    """Login screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Title
        title_label = Label(
            text=config.APP_NAME,
            font_size=dp(24),
            bold=True,
            size_hint_y=None,
            height=dp(80)
        )
        layout.add_widget(title_label)
        
        # Login input
        self.login_input = TextInput(
            hint_text='Login',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            font_size=dp(16)
        )
        layout.add_widget(self.login_input)
        
        # Password input
        self.password_input = TextInput(
            hint_text='Mot de passe',
            password=True,
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            font_size=dp(16)
        )
        layout.add_widget(self.password_input)
        
        # Login button
        login_button = Button(
            text='Se connecter',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(18),
            background_color=config.COLOR_SUCCESS
        )
        login_button.bind(on_press=self.login)
        layout.add_widget(login_button)
        
        # Error label
        self.error_label = Label(
            text='',
            color=config.COLOR_DANGER,
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(self.error_label)
        
        self.add_widget(layout)
    
    def login(self, instance):
        """Handle login"""
        login = self.login_input.text
        password = self.password_input.text
        
        if not login or not password:
            self.error_label.text = 'Veuillez remplir tous les champs'
            return
        
        success, message, user = auth.auth_service.login(login, password)
        
        if success:
            self.error_label.text = ''
            self.manager.current = 'dashboard'
        else:
            self.error_label.text = message


class DashboardScreen(Screen):
    """Dashboard screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'
        
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60))
        header_label = Label(
            text='Tableau de bord',
            font_size=dp(20),
            bold=True
        )
        header.add_widget(header_label)
        layout.add_widget(header)
        
        # Stats grid
        stats_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(200))
        
        # Get stats
        stats = services.report_service.get_dashboard_stats()
        
        # Stat items
        stat_items = [
            ('Clients', str(stats.total_clients)),
            ('Cartes actives', str(stats.total_cartes_actives)),
            ('Cartes bloquées', str(stats.total_cartes_bloquees)),
            ('Solde zéro', str(stats.total_cartes_solde_zero)),
            ('Recharges jour', str(stats.total_recharges_jour)),
            ('Débits jour', str(stats.total_debits_jour)),
            ('CA jour', f"{stats.chiffre_affaires_jour:,} {config.CURRENCY}"),
            ('CA mois', f"{stats.chiffre_affaires_mois:,} {config.CURRENCY}")
        ]
        
        for label, value in stat_items:
            stat_box = BoxLayout(orientation='vertical', padding=dp(5))
            stat_label = Label(text=label, font_size=dp(12), color=config.COLOR_DARK)
            stat_value = Label(text=value, font_size=dp(16), bold=True)
            stat_box.add_widget(stat_label)
            stat_box.add_widget(stat_value)
            stats_layout.add_widget(stat_box)
        
        layout.add_widget(stats_layout)
        
        # Action buttons
        actions_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(300))
        
        buttons = [
            ('Activer carte', config.COLOR_SUCCESS, 'activate_card'),
            ('Recharger carte', config.COLOR_SECONDARY, 'recharge_card'),
            ('Débiter coiffure', config.COLOR_WARNING, 'debit_card'),
            ('Gérer clients', config.COLOR_DARK, 'manage_clients'),
            ('Rapports', config.COLOR_DANGER, 'reports'),
        ]
        
        # Add user management button only for admins
        if auth.auth_service.can_manage_users():
            buttons.append(('Gérer utilisateurs', config.COLOR_PRIMARY, 'manage_users'))
        
        for text, color, screen_name in buttons:
            btn = Button(
                text=text,
                font_size=dp(14),
                background_color=color
            )
            btn.bind(on_press=lambda instance, s=screen_name: self.go_to_screen(s))
            actions_layout.add_widget(btn)
        
        layout.add_widget(actions_layout)
        
        # Logout button
        logout_button = Button(
            text='Déconnexion',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(16),
            background_color=config.COLOR_DANGER
        )
        logout_button.bind(on_press=self.logout)
        layout.add_widget(logout_button)
        
        self.add_widget(layout)
    
    def go_to_screen(self, screen_name):
        """Navigate to a screen"""
        self.manager.current = screen_name
    
    def logout(self, instance):
        """Handle logout"""
        auth.auth_service.logout()
        self.manager.current = 'login'


class ActivateCardScreen(Screen):
    """Card activation screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'activate_card'
        
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60))
        header_label = Label(
            text='Activer une carte',
            font_size=dp(20),
            bold=True
        )
        header.add_widget(header_label)
        layout.add_widget(header)
        
        # Back button
        back_button = Button(
            text='Retour',
            size_hint_y=None,
            height=dp(40)
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        """Go back to dashboard"""
        self.manager.current = 'dashboard'


class RechargeCardScreen(Screen):
    """Card recharge screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'recharge_card'
        
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60))
        header_label = Label(
            text='Recharger une carte',
            font_size=dp(20),
            bold=True
        )
        header.add_widget(header_label)
        layout.add_widget(header)
        
        # Back button
        back_button = Button(
            text='Retour',
            size_hint_y=None,
            height=dp(40)
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        """Go back to dashboard"""
        self.manager.current = 'dashboard'


class DebitCardScreen(Screen):
    """Card debit screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'debit_card'
        
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60))
        header_label = Label(
            text='Débiter une coiffure',
            font_size=dp(20),
            bold=True
        )
        header.add_widget(header_label)
        layout.add_widget(header)
        
        # Back button
        back_button = Button(
            text='Retour',
            size_hint_y=None,
            height=dp(40)
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        """Go back to dashboard"""
        self.manager.current = 'dashboard'


class ManageClientsScreen(Screen):
    """Client management screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'manage_clients'
        
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60))
        header_label = Label(
            text='Gérer les clients',
            font_size=dp(20),
            bold=True
        )
        header.add_widget(header_label)
        layout.add_widget(header)
        
        # Back button
        back_button = Button(
            text='Retour',
            size_hint_y=None,
            height=dp(40)
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        """Go back to dashboard"""
        self.manager.current = 'dashboard'


class ReportsScreen(Screen):
    """Reports screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'reports'
        
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60))
        header_label = Label(
            text='Rapports',
            font_size=dp(20),
            bold=True
        )
        header.add_widget(header_label)
        layout.add_widget(header)
        
        # Back button
        back_button = Button(
            text='Retour',
            size_hint_y=None,
            height=dp(40)
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        """Go back to dashboard"""
        self.manager.current = 'dashboard'


class ManageUsersScreen(Screen):
    """User management screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'manage_users'
        
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(60))
        header_label = Label(
            text='Gérer les utilisateurs',
            font_size=dp(20),
            bold=True
        )
        header.add_widget(header_label)
        layout.add_widget(header)
        
        # Back button
        back_button = Button(
            text='Retour',
            size_hint_y=None,
            height=dp(40)
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        """Go back to dashboard"""
        self.manager.current = 'dashboard'


class BarberShopApp(App):
    """Main application class"""
    
    def build(self):
        """Build the application"""
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(LoginScreen())
        sm.add_widget(DashboardScreen())
        sm.add_widget(ActivateCardScreen())
        sm.add_widget(RechargeCardScreen())
        sm.add_widget(DebitCardScreen())
        sm.add_widget(ManageClientsScreen())
        sm.add_widget(ReportsScreen())
        sm.add_widget(ManageUsersScreen())
        
        return sm


if __name__ == '__main__':
    BarberShopApp().run()
