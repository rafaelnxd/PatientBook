import json

# Função para carregar os pacientes do arquivo pacientes.json

def carregar_pacientes():
    try:
        with open("pacientes.json", "r", encoding="utf-8") as file:
            pacientes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pacientes = []
    return pacientes