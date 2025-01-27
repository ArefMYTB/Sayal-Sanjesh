import hashlib


class Hashing:
    salt = "#mara*&^CheshmIst!KhonAfshan?_"

    def get_password_string(self, password):
        # password = password + self.salt
        # password = password.encode('utf-8')
        # hash_password = hashlib.sha256(password).hexdigest()
        hash_password = password
        return hash_password
