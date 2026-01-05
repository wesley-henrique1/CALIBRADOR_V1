from path_dados import FILE_RETORNO
import matplotlib
matplotlib.use('TkAgg') # Força o uso da interface do Tkinter
import matplotlib.pyplot as plt
from logica import Auxiliares
import pandas as pd
aux = Auxiliares()



class Dashboard:
    def __init__(self):
        self.df_retorno = None
        self.sucesso = False  # Flag de controle
        self.col = ['RUA', 'CRIT_CAP', 'STATUS_PROD', 'SIT_REPOS','ALERTA_50','STATUS_FINAL']
        try:
            self.df_retorno = pd.read_excel(FILE_RETORNO, usecols= self.col)
            self.sucesso = True # Se chegar aqui, deu certo
        except Exception as e:
            # Chama sua classe de erro (estática ou instanciada conforme conversamos)
            aux.validar_erro(e, "CARREGAMENTO_DASHBOARD")
            self.sucesso = False

    def pizza(self):
        """
        Saúde do Estoque - Gráfico de Pizza
        """
        try:
            # 1. Contagem dos valores
            divergencia = len(self.df_retorno[self.df_retorno['STATUS_FINAL'] == "DIV"])
            normal = len(self.df_retorno[self.df_retorno['STATUS_FINAL'] == "NORMAL"])
            print(f"Divergências: {divergencia} | Normais: {normal}")
            # 2. Preparação dos dados para o Matplotlib
            labels = ['Divergente', 'Normal']
            valores = [divergencia, normal]
            cores = ['#ff4d4d', '#2eb82e'] # Vermelho e Verde

            # 3. Criação do gráfico
            plt.figure(figsize=(6, 4))
            plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=140, colors=cores)
            plt.title("Saúde do Estoque")
            
            plt.show()
        except Exception as e:
            from logica import Auxiliares
            aux = Auxiliares()
            aux.validar_erro(e, "GERAÇÃO_GRAFICO_PIZZA")    

    def list_mutiplico(self):
        """
        COMPARATIVO
        """
        pass
    def area_1(self):
        """
        Mapeamento de Falhas de Capacidade e Giro
        """
        pass
    
    def coluna_1(self):
        """
        Ruptura de Fluxo: Itens que Exigem Mais de Uma Reposição Diária
        """
        pass
    def coluna_2(self):
        """
        Itens Críticos por Rua (Reposição < Giro_dia)
        """
        pass
   
    def coluna_3(self):
        """
        Produtos com Consumo Diário > 50% da Capacidade
        """
        pass
    def area_2(self):
        """
        Mapeamento de produtos dividos
        """
        pass



if __name__ == "__main__":
    dash = Dashboard()
    dash.pizza()