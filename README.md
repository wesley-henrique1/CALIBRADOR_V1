# CALIBRADOR_V1

### pasta unica
python -m PyInstaller --onefile --noconsole --name=CALIBRADOR_V1 --icon=style/favicon.ico --paths=. --paths=base_dados main.py

### mutipasta
python -m PyInstaller --onedir --noconsole --name=CALIBRADOR_V1 --icon=style/favicon.ico --paths=. --paths=base_dados main.py

Documentação do Processo de Consolidação e Análise de Estoque

1. Objetivo
    O objetivo desta aplicação é centralizar informações de diferentes fontes (.xlsx e .txt) para realizar a análise de ocupação, giro e status de armazenagem dos produtos. A base principal de consolidação é o arquivo 8596 - dados_prod.

2. Integração de Dados (ETL)
    A unificação dos dados é realizada através de um cruzamento (Join) utilizando a chave primária:

    Chave de Ligação: CODPROD (Código do Produto).

    Fontes: Arquivos variados em formatos Excel e Texto.

3. Regras de Negócio (Colunas Calculadas)
    Abaixo estão as métricas calculadas para a validação do estoque e capacidade:

    SUG_%	
    SUGESTÃO / NORMA PALETE	
    Percentual da sugestão em relação à norma do palete.

    ATUAL_%	
    CAPACIDADE / NORMA PALETE	
    Percentual de ocupação atual em relação à norma do palete.

    SIT_REPOS	
    Se PONTOREPOSICAO < 1_DIA então "MENOR", senão "NORMAL"	
    Identifica se o ponto de reposição está abaixo do consumo diário.

    CRIT_CAP	
    Se GIRO DIA >= CAPACIDADE então "ALERTA", senão "NORMAL"	
    Valida se o giro diário ultrapassa a capacidade física.

    ALERTA_50	   
    Se GIRO_DIA_1 == "NORMAL" E (GIRO_DIA / CAPACIDADE) > 0.5 então "CAP MENOR", senão "NORMAL"	
    Refinamento para identificar produtos com capacidade crítica.

    FREQ_PROD	    
    Contagem de prédios encontrados	    
    Totalizador de endereços/prédios ocupados pelo produto.

4. Classificação de Status (CLASSE_LOC)
    Esta lógica define a ocupação física do produto no armazém com base na estrutura e quantidade de produtos por prédio:

    INT (Inteiro): * Condição: CONT_AP > 2 E Estrutura pertence a ('2-INTEIRO(1,90)', '1-INTEIRO (2,55)').

    Significado: Indica que o prédio está sendo utilizado em sua totalidade por apenas 1 ou 2 produtos.

    DIV (Dividido):

    Condição: CONT_AP > 3.