import requests
import sys
from pathlib import Path
from datetime import datetime, timezone

url = "https://brasilapi.com.br/api/feriados/v1/2026"

try:
    resposta = requests.get(url, headers = {"User-Agent": "restaurant_data_copilot/0.1(+https://github.com/joaodevlopes/restaurant-data-copilot)"},
                            timeout= 30
    )
    print(resposta.request.headers)
    resposta.raise_for_status()
    resposta_json = resposta.json()
except requests.exceptions.Timeout:
    sys.exit("Erro: a API demorou mais de 30 segundos para responder.")
except requests.exceptions.ConnectionError:
    sys.exit("Erro: sem conexão com a API. Verifique a internte ou a URL")
except requests.exceptions.HTTPError as error: 
    sys.exit(f"Erro: a API respondeu com status {error.response.status_code}") 
    
    
# Monta caminho para mandar para a camada bronze
data = datetime.now(timezone.utc)
data_extracao = data.date().isoformat()
run_id = data.strftime("%Y%m%dT%H%M%SZ")
pasta = Path("data")/("bronze")/("holidays")/f"extracted_at={data_extracao}"/f"run_id={run_id}"

pasta.mkdir(parents=True, exist_ok=True)
arquivo = pasta/"holidays.json"

#gravar arquivo
try: 
    with open(arquivo, "xb") as f:
        f.write(resposta.content)
except FileExistsError:
    sys.exit(f"Erro: {arquivo} já existe. A bronze nunca subscreve") 
    
print(f"Salvo em {arquivo} | tamanho: {len(resposta.content)} bytes " )

print("Status: ", resposta.status_code)
    
print(resposta_json)
    
