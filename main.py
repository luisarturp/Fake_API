import requests
import pandas as pd
import Levenshtein

def buscar_nomes(api_url, count=10, token="Sicredi123"):
    # Define os cabeçalhos com o token de autenticação
    headers = {
        "Authorization": f"Bearer {token}"
    }
    # Faz a requisição para a API buscar os nomes com o token
    response = requests.get(f"{api_url}?count={count}", headers=headers)
    response.raise_for_status()  # Levanta uma exceção se a resposta tiver um erro
    dados = response.json()
    # Extrai apenas os nomes dos usuários
    nomes = [user["first name"] for user in dados]
    return nomes

def calcular_distancia_levenshtein(nomes):
    # Define o primeiro nome como origem
    nome_origem = nomes[0]
    # Calcula a distância de Levenshtein entre o nome de origem e os outros nomes
    distancias = [(nome, Levenshtein.distance(nome_origem, nome)) for nome in nomes[1:]]
    # Ordena os nomes com base na distância
    distancias_ordenadas = sorted(distancias, key=lambda x: x[1])
    return distancias_ordenadas

def main():
    # URL da API
    api_url = "http://127.0.0.1:8000/fake-user-data"
    # Token de autenticação 
    token = "Sicredi123"
    
    try:
        # Passo 1: Buscar nomes
        nomes = buscar_nomes(api_url, count=10, token=token)
        
        # Passo 2: Calcular distâncias de Levenshtein
        distancias_ordenadas = calcular_distancia_levenshtein(nomes)
        
        # Passo 3: Exibir o resultado em um DataFrame
        df = pd.DataFrame(distancias_ordenadas, columns=["Nome", "Distância para origem"])
        print(df)
    
    except requests.RequestException as e:
        print("Erro ao acessar a API:", e)

# Executa a função principal
main()
