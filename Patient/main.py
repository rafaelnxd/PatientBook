from packages.patient_data import carregar_pacientes
from packages.patient_views import show_pacientes, show_editar_paciente, show_marcar_consulta, show_notas_paciente
import streamlit as st

def main():
    st.title("PatientBook")

    ## Carrega os pacientes do arquivo pacientes.json
    pacientes = carregar_pacientes()

    ## Barra de Navegação
    tabs = ["Pacientes", "Editar Paciente", "Marcar Consulta", "Notas pro Paciente"]
    choice = st.radio("Escolha uma opção: ", tabs)

    ## Mostra a página escolhida
    if choice == "Pacientes":
        show_pacientes(pacientes)
    elif choice == "Editar Paciente":
        show_editar_paciente(pacientes)
    elif choice == "Marcar Consulta":
        show_marcar_consulta(pacientes)
    elif choice == "Notas pro Paciente":
        show_notas_paciente(pacientes)

if __name__ == "__main__":
    main()