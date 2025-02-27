import base64
import hashlib
import json
import requests
from Crypto.Cipher import AES
from urllib.parse import quote, unquote

class StringHelpers:
    QUERY_STRING_DELIMITER = '&'
    IV = bytes([0] * 16)
    
    def __init__(self, key_string):
        self.key = hashlib.sha256(key_string.encode('utf-8')).digest()
    
    def encrypt(self, unencrypted_string):
        cipher = AES.new(self.key, AES.MODE_CBC, self.IV)
        padded_data = self._pad(unencrypted_string)
        encrypted_bytes = cipher.encrypt(padded_data.encode('utf-8'))
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    
    def decrypt(self, encrypted_string):
        if encrypted_string.strip():
            encrypted_bytes = base64.b64decode(encrypted_string)
            cipher = AES.new(self.key, AES.MODE_CBC, self.IV)
            decrypted_bytes = cipher.decrypt(encrypted_bytes)
            return self._unpad(decrypted_bytes.decode('utf-8'))
        return ""
    
    def _pad(self, s):
        pad_length = 16 - (len(s) % 16)
        return s + (chr(pad_length) * pad_length)
    
    def _unpad(self, s):
        return s[:-ord(s[-1])]
