import streamlit as st
import json

def carregar_pacientes():
    with open("pacientes.json", "r", encoding="utf-8") as file:
        pacientes = json.load(file)
    return pacientes

def main():
    st.title("PatientBook")

    # Carrega pacientes do arquivo JSON
    pacientes = carregar_pacientes()

    # Barra de Navegação
    tabs = ["Pacientes", "Editar Paciente", "Marcar Consulta"]
    choice = st.radio("Escolha uma opção: ", tabs)

    # Renderiza a aba
    if choice == "Pacientes":
        show_pacientes(pacientes)
    elif choice == "Editar Paciente":
        show_editar_paciente(pacientes)
    elif choice == "Marcar Consulta":
        show_marcar_consulta(pacientes)

def show_pacientes(pacientes):
    st.subheader("Lista de Pacientes")

    # Mostra o nome dos pacientes como uma lista
    selected_patient = st.selectbox("Selecione um paciente: ", [paciente["Nome"] for paciente in pacientes])

    # Mostra a ficha do paciente
    if selected_patient:
        paciente = next((p for p in pacientes if p["Nome"] == selected_patient), None)
        if paciente:
            st.write("Nome: ", paciente["Nome"])
            st.write("Idade: ", paciente["Idade"])
            st.write("Endereço: ", paciente["Endereço"])
            st.write("Convênio: ", paciente["Convenio"])
            st.write("Doenças Preexistentes:", paciente["Doenças Preexistentes"])

def show_editar_paciente(pacientes):
    st.subheader("Editar Informações do Paciente")

    # Mostra o nome dos pacientes como uma lista
    selected_patient = st.selectbox("Selecione um paciente: ", [paciente["Nome"] for paciente in pacientes])

    # Mostra o formulário para editar as informações do paciente selecionado
    if selected_patient:
        paciente = next((p for p in pacientes if p["Nome"] == selected_patient), None)
        if paciente:
            st.write("Nome: ", paciente["Nome"])
            idade = st.number_input("Idade: ", value=paciente["Idade"])
            endereco = st.text_input("Endereço: ", value=paciente["Endereço"])
            convenio = st.text_input("Convênio: ", value=paciente["Convenio"])
            doencas_preexistentes = st.text_input("Doenças Preexistentes: ", value=", ".join(paciente["Doenças Preexistentes"]))

            # Atualiza as informações do paciente no dicionário
            paciente["Idade"] = idade
            paciente["Endereço"] = endereco
            paciente["Convenio"] = convenio
            paciente["Doenças Preexistentes"] = [d.strip() for d in doencas_preexistentes.split(",")]

            # Salva as alterações no arquivo pacientes.json
            with open("pacientes.json", "w", encoding="utf-8") as file:
                json.dump(pacientes, file, indent=4)

def show_marcar_consulta(pacientes):
    st.subheader("Marcar Consulta")

    # Mostra o nome dos pacientes como uma lista
    selected_patient = st.selectbox("Selecione um paciente: ", [paciente["Nome"] for paciente in pacientes])

    # Mostra o formulário para marcar a consulta para o paciente selecionado
    if selected_patient:
        paciente = next((p for p in pacientes if p["Nome"] == selected_patient), None)
        if paciente:
            st.write("Nome: ", paciente["Nome"])
            data_consulta = st.date_input("Data da Consulta: ")
            horario_consulta = st.time_input("Horário da Consulta: ")

            # Salva as informações da consulta no dicionário do paciente
            consulta = {
                "Data": str(data_consulta),
                "Horário": str(horario_consulta)
            }
            paciente["Consulta"] = consulta

            # Salva as alterações no arquivo pacientes.json
            with open("pacientes.json", "w", encoding="utf-8") as file:
                json.dump(pacientes, file, indent=4)

if __name__ == "__main__":
    main()