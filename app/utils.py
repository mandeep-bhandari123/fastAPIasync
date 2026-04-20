from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password):
  return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
  return password_hash.verify(plain_password, hashed_password)

''' 

from passlib.context import CryptContext

pwt_content = CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash(password:str):
    return pwt_content.hash(password)

def verify(given_password, real_password):
    return pwt_content.verify(given_password, real_password)
    


'''
