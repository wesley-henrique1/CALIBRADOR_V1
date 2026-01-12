import os
import sys
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, diretorio_atual)

from path_dados import *
import datetime as data
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)


class Auxiliares:
    def validar_erro(self, e, etapa):
        LARGURA = 78
        if isinstance(e, PermissionError):
            msg = (
                f">>> O arquivo de destino está aberto ou você não tem permissão."
                f">>> Por favor, feche o Excel e tente novamente."
            )      
        elif isinstance(e, FileNotFoundError):
            msg = (
                f">>> Um dos arquivos de origem não foi encontrado."
                f">>> Verifique se a pasta 'base_dados' está ao lado do executável."
            )
        elif isinstance(e, KeyError):
            msg = (f">>> A coluna ou chave '{e}' não foi encontrada no DataFrame.")           
        elif isinstance(e, TypeError):
            msg = (
                f">>> Erro de tipo: Operação inválida entre dados incompatíveis."
                f">>> Detalhe: {e}"
            )     
        elif isinstance(e, ValueError):
            msg = (
                f">>> Erro de valor: O formato do dado não corresponde ao esperado."
                f">>> Detalhe: {e}"
            )
        elif isinstance(e, NameError):
            msg = (
                f">>> Erro de definição: Variável ou função não definida."
                f">>> Detalhe: {e}"
            )
        else:
            msg = (f">>> Erro não mapeado: {e}")
        agora = data.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        log_conteudo = (
            f"{'='* LARGURA}\n"
            f"ETAPA: {etapa} - {agora}\n"
            f"TIPO: {type(e).__name__}\n"
            f"MENSAGEM: {msg}\n"
            f"{'='* LARGURA}\n\n"
        )
        try:
            with open("log_erros.txt", "a", encoding="utf-8") as erros_log:
                erros_log.write(log_conteudo)
        except Exception as erro_gravacao:
            print(f"Não foi possível gravar o log: {erro_gravacao}")
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
class Logicas(Auxiliares):
    def __init__(self):
        os.system("title CALIBRADOR_V1")
        self.listagem_path = [
            Path_dados.cadastro_8596    # CADASTRO DOS PRODUTOS
            ,Path_dados.acesso_8560     # ESTOQUE E O CUSTO DOS PRODUTOS
            ,Path_dados.estoque_286     # ACESSO DOS PRODUTOS
            ,Path_dados.baixa_8628      # BAIXA DOS PRODUTOS
        ]
        self.list_sugestao = [
            Path_dados.sugestao_1   # DEPOSITO 1
            ,Path_dados.sugestao_2  # DEPOSITO 2
            ,Path_dados.sugestao_3  # DEPOSITO 3
            ,Path_dados.sugestao_4  # DEPOSITO 4
        ]
        self.list_movimentar = [
            Path_dados.movimentar_1     # DEPOSITO 1
            ,Path_dados.movimentar_2    # DEPOSITO 2
            ,Path_dados.movimentar_3    # DEPOSITO 3
            ,Path_dados.movimentar_4    # DEPOSITO 4
        ]
        self.LARGURA = 78
        self.list_int = ['2-INTEIRO(1,90)', '1-INTEIRO (2,55)']

    def carregamento(self, indice):
        lista_de_logs = []
        if indice:
            itens_movi = [self.list_movimentar[i] for i in indice]
            itens_sug = [self.list_sugestao[i] for i in indice]
        else:
            itens_movi = self.list_movimentar
            itens_sug = self.list_sugestao

        lista_completa = self.listagem_path + itens_movi + itens_sug
        try:
            for contador, path in enumerate(lista_completa, 1):
                if os.path.exists(path):
                    data_file = os.path.getmtime(path)
                    nome_file = os.path.basename(path)

                    data_modificacao = data.datetime.fromtimestamp(data_file)
                    data_formatada = data_modificacao.strftime('%d/%m/%Y')
                    horas_formatada = data_modificacao.strftime('%H:%M:%S')

                    dic_log = {
                        "CONTADOR" : contador
                        ,"ARQUIVO" : nome_file
                        ,"DATA" : data_formatada
                        ,"HORAS" : horas_formatada
                    }
                    lista_de_logs.append(dic_log)
                else:
                    lista_de_logs.append({
                        "CONTADOR": contador,
                        "ARQUIVO": f"ERRO: {os.path.basename(path)} (Não encontrado)",
                        "DATA": "--/--/----",
                        "HORAS": "--:--:--"
                    })
            return lista_de_logs
        except Exception as e:
            self.validar_erro(e, "CARREGAMENTO")
            return False
    def pipeline(self, filtro_rua, indice):
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
                ,'PK_END'
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
                ,'GIRO_DIA'
                ,'SUGESTAO'
                ,'VARIAÇÃO'
                ,'%'
                ]
            col_baixa = [
                'CODPROD'
                ,'NIVEL'    
                ,'NIVEL_1'
                ,'CODROTINA'
                ,'Tipo O.S.'
            ]
            df_produtos = pd.read_excel(self.listagem_path[0], usecols= col_produtos)
            df_acesso = pd.read_excel(self.listagem_path[1], usecols= col_acesso)
            df_estoque = pd.read_excel(self.listagem_path[2], usecols= col_estoque)
            df_baixa = pd.read_excel(
                self.listagem_path[3]
                ,usecols= col_baixa
                ,dtype= {'NIVEL': 'Int64', 'NIVEL_1': 'Int64', 'CODROTINA': 'Int64'}
            )

            if  indice:
                itens_sug = [self.list_sugestao[i] for i in indice]
                itens_movi = [self.list_movimentar[i] for i in indice]
                df_sugestao = self.director(itens_sug)
                df_movimentar = self.director(itens_movi)
            else:
                df_sugestao = self.director(self.list_sugestao)
                df_movimentar = self.director(self.list_movimentar)

            df_sugestao.columns = col_sugestao
            df_movimentar.columns = col_movimentar  
        except Exception as e:
            self.validar_erro(e, "EXTRAIR")
            return False

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
                df_produtos = df_produtos.loc[df_produtos['RUA'].between(1,39)]

            df_produtos['OBS2'] = df_produtos['OBS2'].fillna("Ativos")

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
            
            df_baixa = df_baixa.loc[
                ((df_baixa['CODROTINA'].isin([1709, 1723])))
                & (df_baixa['NIVEL'].between(2,8))
                & (df_baixa['NIVEL_1'] == 1)
                & (df_baixa['Tipo O.S.'] == "58 - Transferencia de Para Vertical")
            ]
            baixa_grupado = df_baixa.groupby('CODPROD').agg(
                BAIXA = ('CODPROD', 'size')
            ).reset_index().fillna(0)

            df_calibrado = df_produtos.merge(
                df_sugestao
                ,left_on= 'CODPROD'
                ,right_on= 'COD'
                ,how= 'left'
            ).drop(columns= 'COD')
            df_calibrado = df_calibrado.merge(
                df_movimentar
                ,left_on='CODPROD'
                ,right_on='COD'
                ,how="left"
            ).drop(columns= 'COD')
            df_calibrado = df_calibrado.merge(
                df_estoque
                ,on='CODPROD'
                ,how='left'
            )
            df_calibrado = df_calibrado.merge(
                df_acesso
                ,on='CODPROD'
                ,how= 'left'
            )
            df_calibrado = df_calibrado.merge(
                baixa_grupado
                ,on='CODPROD'
                ,how= 'left'
            )
            df_calibrado = df_calibrado.fillna({
                'MOVI': 0, 
                'BAIXA': 0,
                'Estoque': 0
            }).astype({
                'MOVI': int, 
                'BAIXA': int
            })

            concat = df_calibrado['RUA'].astype(str) + " - " + df_calibrado['PREDIO'].astype(str)
            df_calibrado['CUSTO'] = df_calibrado['CUSTO_ULT_ENTRADA'].round(2)

            df_calibrado['SUG_%'] = round(df_calibrado['SUGESTAO'] / df_calibrado['QTTOTPAL'], 2).fillna(0)
            df_calibrado['ATUAL_%'] = round(df_calibrado['CAPACIDADE'] / df_calibrado['QTTOTPAL'], 2).fillna(0)

            df_calibrado['SIT_REPOS'] = np.where(
                df_calibrado['PONTOREPOSICAO'] < df_calibrado['GIRO_DIA']
                ,"AJUSTAR"
                ,"NORMAL"
            )
            df_calibrado['CRIT_CAP'] = np.where(
                df_calibrado['GIRO_DIA'] >= df_calibrado['CAPACIDADE']
                ,"AJUSTAR"
                ,"NORMAL"
            )
            df_calibrado['ALERTA_50'] = np.where(
                df_calibrado['CRIT_CAP'] == "NORMAL"
                ,np.where((
                    df_calibrado['GIRO_DIA'].astype(float) / df_calibrado['CAPACIDADE'].astype(float)) > 0.5
                        ,"AJUSTAR"
                        ,"NORMAL"
                    )
                ,"NORMAL" 
            )
            df_calibrado['FREQ_PROD'] = concat.map(concat.value_counts())

            df_calibrado['STATUS_PROD'] = np.where(
                (df_calibrado['FREQ_PROD'] <= 2) & (df_calibrado['PK_END'].isin(self.list_int))
                ,"INT",
                np.where(
                    df_calibrado['FREQ_PROD'] > 3,
                    "DIV"
                    ,"VAL"
                )
            )
            df_calibrado['STATUS_FINAL'] = np.where(
                (df_calibrado['CRIT_CAP'] == "NORMAL")
                & (df_calibrado['SIT_REPOS'] == "NORMAL")
                & (df_calibrado['ALERTA_50'] == "NORMAL")
                ,"NORMAL"
                ,"DIV"
            )
            
            df_calibrado['EST_CX'] = round(
               (df_calibrado['Estoque'].replace(0, np.nan) / df_calibrado['QTUNITCX'].replace(0, np.nan))
                ,1
            ).fillna(0)
            df_calibrado['EST_PLT'] = round(
                (df_calibrado['EST_CX'].replace(0, np.nan) / df_calibrado['QTTOTPAL'].replace(0, np.nan))
                ,1
            ).fillna(0)
            
            col_analises = ['SUG_%', 'ATUAL_%', 'SIT_REPOS','ALERTA_50','CRIT_CAP','FREQ_PROD','STATUS_PROD','STATUS_FINAL']
        except Exception as e:
            self.validar_erro(e, "TRATAMENTO")
            return False

        try: # CARGA
            df_calibrado = df_calibrado.sort_values(by= ['RUA', 'PREDIO'], ascending= True)
            col_ordenar = [
                'CODPROD'
                ,'DESCRICAO'
                ,'OBS2'
                ,'QTUNITCX'
                ,'EMBALAGEM'
                ,'RUA'
                ,'PREDIO'
                ,'APTO'
                ,'CAPACIDADE'
                ,'QTTOTPAL'
                ,'BAIXA'
                ,'Estoque'
                ,'EST_PLT'
                ,'EST_CX'
                ,'PEDIDO_COMP'
                ,'BLOQUEADO'
                ,'AVARIA'
                ,'CUSTO'
                ,'MES_1'
                ,'MES_2'
                ,'MES_3'
                ,'GIRO_DIA'
                ,'SUGESTAO'
                ,'ACESSO'
                ,'MOVI'
                ,'CLASSE'
            ]

            df_calibrado = df_calibrado[col_ordenar + col_analises]
            df_calibrado.to_excel(Path_dados.retorno, index= False, sheet_name= 'Calibração')
            return True                
        except Exception as e:
            self.validar_erro(e, "CARGA")
            return False
