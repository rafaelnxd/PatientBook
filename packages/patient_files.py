import os

def salvar_exames(upload, paciente_nome):
    ## Cria o diretório "exames" se não existir
    if not os.path.exists("exames"):
        os.makedirs("exames")

    ## Define o caminho do arquivo
    path = os.path.join("exames", f"{paciente_nome}_exame.pdf")

    ## Salva o exame no arquivo
    with open(path, "wb") as f:
        f.write(upload.read())

def salvar_prescricao(upload, paciente_nome):
    path = os.path.join("prescricoes", f"{paciente_nome}_prescricao.pdf")
    with open(path, "wb") as f:
        f.write(upload.read())

def salvar_notas(nova_nota, paciente_nome):
    
    ## Define o caminho do arquivo
    path = os.path.join("notas", f"{paciente_nome}_nota.txt")

    ## Salva a nota no arquivo
    with open(path, "w", encoding="utf-8") as file:
        file.write(nova_nota)
