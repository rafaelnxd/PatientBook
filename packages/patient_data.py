import json

def carregar_pacientes():
    try:
        with open("pacientes.json", "r", encoding="utf-8") as file:
            pacientes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver vazio, retorna uma lista vazia.
        pacientes = []
    return pacientes