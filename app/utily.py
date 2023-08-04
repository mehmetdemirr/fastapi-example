from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verifiy(plain_password,hashed_password):
    pas=hash(plain_password)
    if pas == hashed_password:
        return True
    return False