# AquaSinal - CitizenTech de Enchente em São Paulo

Global Solution 2026.2 - FIAP - Engenharia de Software, 1º ano
Disciplina: Computational Thinking with Python

## Integrantes

- Eduardo de Abreu Gouvêa - RM 573414
- Felipe Roberto Cassiano - RM 569238
- Paulo Henrique Moreira Angueira - RM 573245
- Vinícius Mansur Magalhães - RM 571518

## Problema

Alagamentos recorrentes em São Paulo bloqueiam o caminho de quem se desloca todos os dias pelo centro expandido. Em 14/10/2026, por exemplo, uma forte chuva alagou o túnel do Vale do Anhangabaú e atingiu a estação Liberdade do metrô. Quem sai de casa nem sempre sabe quando a chuva vai bloquear o caminho, nem onde a comunidade já viu alagamentos.

## Solução

O **AquaSinal** é um programa de terminal em Python que acompanha o cidadão nas três etapas de uma enchente e reúne relatos da comunidade por bairro.

### Menu principal

| Opção | O que faz |
|---|---|
| 1. Consultar riscos hoje | **Antes:** busca a chuva prevista para hoje em São Paulo (Open-Meteo) e mostra o nível de risco |
| 2. Guia de segurança e rota | **Durante:** orientações de segurança e de rota acessível |
| 3. Guia de saúde pós-alagamento | **Depois:** cuidados com água, limpeza e doenças como a leptospirose |
| 4. Registrar relato de alagamento | Cadastra um relato por zona e bairro, com descrição e nível |
| 5. Consultar relatos | Lista todos os relatos salvos |
| 6. Analisar relatos | Painel com a pontuação dos bairros e das zonas |
| 0. Sair | Encerra o programa |

### Risco de chuva (opção 1)

A chuva do dia vem do Open-Meteo e é classificada em quatro níveis:

| Nível | Chuva do dia |
|---|---|
| Normal | menos de 20 mm |
| Atenção | 20 a 39 mm |
| Alerta | 40 a 69 mm |
| Emergência | 70 mm ou mais |

> Esses limites são **hipóteses didáticas da equipe**, não limites oficiais do CGE.

Se não houver internet, a consulta demorar demais (timeout) ou a API devolver um erro, o programa mostra a mensagem de erro e volta ao menu.

### Relatos da comunidade (opções 4 e 5)

Para registrar um relato, o usuário informa:

1. a **zona** (Zona Norte, Zona Leste, Zona Sul, Zona Oeste ou Centro);
2. o **bairro**, dentre os 40 da lista (a maiúscula e a minúscula são ajustadas automaticamente);
3. uma **descrição do local** (rua ou ponto de referência), com no mínimo 5 caracteres;
4. o **nível** observado: Normal, Atenção, Alerta ou Emergência.

Cada relato é salvo em `relatos.json` com id, bairro, descrição, nível, data e hora. Entradas inválidas são recusadas e o programa pede a informação de novo.

### Análise dos relatos (opção 6)

O painel mostra quais bairros estão mais afetados. É possível ver uma zona específica (com seus bairros) ou o ranking de todas as zonas.

Cada relato vale pontos conforme o nível:

| Nível | Pontos |
|---|---|
| Normal | 0 |
| Atenção | 1 |
| Alerta | 2 |
| Emergência | 3 |

O painel soma os pontos dos relatos de cada bairro (e de cada zona), ordena do maior para o menor e mostra uma barra, a pontuação e a quantidade de relatos. Bairros sem relatos aparecem como "sem relatos". Todos os relatos válidos entram na conta, sem limite de tempo.

## Regras de negócio

- Os relatos falam apenas sobre o **local**. O programa avisa que o relato é anônimo e que não se deve informar dados pessoais.
- Não há dados pessoais reais no projeto.
- O nível do relato e o bairro são validados. Relatos com nível ou bairro inválidos no arquivo são ignorados na análise.
- Os limites de chuva (20, 40 e 70 mm) são hipóteses didáticas, não oficiais.

## Conceitos de Python utilizados

- Menu de opções com `match/case`
- Validação de entradas com `while` e `if/elif/else`
- Tratamento de exceções com `try/except` (consulta à API e leitura do arquivo JSON)
- Estruturas de repetição `while` e `for`
- Funções com parâmetros e retorno
- Tuplas (bairros de cada zona), dicionários (zonas, níveis, pesos e relatos) e listas (relatos)
- Persistência em JSON (leitura e gravação)
- Consumo de API externa com `requests`
- Bibliotecas padrão: `os`, `json`, `time` e `datetime`

## Pré-requisitos

- Python 3.10 ou superior (por causa do `match/case`)
- Biblioteca `requests`

## Instalação e execução

```bash
pip install requests
python main.py
```

O arquivo `relatos.json` é criado automaticamente quando o primeiro relato é salvo.

## Limitações

- A previsão depende de internet e da API do Open-Meteo.
- O painel depende de relatos de usuários, que não são verificados por outras pessoas.
- O nível de chuva do dia usa só o total previsto, sem a intensidade hora a hora.
- A localização dos relatos é por bairro, sem mapa.

## Próximos passos

Mapa de alagamentos, confirmação dos relatos pela comunidade, informações de unidades de saúde próximas, sensor de nível de água conectado e parceria com a Defesa Civil.

## Fonte dos dados

Chuva: [Open-Meteo](https://open-meteo.com) (uso não comercial, licença CC-BY).

## ODS

- ODS 03: saúde e bem-estar
- ODS 11: cidades e comunidades sustentáveis
- ODS 13: ação contra a mudança do clima
- ODS 10: redução das desigualdades

## Arquivos do projeto

- `main.py`: código-fonte
- `relatos.json`: criado automaticamente ao registrar relatos