from .patient_data import carregar_pacientes
from .patient_files import salvar_exames, salvar_prescricao, salvar_notas
import streamlit as st
import json
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
            st.write("Doenças Preexistentes:", paciente["Doenças Preexistentes"])
            st.write("Próxima Consulta: ", paciente.get("Próxima Consulta", "Sem consulta marcada"))


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
            st.write("Consulta: ", paciente.get("Consulta", "Sem consulta marcada"))

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
            notas = paciente.get("Notas", [])
            if notas:
                st.subheader("Notas: " )
                for nota in notas:
                    st.write(nota)


def show_editar_paciente(pacientes):
    st.subheader("Editar Informações do Paciente")

    ## Mostra o nome dos pacientes como uma lista
    selected_patient = st.selectbox("Selecione um paciente: ", [paciente["Nome"] for paciente in pacientes])

    ## Mostra o formulário para editar as informações do paciente selecionado
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
            horario_consulta = st.time_input("Horário da Consulta: ")

            ## Salva as informações da consulta no dicionário do paciente
            paciente["Próxima Consulta"] = {
                "Data": str(data_consulta),
                "Horário": str(horario_consulta)
            }

            ## Salva as alterações no arquivo pacientes.json
            with open("pacientes.json", "w", encoding="utf-8") as file:
                json.dump(pacientes, file, indent=4)




