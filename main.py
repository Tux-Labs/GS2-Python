import requests
import os

def limparTela():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    barra = "=========================="
    while True:
        limparTela()
        print(f"{barra}\n{"NOME DO PROJETO SLA OQ":^26}\n{barra}")
        print(f"1. Consultar riscos hoje\n2. Guia de segurança e rota (DURANTE)\n3. Guia de saúde pós-alagamento (DEPOIS)\n4. Registrar relato de alagamento\n5. Consultar relatos\n0. Sair")
        print("Digite oq vc quer acessar ai bro:")
        op = input("- ")
        if op == "1":
            clima(barra)
        if op == "2":
            guiaDurante(barra)
        if op == "3":
            guiaApos(barra)
        if op == "0":
            return


def buscarClima(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "daily": "precipitation_sum,precipitation_hours", "timezone": "America/Sao_Paulo", "forecast_days": 1}
    try: 
        resposta = requests.get(url, params=params, timeout=10)
        dic = resposta.json()
    except requests.exceptions.Timeout as e:
        print(f"Erro ao buscar o clima. (Erro: {e})")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Sem conexão com a internet. (Erro: {e})")
        return None
    except Exception as e:
        print(f"Erro ao buscar o clima. (Erro: {e})")
        return None

    chuva = dic["daily"]["precipitation_sum"]
    horas = dic["daily"]["precipitation_hours"]
    
    return chuva, horas

def nivelChuva(chuva):
    if chuva >= 70:
        return "EMERGÊNCIA"
    elif chuva >= 40:
        return "ALERTA"
    elif chuva >= 20:
        return "ATENÇÃO"
    else:
        return "NORMAL"

def clima(barra):
    limparTela()
    resultado = buscarClima(-23.5505, -46.6333)
    chuva = resultado[0][0]
    horas = resultado[1][0]
    print(f"{barra}\n{"RISCO DE CHUVA HOJE":^26}\n{barra}")
    print(f"Chuva prevista para hoje: {chuva} mm")
    print(f"Horas com chuva hoje: {horas} h")
    print(f"Nível: {nivelChuva(chuva)}")
    input("Digite algo para retornar: ")

def guiaDurante(barra):
    limparTela()
    print(f"{barra}\n{"GUIA DURANTE ENCHENTES":^26}\n{barra}")
    print("Evite atravessar ruas, túneis e passagens alagadas.")
    print("Prefira rotas mais altas e sem degraus ou rampas alagadas.")
    print("Se estiver em ônibus ou metrô, siga as orientações da operadora.")
    print("Em emergência, ligue 193 (Bombeiros) ou 199 (Defesa Civil).")

def guiaApos(barra):
    limparTela()
    print(f"{barra}\n{"GUIA APOS ENCHENTES":^26}\n{barra}")
    print("Não beba nem use água que tenha tido contato com a enchente.")
    print("Lave e desinfete objetos e superfícies atingidos pela água.")
    print("Evite contato com a água parada (risco de leptospirose).")
    print("Procure uma UBS ou UPA se tiver febre, dores no corpo ou ferimentos.")

def salvarRelatos():
    print()

def visualizarRelatos():
    print()

main()