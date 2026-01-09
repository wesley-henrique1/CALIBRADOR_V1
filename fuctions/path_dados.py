import os
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    INTERNAL_DIR = sys._MEIPASS
else:
    PASTA_FUNCTIONS = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(PASTA_FUNCTIONS)
    INTERNAL_DIR = BASE_DIR

PASTA_DADOS = os.path.join(BASE_DIR, "base_dados")
FILE_RETORNO = os.path.join(BASE_DIR, 'RETORNO.xlsx')
PASTA_STYLE = os.path.join(INTERNAL_DIR, "style")

class Path_dados:
    icone = os.path.join(PASTA_STYLE, 'flesh_perfil.ico')
    retorno = FILE_RETORNO
                         
    cadastro_8596 = os.path.join(PASTA_DADOS, 'DADOS_PRODUTOS_8596.xlsx')
    acesso_8560 = os.path.join(PASTA_DADOS, 'ACESSO_PROD_8560.xlsx')
    estoque_286 = os.path.join(PASTA_DADOS, 'ESTOQUE_CUSTO_286.xls')
    baixa_8628 = os.path.join(PASTA_DADOS, 'BAIXA_8628.xlsx')
    # Movimentações
    movimentar_1 = os.path.join(PASTA_DADOS, 'MOVIMENTAÇÃO_DEP_1_1782.txt')
    movimentar_2 = os.path.join(PASTA_DADOS, 'MOVIMENTAÇÃO_DEP_2_1782.txt')
    movimentar_3 = os.path.join(PASTA_DADOS, 'MOVIMENTAÇÃO_DEP_3_1782.txt')
    movimentar_4 = os.path.join(PASTA_DADOS, 'MOVIMENTAÇÃO_DEP_4_1782.txt')
    # Sugestões
    sugestao_1 = os.path.join(PASTA_DADOS, 'SUGESTÃO_DEP_1_1782.txt')
    sugestao_2 = os.path.join(PASTA_DADOS, 'SUGESTÃO_DEP_2_1782.txt')
    sugestao_3 = os.path.join(PASTA_DADOS, 'SUGESTÃO_DEP_3_1782.txt')
    sugestao_4 = os.path.join(PASTA_DADOS, 'SUGESTÃO_DEP_4_1782.txt')
    

