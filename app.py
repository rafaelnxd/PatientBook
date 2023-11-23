import streamlit as st
import json

def carregar_pacientes():
    with open("pacientes.json", "r", encoding="utf-8") as file:
        pacientes = json.load(file)
    return pacientes

def main():
    st.title("PatientBook")

    # Carrega substâncias do arquivo JSON
    pacientes = carregar_pacientes()

    # Barra de Navegação
    tabs = ["Pacientes", "Editar Paciente", "Marcar Consulta"]
    choice = st.radio("Escolha uma opção: ", tabs)

    # Renderiza a aba
    if choice == "Pacientes":
        show_pacientes(pacientes)
    elif choice == "Editar Paciente":
        show_editar_paciente(pacientes)
    



def show_pacientes(pacientes):
    st.subheader("Lista de Pacientes")

    # Mostra o nome dos pacientes como uma lista
    selected_patient = st.selectbox("Selecione um paciente: ", list(pacientes.keys()))

    # Mostra a ficha do paciente
    if selected_patient:
        paciente = pacientes[selected_patient]
        st.write("Nome: ", paciente["Nome"])
        st.write("Idade: ", paciente["Idade"])
        st.write("Endereço: ", paciente["Endereço"])
        st.write("Convênio: ", paciente["Convênio"])
        st.write("Doenças Preexistentes:", paciente["Doenças Preexistentes"])






def show_editar_paciente(pacientes):
    return


def show_marcar_consulta(pacientes):
    return
