import os
import sys
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, diretorio_atual)
from base_dados.path_dados import *
import datetime as data
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)


class Calibrar_ruas:
    def __init__(self):
        os.system("title CALIBRADOR_V1")
        listagem_path = [
            Path_dados.cadastro_8596, Path_dados.acesso_8560, Path_dados.estoque_286
            ,Path_dados.movimentar_1,Path_dados.movimentar_2,Path_dados.movimentar_3,Path_dados.movimentar_4
            ,Path_dados.sugestao_1,Path_dados.sugestao_2,Path_dados.sugestao_3,Path_dados.sugestao_4
        ]

        self.LARGURA = 78

        self.carregamento(list_path= listagem_path)
        print("Digite a(s) rua(s) a ser(em) filtrada(s) separadas por espaço (ex: 1 5 10):")
        entrada = input(">>> ").split()
        self.pipeline(list_path= listagem_path, filtro_rua= entrada)
        
    def validar_erro(self, e, etapa):
        print("=" * self.LARGURA)
        print(f"ETAPA: {etapa}")
        print(f"ERRO DETECTADO: {type(e).__name__}")

        if isinstance(e, PermissionError):
            print(">>> O arquivo de destino está aberto ou você não tem permissão.")
            print(">>> Por favor, feche o Excel e tente novamente.")       
        elif isinstance(e, FileNotFoundError):
            print(">>> Um dos arquivos de origem não foi encontrado.")
            print(">>> Verifique se a pasta 'base_dados' está ao lado do executável.")
        elif isinstance(e, KeyError):
            print(f">>> A coluna ou chave '{e}' não foi encontrada no DataFrame.")           
        elif isinstance(e, TypeError):
            print(f">>> Erro de tipo: Operação inválida entre dados incompatíveis.")
            print(f">>> Detalhe: {e}")     
        elif isinstance(e, ValueError):
            print(f">>> Erro de valor: O formato do dado não corresponde ao esperado.")
            print(f">>> Detalhe: {e}")
        elif isinstance(e, NameError):
            print(f">>> Erro de definição: Variável ou função não definida.")
            print(f">>> Detalhe: {e}")    
        else:
            print(f">>> Erro não mapeado: {e}")

        print("=" * self.LARGURA)
        input("Pressione ENTER para fechar o programa...")
        sys.exit()
    def director(self, lista_files):
        lista = []
        for arquivo in lista_files:
            try:
                x = pd.read_csv(arquivo, header=None)
                lista.append(x)
            except Exception as e:
                self.validar_erro(e, "DIRECTOR")
        if not lista:
            return pd.DataFrame()
        df_temp = pd.concat(lista, axis=0, ignore_index=True)
        return df_temp


    def carregamento(self, list_path):
        try:
            print(f"\n{"ARQUIVOS":_^{self.LARGURA}}")
            for contador, path in enumerate(list_path, 1):
                data_file = os.path.getmtime(path)
                nome_file = os.path.basename(path)

                data_modificacao = data.datetime.fromtimestamp(data_file)
                data_formatada = data_modificacao.strftime('%d/%m/%Y - %H:%M:%S')

                files_completo = nome_file + " - " + data_formatada
                print(f"{contador} - {files_completo}\n")
            print(f"{"_" * self.LARGURA}")
        except Exception as e:
            self.erro = self.validar_erro(e, "CARREGAMENTO")
            input("ENTER...")
            exit()
    def pipeline(self, list_path, filtro_rua):
        try: # CARREGAMENTO
            col_produtos =[
                'CODPROD'
                ,'DESCRICAO'
                ,'QTUNITCX'
                ,'QTTOTPAL'
                ,'OBS2'
                ,'RUA'
                ,'PREDIO'
                ,'APTO'
                ,'EMBALAGEM'
                ,'CAPACIDADE'
                ,'PONTOREPOSICAO'
                ]
            col_acesso =[
                'CODPROD'
                ,'QTOS'
                ,'QT'
                ]
            col_estoque =[
                'Código'
                ,'Estoque'
                ,'Custo ult. ent.'
                ,'Qtde Pedida'
                ,'Bloqueado(Qt.Bloq.-Qt.Avaria)'
                ,'Qt.Avaria'
                ]
            col_movimentar = [
                'COD'
                ,'DESC'
                ,'EMBALAGEM'
                ,'UNID'
                ,'MOVI'
                ,'%'
                ,'%_ACUM'
                ,'CLASSE'
                ]
            col_sugestao = [
                'COD'
                ,'DESC'
                ,'EMBALAGEM'
                ,'UNID.'
                ,'DEP'
                ,'RUA'
                ,'PREDIO'
                ,'NIVEL'
                ,'APTO'
                ,'MES_1'
                ,'MES_2'
                ,'MES_3'
                ,'TIPO'
                ,'CAP'
                ,'1_DIA'
                ,'COM_FATOR'
                ,'VARIAÇÃO'
                ,'%'
                ]

            df_produtos = pd.read_excel(list_path[0], usecols= col_produtos)
            df_acesso = pd.read_excel(list_path[1], usecols= col_acesso)
            df_estoque = pd.read_excel(list_path[2], usecols= col_estoque)

            list_sugestao = [
                Path_dados.sugestao_1
                ,Path_dados.sugestao_2
                ,Path_dados.sugestao_3
                ,Path_dados.sugestao_4
            ]
            df_sugestao = self.director(list_sugestao)
            df_sugestao.columns = col_sugestao
            
            list_movimentar = [
                Path_dados.movimentar_1
                ,Path_dados.movimentar_2
                ,Path_dados.movimentar_3
                ,Path_dados.movimentar_4
            ]
            df_movimentar = self.director(list_movimentar)
            df_movimentar.columns = col_movimentar
        except Exception as e:
            self.validar_erro(e, "EXTRAIR")
            return

        try: # TRATAMENTO
            df_sugestao = df_sugestao.drop_duplicates(subset=['COD'], keep='first')
            df_sugestao.replace([np.inf, -np.inf], 0, inplace=True) 
            df_sugestao = df_sugestao.drop(columns= ['EMBALAGEM','DESC','UNID.','DEP', 'RUA', 'PREDIO', 'NIVEL', 'APTO','TIPO', 'CAP','%'])
            
            df_movimentar = df_movimentar.drop_duplicates(subset=['COD'], keep='first')
            df_movimentar.replace([np.inf, -np.inf], 0, inplace=True) 
            df_movimentar = df_movimentar.drop(columns= ['DESC', 'EMBALAGEM', 'UNID','%','%_ACUM'])

            if filtro_rua:
                filtro = list(map(int, filtro_rua))
                df_produtos = df_produtos.loc[df_produtos['RUA'].isin(filtro)]
            else:
                print(">>> Nenhuma rua digitada. filtrando rua 1 a rua 39.")
                df_produtos = df_produtos.loc[df_produtos['RUA'].between(1,39)]

            df_produtos['OBS2'] = df_produtos['OBS2'].fillna("Ativos")
            df_produtos["PRODUTO"] = df_produtos['CODPROD'].astype(str)

            df_estoque = df_estoque.fillna(0)
            rename = {
                "Código" : "CODPROD"
                ,"Qtde Pedida" : "PEDIDO_COMP"
                ,"Bloqueado(Qt.Bloq.-Qt.Avaria)" : "BLOQUEADO"
                ,"Qt.Avaria" : "AVARIA"
                ,"Custo ult. ent." : "CUSTO_ULT_ENTRADA"
            }

            df_estoque = df_estoque.rename(columns=rename)
            df_acesso = df_acesso.groupby('CODPROD').agg(
            ACESSO = ("QTOS", "sum")
            ).reset_index()
            
            df_calibrado = df_produtos.merge(df_sugestao, left_on= 'CODPROD', right_on= 'COD', how= 'left').drop(columns= 'COD')
            df_calibrado = df_calibrado.merge(df_estoque, left_on='CODPROD', right_on='CODPROD', how='left')
            df_calibrado = df_calibrado.merge(df_acesso, left_on='CODPROD', right_on='CODPROD', how= 'left')
            df_calibrado = df_calibrado.merge(df_movimentar, left_on='CODPROD', right_on='COD', how="left").drop(columns= 'COD')

            df_calibrado['SUG_%'] = round(df_calibrado['COM_FATOR'] / df_calibrado['QTTOTPAL'], 2).fillna(0)
            df_calibrado['ATUAL_%'] = round(df_calibrado['CAPACIDADE'] / df_calibrado['QTTOTPAL'], 2).fillna(0)
            df_calibrado['VAL_1_DIA'] = np.where(
                df_calibrado['PONTOREPOSICAO'] < df_calibrado['1_DIA'], "MENOR", "NORMAL"
            )
            df_calibrado['CUSTO'] = df_calibrado['CUSTO_ULT_ENTRADA'].round(2)

        except Exception as e:
            self.validar_erro(e, "TRATAMENTO")

        try: # CARGA

            df_calibrado = df_calibrado.sort_values(by= ['RUA', 'PREDIO'], ascending= True)
            col_ordenar = [
                'PRODUTO'
                ,'CODPROD'
                ,'DESCRICAO'
                ,'OBS2'
                ,'QTUNITCX'
                ,'EMBALAGEM'
                ,'RUA'
                ,'PREDIO'
                ,'APTO'
                ,'CAPACIDADE'
                ,'QTTOTPAL'
                ,'Estoque'
                ,'PEDIDO_COMP'
                ,'BLOQUEADO'
                ,'AVARIA'
                ,'CUSTO'
                ,'MES_1'
                ,'MES_2'
                ,'MES_3'
                ,'1_DIA'
                ,'COM_FATOR'
                ,'ACESSO'
                ,'MOVI'
                ,'SUG_%'
                ,'ATUAL_%'
                ,'VAL_1_DIA'
                ,'CLASSE'
            ]
            df_calibrado = df_calibrado[col_ordenar]

            
            df_calibrado.to_excel(Path_dados.retorno, index= False, sheet_name= 'Calibração')
        except Exception as e:
            self.validar_erro(e, "CARGA")
   
if __name__ == '__main__':
    Calibrar_ruas()
    print("_" * 78)
    input("\nFavor pressionar a tecla 'enter' para finalizar o processo")
