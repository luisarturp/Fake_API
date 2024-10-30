from faker import Faker
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

app = FastAPI()
fake = Faker()

API_TOKEN = "Sicredi123"

# Configuração de segurança
security = HTTPBearer()

# Função de verificação do token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

# cria rota do home
@app.get('/')
def home():
    return {'msg': 'Ola Sicredi'}

# Função para gerar as informações (com autenticação)
@app.get('/fake-user-data')
def get_users(count: int = 1, _: HTTPAuthorizationCredentials = Depends(verify_token)) -> List[dict]:
    # Gerar uma lista de usuários com base no parâmetro count
    users = []
    for _ in range(count):
        user = {
            'first name': fake.first_name(),
            #'last name': fake.last_name(),
            #'username': fake.user_name(),
            #'email': fake.email(),
        }
        users.append(user)
    
    return users