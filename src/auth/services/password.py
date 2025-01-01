import bcrypt


class PasswordService:
    @staticmethod
    def hash_password(password: str):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password

    @staticmethod
    def check_password(password: str, hashed_password: str):
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
        return False