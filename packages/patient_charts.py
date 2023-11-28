import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def verificar_t_sanguineo(pacientes):
    with st.expander("Tipos Sanguíneos Predominantes"):
        ## Coleta todos os tipos sanguíneos
        todos_tipos = [paciente.get("Tipo Sanguíneo", "").strip() for paciente in pacientes if "Tipo Sanguíneo" in paciente]

        ## Cria um gráfico
        plt.figure(figsize=(10, 6))
        sns.countplot(y=todos_tipos, order=pd.Series(todos_tipos).value_counts().index)
        plt.title("Tipos Sanguíneos Predominantes")
        plt.xlabel("Número de Pacientes")
        plt.ylabel("Tipos Sanguíneos")
        
        st.pyplot(plt)



def plot_doencas_comuns(pacientes):
    with st.expander("Doenças Comuns entre os Pacientes"):
        ## Coleta todas as doenças
        todas_doencas = [doenca.strip() for paciente in pacientes for doenca in paciente["Doenças Preexistentes"]]

        ## Cria um gráfico
        plt.figure(figsize=(10, 6))
        sns.countplot(y=todas_doencas, order=pd.Series(todas_doencas).value_counts().index)
        plt.title("Tipos Comuns de Doenças")
        plt.xlabel("Número de Pacientes")
        plt.ylabel("Doenças")
        
        st.pyplot(plt)
