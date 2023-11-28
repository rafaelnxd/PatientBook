from .patient_data import carregar_pacientes
from .patient_files import salvar_exames, salvar_prescricao, salvar_notas
import streamlit as st
import json
from datetime import datetime, timedelta
import os
import fitz


def show_pacientes(pacientes):
    st.subheader("Lista de Pacientes")

    ## Mostra o nome dos pacientes como uma lista
    selected_patient = st.selectbox("Selecione um paciente: ", [paciente["Nome"] for paciente in pacientes])

    ## Mostra a ficha do paciente
    if selected_patient:
        paciente = next((p for p in pacientes if p["Nome"] == selected_patient), None)
        if paciente:
            st.write("Nome: ", paciente["Nome"])
            st.write("Idade: ", paciente["Idade"])
            st.write("Endereço: ", paciente["Endereço"])
            st.write("Convênio: ", paciente["Convenio"])
            st.write("Doenças Preexistentes: ", ", ".join(paciente["Doenças Preexistentes"]))
            st.write("Tipo Sanguíneo:", paciente.get("Tipo Sanguíneo", "Não informado"))

             ## Formata e mostra a Próxima Consulta
            proxima_consulta = paciente.get("Próxima Consulta", "Sem consulta marcada")
            st.write("Próxima Consulta:", formatar_proxima_consulta(proxima_consulta))
            
           
            ## Mostra o histórico médico
            with st.expander("Histórico de Consultas"):
                show_historico_paciente(paciente)

            with st.expander("Exame de Sangue"):
                mostrar_pdf_exames_sangue(selected_patient)

            ## Mostra a edição de paciente
            editar_expander = st.expander("Editar Informações do Paciente")
            show_editar_paciente(editar_expander, pacientes, selected_patient)
              
def show_notas_paciente(pacientes):
    st.subheader("Notas para o Paciente")

    ## Mostra o nome dos pacientes como uma lista
    selected_patient = st.selectbox("Selecione um paciente: ", [paciente["Nome"] for paciente in pacientes])

    ## Mostra a aba de notas para o paciente selecionado
    if selected_patient:
        paciente = next((p for p in pacientes if p["Nome"] == selected_patient), None)
        if paciente:
            st.write("Nome: ", paciente["Nome"])
            st.write("Idade: ", paciente["Idade"])

             ## Formata e mostra a Próxima Consulta
            proxima_consulta = paciente.get("Próxima Consulta", "Sem consulta marcada")
            st.write("Próxima Consulta:", formatar_proxima_consulta(proxima_consulta))

            # Adiciona as notas para o paciente
            st.subheader("Recomendações Médicas: ")
            nova_nota = st.text_area("Digite o seu comentário:", key=f"nota_{selected_patient}")
            adicionar_nota = st.button("Adicionar Nota", key=f"btn_nota_{selected_patient}")

            if adicionar_nota and nova_nota:
                paciente["Notas"] = paciente.get("Notas", []) + [nova_nota]
                salvar_notas(nova_nota, selected_patient)  # Salva a nota na pasta "notas"
                st.success("Nota adicionada com sucesso!")

            ## Adiciona upload de prescrição
            st.subheader("Fazer Upload de Prescrição: ")
            prescricao_upload = st.file_uploader("Selecione o arquivo:", key=f"prescricao_{selected_patient}")
            if prescricao_upload:
                salvar_prescricao(prescricao_upload, selected_patient)
                st.success("Prescrição enviada com sucesso!")

            ## Adiciona upload de exames
            st.subheader("Fazer Upload de Exames: ")
            exames_upload = st.file_uploader("Selecione o arquivo:", key=f"exames_{selected_patient}")
            if exames_upload:
                salvar_exames(exames_upload, selected_patient)
                st.success("Exames enviados com sucesso!")

            ## Mostra as notas do paciente
            # notas = paciente.get("Notas", [])
            # if notas:
            #     st.subheader("Notas: " )
            #     for nota in notas:
            #         st.write(nota)

def show_editar_paciente(expander, pacientes, selected_patient):
    ## Mostra o formulário para editar as informações do paciente selecionado dentro do expander
    with expander:
        if selected_patient:
            paciente = next((p for p in pacientes if p["Nome"] == selected_patient), None)
            if paciente:
                st.write("Nome: ", paciente["Nome"])
                idade = st.number_input("Idade: ", value=paciente["Idade"])
                endereco = st.text_input("Endereço: ", value=paciente["Endereço"])
                convenio = st.text_input("Convênio: ", value=paciente["Convenio"])
                doencas_preexistentes = st.text_input("Doenças Preexistentes: ", value=", ".join(paciente["Doenças Preexistentes"]))
            


                ## Atualiza as informações do paciente no dicionário
                paciente["Idade"] = idade
                paciente["Endereço"] = endereco
                paciente["Convenio"] = convenio
                paciente["Doenças Preexistentes"] = [d.strip() for d in doencas_preexistentes.split(",")]

                ## Salva as alterações no arquivo pacientes.json
                with open("pacientes.json", "w", encoding="utf-8") as file:
                    json.dump(pacientes, file, indent=4)

def show_marcar_consulta(pacientes):
    st.subheader("Marcar Consulta")

    ## Mostra o nome dos pacientes como uma lista
    selected_patient = st.selectbox("Selecione um paciente: ", [paciente["Nome"] for paciente in pacientes])

    ## Mostra o formulário para marcar a consulta para o paciente selecionado
    if selected_patient:    
        paciente = next((p for p in pacientes if p["Nome"] == selected_patient), None)
        if paciente:
            st.write("Nome: ", paciente["Nome"])
            data_consulta = st.date_input("Data da Consulta: ")
            horario_consulta = st.time_input(f"Horário da Consulta : ", key=f"horario_consulta_{selected_patient}")


            ## Verifica se a data é no futur
            if data_consulta < datetime.now().date():
                st.error("A data da consulta deve ser no futuro.")
                return
            
            ## Verifica se já existe outra consulta marcada no mesmo horario e dia
            if consulta_conflitante(pacientes, data_consulta, horario_consulta):
                st.error("Já existe uma consulta marcada para esse dia e horário.")
                return

    
            ## Salva as informações da consulta no dicionário do paciente
            if st.button("Confirmar Consulta"):
                ## Salva as informações da consulta no dicionário do paciente
                paciente["Próxima Consulta"] = {
                    "Data": str(data_consulta),
                    "Horário": str(horario_consulta)
                }
                st.success("Consulta marcada com sucesso!")

            ## Salva as alterações no arquivo pacientes.json
            with open("pacientes.json", "w", encoding="utf-8") as file:
                json.dump(pacientes, file, indent=4)

    
def show_historico_paciente(paciente):
     # Obtém o histórico médico do paciente
    historico = paciente.get("Histórico", [])
    
     # Verifica se há registros no histórico e itera sobre cada evento
    if historico:
        for evento in historico:
            st.write(f"Data: {evento['Data']}")
            st.write(f"Descrição: {evento['Descrição']}")
            st.write("----")
    else:
        st.write("Nenhum registro no histórico médico.")


def show_consultas(pacientes):
    with st.expander("Próximas Consultas", expanded=False):
        for paciente in pacientes:
            if "Próxima Consulta" in paciente:
                st.write(f"Nome: {paciente['Nome']}")
                st.write(f"Próxima Consulta: {paciente['Próxima Consulta']['Data']} às {paciente['Próxima Consulta']['Horário']}")
                st.write("---")


def consulta_conflitante(pacientes, nova_data, novo_horario):
    # Verifica se uma nova consulta tem conflito de data e horário com consultas existentes
    for paciente in pacientes:
        if "Próxima Consulta" in paciente:
            consulta_existente = paciente["Próxima Consulta"]
            data_existente = datetime.strptime(consulta_existente["Data"], "%Y-%m-%d").date()
            horario_existente = datetime.strptime(consulta_existente["Horário"], "%H:%M:%S").time()

            if data_existente == nova_data and horario_existente == novo_horario:
                return True

    return False

def formatar_proxima_consulta(consulta):
    if consulta != "Sem consulta marcada":
        data_consulta = datetime.strptime(consulta["Data"], "%Y-%m-%d").strftime("%d-%m-%Y")
        horario_consulta = consulta["Horário"]
        return f" {data_consulta} às {horario_consulta}"
    else:
        return "Sem consulta marcada"
    
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



