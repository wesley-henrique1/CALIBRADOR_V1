import os
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    ARQUIVO_ATUAL = os.path.abspath(__file__)
    PASTA_DO_SCRIPT = os.path.dirname(ARQUIVO_ATUAL)
    BASE_DIR = os.path.dirname(PASTA_DO_SCRIPT)

PASTA_DADOS = os.path.join(BASE_DIR, "base_dados")
FILE_RETORNO = os.path.join(BASE_DIR, 'RETORNO.xlsx')

class Path_dados:
    cadastro_8596 = os.path.join(PASTA_DADOS, 'DADOS_PRODUTOS_8596.xlsx')
    acesso_8560 = os.path.join(PASTA_DADOS, 'ACESSO_PROD_8560.xlsx')
    estoque_286 = os.path.join(PASTA_DADOS, 'ESTOQUE_CUSTO_286.xls')
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
    retorno = FILE_RETORNO