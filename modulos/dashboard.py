from modulos._settings import FILE_RETORNO
import plotly.express as px
import streamlit as tk
import pandas as pd


class Dashboard:
    def __init__(self):
        self.dados_retorno = pd.read_excel(FILE_RETORNO)
        
        self.fundo = "#E3F2FF"
        self.valores = "#AA3032"
        self.barras = "#115086"

        self.dados()

    def dados(self):
        # Saúde do Estoque
        life_ST = self.dados_retorno.groupby("STATUS_FINAL").size().reset_index(name='CONTAGEM') 

        # Mapeamento de Falhas de Capacidade e Giro
        map_div = self.dados_retorno.groupby("RUA").agg(
            DIVERGENCIA = ("STATUS_FINAL", lambda x: (x == "DIV").sum())
        ).reset_index()
        map_div = map_div[map_div["DIVERGENCIA"] > 0]

        # Ruptura de Fluxo: Itens que Exigem Mais de Uma Reposição Diária
        crit_cap = self.dados_retorno.groupby("RUA").agg(
            qtde = ("CRIT_CAP", lambda x: (x == "AJUSTAR").sum())
        ).reset_index()
        crit_cap = crit_cap[crit_cap["qtde"] > 0]

        #Itens Críticos por Rua (Reposição < Giro_dia)
        sit_ros = self.dados_retorno.groupby("RUA").agg(
            qtde = ("SIT_REPOS", lambda x: (x == "AJUSTAR").sum())
        ).reset_index()
        sit_ros = sit_ros[sit_ros["qtde"] > 0]

        # Produtos com Consumo Diário > 50% da Capacidade
        alerta_50 = self.dados_retorno.groupby("RUA").agg(
            qtde = ("ALERTA_50", lambda x: (x == "AJUSTAR").sum())
        ).reset_index()
        alerta_50 = alerta_50[alerta_50["qtde"] > 0]

        # Mapeamento de produtos dividos
        divididos = self.dados_retorno.groupby("RUA").agg(
            qtde = ("STATUS_PROD", lambda x: x.isin(["DIV", "VAL"]).sum())
        ).reset_index()
        divididos = divididos[divididos["qtde"] > 0]

        resumo_geral = pd.DataFrame({
            "INDICADOR": ["Capacidade Critica", "Pressão de Preposição", "Ponto de Reposição Critico"],
            "VALOR": [
                (self.dados_retorno["CRIT_CAP"] == "AJUSTAR").sum(),
                (self.dados_retorno["ALERTA_50"] == "AJUSTAR").sum(),
                (self.dados_retorno["SIT_REPOS"] == "AJUSTAR").sum(),
            ]
        })
    def graficos(self):
        pass