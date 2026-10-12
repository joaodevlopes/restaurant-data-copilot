import requests
import sys
from datetime import datetime, timezone
from pathlib import Path

# Busca Via API
try:
    resposta = requests.get(
    "https://archive-api.open-meteo.com/v1/archive",
    params={
        "latitude" : -19.9167,
        "longitude" : -43.9345,
        "start_date" : "2026-01-01",
        "end_date" : "2026-06-30",
        
        "daily" : "temperature_2m_mean,temperature_2m_min,rain_sum,temperature_2m_max,precipitation_sum,weather_code",
        
        "timezone" : "America/Sao_Paulo"
        },
        timeout=30,
    )
    resposta.raise_for_status()
except requests.exceptions.Timeout:
    sys.exit("Erro: a API demorou mais de 30 segundos para responder.")
except requests.exceptions.ConnectionError:
    sys.exit("Erro: sem conexão com a API. Verifique a internte ou a URL")
except requests.exceptions.HTTPError as error: 
    sys.exit(f"Erro: a API respondeu com status {error.response.status_code}") 
    
    
# Monta caminho para mandar para a camada bronze

agora = datetime.now(timezone.utc)
data_extracao = agora.date().isoformat()
run_id = agora.strftime("%Y%m%dT%H%M%SZ")

pasta = Path("data") / "bronze" / "weather" / f"extracted_at={data_extracao}" / f"run_id={run_id}"
pasta.mkdir(parents=True, exist_ok=True)
arquivo = pasta / "weather.json"

#Gravar arquivo
try: 
    with open(arquivo, "xb") as f:
        f.write(resposta.content)
except FileExistsError:
    sys.exit(f"Erro: {arquivo} já existe. A bronze nunca subscreve") 

print("Salvo em:", arquivo, "| tamanho:", len(resposta.content), "bytes")

print("Status: ", resposta.status_code)

dados = resposta.json()
print("Dias: ", dados["daily"]["time"])

print("Temperatura média: ", dados["daily"]["temperature_2m_mean"])


print("Chuva em mm: ", dados["daily"]["rain_sum"])


