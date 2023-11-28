import os
import fitz
import streamlit as st

def salvar_exames(upload, paciente_nome):
    ## Cria o diretório exames se não existir
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

def mostrar_pdf_exames_sangue(selected_patient):
    ## Caminho para o arquivo PDF de exames de sangue do paciente selecionado
    path = os.path.join("sangue", f"{selected_patient}_exame.pdf")

    ## Verifica se o arquivo PDF existe
    if os.path.exists(path):
        pdf_doc = fitz.open(path)

        for page_num in range(pdf_doc.page_count):
            page = pdf_doc[page_num]
            image_bytes = page.get_pixmap().tobytes()

            st.image(image_bytes, use_column_width=True)

        pdf_doc.close()
    else:
        st.warning("PDF não encontrado.")