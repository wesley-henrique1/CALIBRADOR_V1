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
    estoque_286 = os.path.join(PASTA_DADOS, 'ESTOQUE_CUSTO.xls')
    acesso_8560 = os.path.join(PASTA_DADOS, 'ACESSO_PROD.xlsx')
    cadastro_8596 = os.path.join(PASTA_DADOS, 'DADOS_PRODUTOS.xlsx')

    # Sugestões
    sugestao_1 = os.path.join(PASTA_DADOS, 'SUGESTÃO_DEP_1.txt')
    sugestao_2 = os.path.join(PASTA_DADOS, 'SUGESTÃO_DEP_1.txt')
    sugestao_3 = os.path.join(PASTA_DADOS, '1782 - Sugestão DEP_3.txt')
    sugestao_4 = os.path.join(PASTA_DADOS, '1782 - Sugestão DEP_4.txt')

    # Movimentações
    movimentar_1 = os.path.join(PASTA_DADOS, '1782 - Movimentação DEP_1.txt')
    movimentar_2 = os.path.join(PASTA_DADOS, '1782 - Movimentação DEP_2.txt')
    movimentar_3 = os.path.join(PASTA_DADOS, '1782 - Movimentação DEP_3.txt')
    movimentar_4 = os.path.join(PASTA_DADOS, '1782 - Movimentação DEP_4.txt')
    retorno = FILE_RETORNO
   