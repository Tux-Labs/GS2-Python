import requests
import os
import json
from time import sleep
from datetime import datetime

bairros = {
    "Zona Norte": ("Santana", "Tucuruvi", "Parada Inglesa", "Lauzane Paulista", "Vila Guilherme", "Jardim São Paulo"),
    "Zona Leste": ("Jardim Anália Franco", "Tatuapé", "Mooca", "Belém", "Vila Prudente", "Vila Formosa", "Vila Matilde", "Vila Antonieta", "Carrão"),
    "Zona Sul": ("Moema", "Ipiranga", "Paraíso", "Vila Nova Conceição", "Vila Mariana", "São Judas", "Jabaquara", "Morumbi", "Interlagos"),
    "Zona Oeste": ("Pinheiros", "Perdizes", "Vila Madalena", "Lapa", "Butantã", "Bara Funda", "Pirituba"),
    "Centro": ("Bela Vista", "República", "Higienópolis", "Sé", "Bom Retiro", "Cambuci", "Brás", "Consolação", "Liberdade")
}

alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

niveis = {
    "Normal": ("Quando ta de boa", "NORMAL"), 
    "Atenção": ("Quando o baguio ta sla", "ATENÇÃO"), 
    "Alerta": ("Quando o bagulho ta louco", "ALERTA"), 
    "Emergência": ("Segura tuas telha que hoje tua casa cai kk", "EMERGÊNCIA")
}

def limparTela():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    barra = "=========================="
    while True:
        limparTela()
        print(f"{barra}\n{"Projeto AquaSinal":^26}\n{barra}")
        print(f"1. Consultar riscos hoje\n2. Guia de segurança e rota (DURANTE)\n3. Guia de saúde pós-alagamento (DEPOIS)\n4. Registrar relato de alagamento\n5. Consultar relatos\n0. Sair")
        op = input("Digite a opção que você deseja acessar\n- ")
        if op == "1":
            clima(barra)
        if op == "2":
            guiaDurante(barra)
        if op == "3":
            guiaApos(barra)
        if op == "4":
            salvarRelatos(barra)
        if op == "5":
            visualisarRelatos(barra)
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
        return niveis[1][3]
    elif chuva >= 40:
        return niveis[1][2]
    elif chuva >= 20:
        return niveis[1][1]
    else:
        return niveis[1][0]

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
    print("1. Evite atravessar ruas, túneis e passagens alagadas.")
    print("2. Prefira rotas mais altas e sem degraus ou rampas alagadas.")
    print("3. Se estiver em ônibus ou metrô, siga as orientações da operadora.")
    print("4. Em emergência, ligue 193 (Bombeiros) ou 199 (Defesa Civil).")
    input("Digite algo para retornar: ")

def guiaApos(barra):
    limparTela()
    print(f"{barra}\n{"GUIA APÓS ENCHENTES":^26}\n{barra}")
    print("1. Não beba nem use água que tenha tido contato com a enchente.")
    print("2. Lave e desinfete objetos e superfícies atingidos pela água.")
    print("3. Evite contato com a água parada (risco de leptospirose).")
    print("4. Procure uma UBS ou UPA se tiver febre, dores no corpo ou ferimentos.")
    input("Digite algo para retornar: ")

#----------------------------------------------------------------------------------

def carregarRelatos():
    try:
        with open("relatos.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError as e:
        print(f"Arquivo não encontrado, começando com lista vazia. (Erro: {e})")
        return []
    except json.JSONDecodeError as e:
        print(f"Arquivo corrompido, começando com lista vazia. (Erro: {e})")
        return []

def registrarRelatos(relatos):
    with open("relatos.json", "w", encoding="utf-8") as arquivo:
        json.dump(relatos, arquivo)

def escolherZona(barra):
    while True:
            limparTela()
            print(f"{barra}\n{"Registrar Relato":^26}\n{barra}")
            for i in bairros.keys():
                print(i)
            escolhaZona = input("Digite a zona que seu bairro se localiza\n- ")
            resultado = ""
            letraAnteriorELetra = False
            for letra in escolhaZona:
                if letraAnteriorELetra:
                    resultado += letra.lower()
                else:
                    resultado += letra.upper()
                letraAnteriorELetra = letra in alfabeto
            escolhaZona = resultado
            if escolhaZona in bairros:
                return escolhaZona
            else:
                print("Zona não encontrada, digite uma das opções acima")
                sleep(2.5)

def escolherBairro(escolhaZona, barra):
    while True:
        limparTela()
        print(f"{barra}\n{"Registrar Relato":^26}\n{barra}")
        for bairro in bairros[escolhaZona]:
            print(bairro)
        escolhaBairro = input("Digite o bairro em que ocorreu o relato\n- ")
        resultado = ""
        letraAnteriorELetra = False
        for letra in escolhaBairro:
            if letraAnteriorELetra:
                resultado += letra.lower()
            else:
                resultado += letra.upper()
            letraAnteriorELetra = letra in alfabeto
        escolhaBairro = resultado
        if escolhaBairro == "":
            print("Bairro não encontrado, digite uma ds opções acima")
            sleep(2.5)
        elif escolhaBairro in bairros[escolhaZona]:
            return escolhaBairro
        else:
            print("Bairro não encontrado, digite uma das opções acima")
            sleep(2.5)

def salvarRelatos(barra):
    escolhaZona = escolherZona(barra)
    escolhaBairro = escolherBairro(escolhaZona, barra)
    limparTela()
    print(f"{barra}\n{"Registrar Relato":^26}\n{barra}")
    desc = ""
    while len(desc) < 5:
        desc = input("Descreva o local (Rua, Ponto de Refenrência, Etc.)(Min. 5 caracteres): ")
        if len(desc) < 5:
            print("Descrição muito curta\n")
    limparTela()
    print(f"{barra}\n{"Registrar Relato":^26}\n{barra}")
    for nivel in niveis:
        print(f"{nivel} ({niveis[nivel][0]})")
    nivel = input("\nDigite o nível que deseja incluir no relato: ")
    relatos = carregarRelatos()
    idRelato = len(relatos) + 1
    relato = {
        "id": idRelato,
        "bairro": escolhaBairro,
        "desc": desc,
        "nivel": nivel,
        "dataHora": datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }
    print(relato)
    relatos.append(relato)
    registrarRelatos(relatos)
    input()

def visualisarRelatos(barra):
    print(f"{barra}\n{"Visualisar Relatos":^26}\n{barra}")
    relatos = carregarRelatos()
    if len(relatos) == 0:
        print("Nenhum relato registrado ainda")
    for relato in relatos:
        print(f"Relato: {relato["id"]}, Bairro: {relato["bairro"]}, Descrição: {relato["desc"]}, Nível: {relato["nivel"]}, Data e Hora: {relato["dataHora"]}")
    input()

main()