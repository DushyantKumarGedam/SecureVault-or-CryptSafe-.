from cryptography.fernet import Fernet

class EncryptionUtils:
    def __init__(self, key=None):
        self.key = key or Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, data):
        return self.cipher_suite.encrypt(data)

    def decrypt(self, token):
        return self.cipher_suite.decrypt(token)

# Example usage
# utils = EncryptionUtils()
# encrypted = utils.encrypt(b"Secret Data")
# print(encrypted)
# decrypted = utils.decrypt(encrypted)
# print(decrypted)
