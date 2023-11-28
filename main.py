from packages.patient_data import carregar_pacientes
from packages.patient_views import show_pacientes, show_editar_paciente, show_marcar_consulta, show_notas_paciente, show_consultas, plot_doencas_comuns
import streamlit as st

st.set_page_config(
    page_title="PatientBook",
    page_icon=":clipboard:",
    layout="centered",
    initial_sidebar_state="auto",
)

def main():
    st.title("PatientBook")

    ## Carrega os pacientes do arquivo pacientes.json
    pacientes = carregar_pacientes()

    ## Barra de Navegação
    tabs = ["Pacientes","Notas pro Paciente", "Consultas", "Estatísticas" ]
    choice = st.radio("Escolha uma opção: ", tabs)

    ## Mostra a página escolhida
    if choice == "Pacientes":
        show_pacientes(pacientes)
    elif choice == "Consultas":
        show_consultas(pacientes)
        show_marcar_consulta(pacientes)
    elif choice == "Notas pro Paciente":
        show_notas_paciente(pacientes)
    elif choice == "Estatísticas":
        plot_doencas_comuns(pacientes)

if __name__ == "__main__":
    main()