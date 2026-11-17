import requests
import os
import json
from time import sleep
from datetime import datetime

bairros = {
    "Zona Norte": ("Santana", "Tucuruvi", "Parada Inglesa", "Lauzane Paulista", "Vila Guilherme", "Jardim São Paulo"),
    "Zona Leste": ("Jardim Anália Franco", "Tatuapé", "Mooca", "Belém", "Vila Prudente", "Vila Formosa", "Vila Matilde", "Vila Antonieta", "Carrão"),
    "Zona Sul": ("Moema", "Ipiranga", "Paraíso", "Vila Nova Conceição", "Vila Mariana", "São Judas", "Jabaquara", "Morumbi", "Interlagos"),
    "Zona Oeste": ("Pinheiros", "Perdizes", "Vila Madalena", "Lapa", "Butantã", "Barra Funda", "Pirituba"),
    "Centro": ("Bela Vista", "República", "Higienópolis", "Sé", "Bom Retiro", "Cambuci", "Brás", "Consolação", "Liberdade")
}

alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digitos = "123567890¹²³⁴⁵⁶⁷⁸⁹⁰"

niveis = {
    "Normal": ("Chuva Leve", "NORMAL"),
    "Atenção": ("Chuva Acentuada", "ATENÇÃO"),
    "Alerta": ("Chuva Muito Forte", "ALERTA"),
    "Emergência": ("Tempestade com raios, granizo ou alagamentos", "EMERGÊNCIA")
}

pesos = {"Normal": 0, "Atenção": 1, "Alerta": 2, "Emergência": 3}

def limparTela():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    barra = "=========================="
    while True:
        limparTela()
        print(f"{barra}\n{'Projeto AquaSinal':^26}\n{barra}")
        print(f"1. Consultar riscos hoje\n2. Guia de segurança e rota (DURANTE)\n3. Guia de saúde pós-alagamento (DEPOIS)\n4. Registrar relato de alagamento\n5. Consultar relatos\n6. Analisar relatos\n0. Sair")
        op = input("Digite a opção que você deseja acessar\n- ")
        match op:
            case "1":
                clima(barra)
            case "2":
                guiaDurante(barra)
            case "3":
                guiaApos(barra)
            case "4":
                salvarRelatos(barra)
            case "5":
                visualisarRelatos(barra)
            case "6":
                analisarRelatos(barra)
            case "0":
                return
            case _:
                print("Opção Inválida")
                sleep(1)


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
        return niveis["Emergência"][1]
    elif chuva >= 40:
        return niveis["Alerta"][1]
    elif chuva >= 20:
        return niveis["Atenção"][1]
    else:
        return niveis["Normal"][1]

def keyNivel(texto):
    for key in niveis:
        if key.upper() == str(texto).upper():
            return key
    return None

def clima(barra):
    limparTela()
    resultado = buscarClima(-23.5505, -46.6333)
    chuva = resultado[0][0]
    horas = resultado[1][0]
    print(f"{barra}\n{'RISCO DE CHUVA HOJE':^26}\n{barra}")
    print(f"Chuva prevista para hoje: {chuva} mm")
    print(f"Horas com chuva hoje: {horas} h")
    print(f"Nível: {nivelChuva(chuva)}")
    input("Digite algo para retornar: ")

def guiaDurante(barra):
    limparTela()
    print(f"{barra}\n{'GUIA DURANTE ENCHENTES':^26}\n{barra}")
    print("1. Evite atravessar ruas, túneis e passagens alagadas.")
    print("2. Prefira rotas mais altas e sem degraus ou rampas alagadas.")
    print("3. Se estiver em ônibus ou metrô, siga as orientações da operadora.")
    print("4. Em emergência, ligue 193 (Bombeiros) ou 199 (Defesa Civil).")
    input("Digite algo para retornar: ")

def guiaApos(barra):
    limparTela()
    print(f"{barra}\n{'GUIA APÓS ENCHENTES':^26}\n{barra}")
    print("1. Não beba nem use água que tenha tido contato com a enchente.")
    print("2. Lave e desinfete objetos e superfícies atingidos pela água.")
    print("3. Evite contato com a água parada (risco de leptospirose).")
    print("4. Procure uma UBS ou UPA se tiver febre, dores no corpo ou ferimentos.")
    input("Digite algo para retornar: ")

#----------------------------------------------------------------------------------

def carregarRelatos():
    try:
        with open("relatos.json", "r", encoding="UTF-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print(f"Arquivo não encontrado, começando com lista vazia.")
        return []
    except json.JSONDecodeError:
        print(f"Arquivo corrompido, começando com lista vazia.")
        return []

def registrarRelatos(relatos):
    with open("relatos.json", "w", encoding="UTF-8") as arquivo:
        json.dump(relatos, arquivo)

def escolherZona(barra):
    while True:
            limparTela()
            print(f"{barra}\n{'Registrar Relato':^26}\n{barra}")
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
        print(f"{barra}\n{'Registrar Relato':^26}\n{barra}")
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
    print(f"{barra}\n{'Registrar Relato':^26}\n{barra}")
    desc = ""
    while len(desc) < 5:
        desc = input("Descreva o local (Rua, Ponto de Refenrência, Etc.)(Min. 5 caracteres): ")
        if len(desc) < 5:
            print("Descrição muito curta\n")
    limparTela()
    print(f"{barra}\n{'Registrar Relato':^26}\n{barra}")
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
    print("Relato salvo com sucesso!")
    relatos.append(relato)
    registrarRelatos(relatos)
    input("Digite algo para voltar: ")

def visualisarRelatos(barra):
    print(f"{barra*3}\n{'Visualisar Relatos':^78}\n{barra*3}")
    relatos = carregarRelatos()
    if len(relatos) == 0:
        print("Nenhum relato registrado ainda")
    for relato in relatos:
        print(f"#{relato['id']} | {relato['dataHora']} | {relato['bairro']:^10} | Nível: {relato['nivel']} | Descrição: {relato['desc']}")
    input("Digite algo para voltar: ")

#----------------------------------------------------------------

def relatosValidos(relatos):
    validos = []
    for relato in relatos:
        try:
            nivel = keyNivel(relato["nivel"])
            bairro = relato["bairro"]
        except (KeyError, TypeError):
            continue
        if nivel != None:
            validos.append({"bairro": bairro, "nivel": nivel})
    return validos


def pontuarBairros(relatos):
    resultado = {}
    for zona in bairros:
        for bairro in bairros[zona]:
            resultado[bairro] = {"pontos": 0, "qtd": 0, "pior": None}
    for relato in relatos:
        if relato["bairro"] in resultado:
            dados = resultado[relato["bairro"]]
            dados["pontos"] += pesos[relato["nivel"]]
            dados["qtd"] += 1
            if dados["pior"] is None or pesos[relato["nivel"]] > pesos[dados["pior"]]:
                dados["pior"] = relato["nivel"]
    return resultado

def somarZona(pontuacao, zona):
    total = {"pontos": 0, "qtd": 0, "pior": None}
    for bairro in bairros[zona]:
        dados = pontuacao[bairro]
        total["pontos"] += dados["pontos"]
        total["qtd"] += dados["qtd"]
        if dados["pior"] is not None:
            if total["pior"] is None or pesos[dados["pior"]] > pesos[total["pior"]]:
                total["pior"] = dados["pior"]
    return total

def montarLinha(nome, dados, largura):
    if dados["qtd"] == 0:
        return f"{nome:<{largura}} · sem relatos"
    tamanho = min(dados["pontos"], 20)
    if tamanho == 0:
        tamanho = 1  # relatos "Normal" valem 0 pontos, mas a barra mostra que existem
    espaco = " " * (20 - tamanho)  # alinha as colunas seguintes
    barraGrafica = f"{'█' * tamanho}{espaco}"
    return f"{nome:<{largura}} {barraGrafica} {dados['pontos']:>3} pts | {dados['qtd']} relato(s)"

def chaveOrdem(item):
    return (-item[1]["pontos"], item[0])

def mostrarTodosZona(barra):
    print(f"{barra}\n{'Visão Geral'}\n{barra}")
    pontuacao = pontuarBairros(relatosValidos(carregarRelatos()))
    totais = {}
    for zona in bairros:
        totais[zona] = somarZona(pontuacao, zona)
    limparTela()
    print(f"{barra}\n{'Análise Todas as Zonas':^26}\n{barra}")
    for zona, dados in sorted(totais.items(), key=chaveOrdem):
        print(montarLinha(zona, dados, 12))
    print(f"pesos: {pesos}")
    input("Digite algo para voltar: ")

def mostrarZona(barra, zona):
    pontuacao = pontuarBairros(relatosValidos(carregarRelatos()))
    limparTela()
    titulo = "Análise " + zona
    print(f"{barra}\n{titulo:^26}\n{barra}")
    daZona = {}
    for bairro in bairros[zona]:
        daZona[bairro] = pontuacao[bairro]
    for bairro, dados in sorted(daZona.items(), key=chaveOrdem):
        print(montarLinha(bairro, dados, 20))
    print(f"pesos: {pesos}")
    input("Digite algo para voltar: ")

def analisarRelatos(barra):
    zonas = list(bairros.keys())
    while True:
        limparTela()
        print(f"{barra}\n{'Analisar Relatos':^26}\n{barra}")
        print("1. Zona Norte\n2. Zona Leste\n3. Zona Sul\n4. Zona Oeste\n5. Centro\n6. Todas as Zonas\n0. Sair")
        op = input("Digite a opção que deseja acessar\n- ")
        if op == "6":
            mostrarTodosZona(barra)
        elif op in digitos and 1 <= int(op) <= len(zonas):
            mostrarZona(barra, zonas[int(op) - 1])
        elif op == "0":
            return
        else:
            print("Opção inválida")
            sleep(1.5)

main()