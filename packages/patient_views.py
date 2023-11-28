from .patient_data import carregar_pacientes
from .patient_files import salvar_exames, salvar_prescricao, salvar_notas
import streamlit as st
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


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

            ## Mostra o histórico médico
            with st.expander("Histórico de Consultas"):
                show_historico_paciente(paciente)

            ## Mostra a edição de paciente
            editar_expander = st.expander("Editar Informações do Paciente")
            show_editar_paciente(editar_expander, pacientes, selected_patient)

            with st.expander("Tipos Comuns de Doenças"):
                plot_doencas_comuns(pacientes)

            
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
            st.write("Próxima Consulta: ", paciente.get("Próxima Consulta", "Sem consulta marcada"))

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
    historico = paciente.get("Historico", [])
    
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


def plot_doencas_comuns(pacientes):
    ## Coleta todas as doenças
    todas_doencas = [doenca.strip() for paciente in pacientes for doenca in paciente["Doenças Preexistentes"]]

    ## Cria um gráfico
    plt.figure(figsize=(10, 6))
    sns.countplot(y=todas_doencas, order=pd.Series(todas_doencas).value_counts().index)
    plt.title("Tipos Comuns de Doenças")
    plt.xlabel("Número de Pacientes")
    plt.ylabel("Doenças")
    
    st.pyplot(plt)