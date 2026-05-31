"""
NFC Handler for HOUSE FADE BARBER SHOP Android
Handles NFC card reading on Android devices
"""

from kivy.utils import platform
from typing import Optional, Callable
import config


class NFCReader:
    """NFC card reader for Android"""
    
    def __init__(self):
        self.nfc_enabled = False
        self.callback: Optional[Callable] = None
        self._setup_nfc()
    
    def _setup_nfc(self):
        """Setup NFC based on platform"""
        if platform == 'android':
            try:
                from jnius import autoclass
                from android import activity
                from android.permissions import request_permissions, Permission
                
                # Request NFC permission
                request_permissions([Permission.NFC])
                
                # Get NFC adapter
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                NfcAdapter = autoclass('android.nfc.NfcAdapter')
                
                current_activity = PythonActivity.mActivity
                self.nfc_adapter = NfcAdapter.getDefaultAdapter(current_activity)
                
                if self.nfc_adapter:
                    self.nfc_enabled = True
                    print("NFC enabled")
                else:
                    print("NFC not available on this device")
                    
            except Exception as e:
                print(f"Error setting up NFC: {e}")
                self.nfc_enabled = False
        else:
            # Desktop simulation
            print("Running on desktop - NFC simulation mode")
            self.nfc_enabled = False
    
    def set_callback(self, callback: Callable):
        """Set callback for NFC tag detection"""
        self.callback = callback
    
    def read_card(self, timeout: int = config.NFC_READER_TIMEOUT) -> Optional[str]:
        """
        Read NFC card UID
        Returns the UID as a string, or None if failed
        """
        if platform == 'android' and self.nfc_enabled:
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                
                current_activity = PythonActivity.mActivity
                intent = current_activity.getIntent()
                
                if intent and intent.getAction():
                    from jnius import cast
                    NfcAdapter = autoclass('android.nfc.NfcAdapter')
                    
                    if intent.getAction() == NfcAdapter.ACTION_NDEF_DISCOVERED or \
                       intent.getAction() == NfcAdapter.ACTION_TAG_DISCOVERED or \
                       intent.getAction() == NfcAdapter.ACTION_TECH_DISCOVERED:
                        
                        tag = intent.getParcelableExtra(NfcAdapter.EXTRA_TAG)
                        if tag:
                            # Get UID from tag
                            uid_bytes = tag.getId()
                            uid_hex = ''.join(format(b, '02X') for b in uid_bytes)
                            return uid_hex.lower()
                
                return None
                
            except Exception as e:
                print(f"Error reading NFC card: {e}")
                return None
        else:
            # Desktop simulation - return None (will need manual input)
            return None
    
    def is_nfc_available(self) -> bool:
        """Check if NFC is available"""
        return self.nfc_enabled
    
    def enable_foreground_dispatch(self):
        """Enable foreground dispatch for NFC"""
        if platform == 'android' and self.nfc_enabled:
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                NfcAdapter = autoclass('android.nfc.NfcAdapter')
                PendingIntent = autoclass('android.app.PendingIntent')
                Intent = autoclass('android.content.Intent')
                IntentFilter = autoclass('android.content.IntentFilter')
                
                current_activity = PythonActivity.mActivity
                
                # Create intent for NFC
                intent = Intent(current_activity, current_activity.getClass())
                intent.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
                pending_intent = PendingIntent.getActivity(
                    current_activity, 0, intent, 0
                )
                
                # Create intent filters
                intent_filters = []
                ndef_tech = IntentFilter(NfcAdapter.ACTION_NDEF_DISCOVERED)
                ndef_tech.addDataType("*/*")
                intent_filters.append(ndef_tech)
                
                tag_tech = IntentFilter(NfcAdapter.ACTION_TAG_DISCOVERED)
                intent_filters.append(tag_tech)
                
                tech_tech = IntentFilter(NfcAdapter.ACTION_TECH_DISCOVERED)
                intent_filters.append(tech_tech)
                
                # Enable foreground dispatch
                tech_lists = [[]]
                self.nfc_adapter.enableForegroundDispatch(
                    current_activity, pending_intent, intent_filters, tech_lists
                )
                
                print("Foreground dispatch enabled")
                
            except Exception as e:
                print(f"Error enabling foreground dispatch: {e}")
    
    def disable_foreground_dispatch(self):
        """Disable foreground dispatch for NFC"""
        if platform == 'android' and self.nfc_enabled:
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                
                current_activity = PythonActivity.mActivity
                self.nfc_adapter.disableForegroundDispatch(current_activity)
                
                print("Foreground dispatch disabled")
                
            except Exception as e:
                print(f"Error disabling foreground dispatch: {e}")


# Global NFC reader instance
nfc_reader = NFCReader()
