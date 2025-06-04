from passlib.context import CryptContext
passwd_context=CryptContext(
    schemes=["bcrypt"]
)


def generate_phash(password:str)->str: #type:ignore
    hash=passwd_context.hash(password)
    return hash

def verify_Passw(password:str,hash:str)->bool:
    return passwd_context.verify(password,hash)