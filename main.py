from logica import Logicas
from tkinter import messagebox 
import tkinter as tk


class Calibrador_v1:
    def __init__(self):
        self.logica = Logicas()

        self.primaria = "#f5eded"
        self.segundaria = "#0a0a0a"
        self.terceiria = "#061857"

        root = tk.Tk()
        root.title("CALIBRADOR_V1")
        root.geometry("540x300")
        root.configure(bg=  self.terceiria)
        root.iconbitmap(r"style\sloth_icon.ico")
        root.resizable(False,False)

        self.tela(root)
        root.mainloop()

    def documentar(self):
        """
        1. Objetivo
            O objetivo desta aplicação é centralizar informações de diferentes fontes (.xlsx e .txt) para realizar a análise de ocupação, giro e status de armazenagem dos produtos. A base principal de consolidação é o arquivo 8596 - dados_prod.

        2. Integração de Dados (ETL)
            A unificação dos dados é realizada através de um cruzamento (Join) utilizando a chave primária:

            Chave de Ligação: CODPROD (Código do Produto).

            Fontes: Arquivos variados em formatos Excel e Texto.
        3. Regras de Negócio (Colunas Calculadas)
            Abaixo estão as métricas calculadas para a validação do estoque e capacidade:
            Coluna  Regra/Cálculo           Descrição
            SUG_%   SUGESTÃO/NORMAPALETE    Percentual da sugestão em relação à norma do palete.ATUAL_%CAPACIDADE / NORMA PALETEPercentual de ocupação atual em relação à norma do palete.ANALISESe PONTOREPOSICAO < 1_DIA então "MENOR", senão "NORMAL"Identifica se o ponto de reposição está abaixo do consumo diário.GIRO_DIA_1Se GIRO DIA >= CAPACIDADE então "ALERTA", senão "NORMAL"Valida se o giro diário ultrapassa a capacidade física.GIRO_DIA_2Se GIRO_DIA_1 == "NORMAL" E (GIRO_DIA / CAPACIDADE) > 0.5 então "CAP MENOR", senão "NORMAL"Refinamento para identificar produtos com capacidade crítica.CONT_APContagem de prédios encontradosTotalizador de endereços/prédios ocupados pelo produto.
        """

    def atualizar_log(self):
        dados_arquivos = self.logica.carregamento()
        conteudo_completo = f"{"ID":^2} | {"ARQUIVO":^41} | {"DATA":^10} | {"HORAS":^8}\n {"-" * 70}\n"

        for i in range(len(dados_arquivos)):
            item = dados_arquivos[i]
            linha = f"{item['CONTADOR']:02d} | {item['ARQUIVO']:<41} | {item['DATA']:<10} | {item["HORAS"]:<8}\n"
            conteudo_completo += linha
        self.tela_principal.config(text=conteudo_completo, justify="left", anchor="nw")
    def BT_iniciar(self):
        self.atualizar_log()

        entrada_user = self.filtro_rua.get()
        list_ruas = entrada_user.split()
        sucesso = self.logica.pipeline(list_ruas)
        if sucesso:
            messagebox.showinfo("CALIBRADOR", "Processo finalizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Ocorreu um erro. Verifique o arquivo log_erros.txt")
    def abrir_documentacao(self):
        # Cria a janela pop-up
        janela_info = tk.Toplevel()
        janela_info.title("Documentação - Regras de Negócio")
        janela_info.geometry("500x450")
        janela_info.configure(bg=self.primaria)
        janela_info.iconbitmap(r"style\sloth_icon.ico")
        janela_info.resizable(False, False)

        docs = (
            f"|{"\U0001F4CA REGRAS DE CÁLCULO":<46}\n"
            f"|{"-" * 46}\n"
             "|SUG_%: Sugestão / Norma Palete\n"
             "|ATUAL_%: Capacidade / Norma Palete\n"
             "|ANALISE: 'MENOR' se Reposição < 1 dia de giro\n\n"
            f"|{"\U0001F4E6 STATUS DO PRODUTO (STATUS_PROD)":<46}\n"
            f"|{"-" * 46}\n"
             "|INT (Inteiro): Prédio com 1 ou 2 produtos em\n"
             "|estruturas de 1,90m ou 2,55m.\n\n"
             "|DIV (Dividido): Prédio com 3+ produtos ou\n"
             "|presença de prateleiras.\n\n"
            f"|{"CONTAGEM":<46}\n"
            f"|{"-" * 46}\n"
             "|CONT_AP: Total de prédios onde o produto\n"
             "|foi localizado."
        )

        # Exibindo o texto em um Label amigável
        lbl_info = tk.Label(
            janela_info, text=docs, 
            font=("Consolas", 14), 
            fg=self.terceiria, # Usando suas variáveis de cor
            bg=self.primaria, 
            justify="left", 
            padx=20, pady=20
        )
        lbl_info.pack(expand=True)
    def BT_limpar(self):
        self.filtro_rua.delete(0, tk.END)
        self.tela_principal.config(text="Aguardando nova entrada...")
        self.filtro_rua.focus_set()


    def tela(self, root):
        self.text_filter = tk.Label(
            root, bg=  self.terceiria, text= "Informe as ruas separadas por espaço (ex: 1 5 10) \U000021C9"
            ,font=("Verdana", 10), fg= self.primaria
            ,justify= "left"
            ,anchor= "center"
        )
        self.filtro_rua = tk.Entry(
            root, bg= self.primaria
            ,highlightthickness= 2, highlightbackground= self.segundaria
        )
        self.bt_iniciar = tk.Button(
            root, bg= self.primaria
            ,cursor="hand2", command= self.BT_iniciar
            ,text= "INICIAR",fg= self.terceiria 
            ,highlightthickness= 2, highlightbackground= self.segundaria
        )
        self.bt_limpar = tk.Button(
            root, bg= self.primaria
            ,cursor="hand2", command= self.BT_limpar
            ,text= "LIMPAR", fg= self.terceiria
            ,highlightthickness= 2, highlightbackground= self.segundaria
        )
        self.bt_documentar = tk.Button(
            root, bg= self.primaria
            ,cursor="hand2", command= self.abrir_documentacao
            ,text= "INFO", fg= self.terceiria
            ,highlightthickness= 2, highlightbackground= self.segundaria
        )
        self.tela_principal = tk.Label(
            root, bg= self.primaria, text="Aguardando inicialização..."
            ,font=("Verdana", 10), fg= self.segundaria
            ,highlightthickness= 2, highlightbackground=self.segundaria
            ,justify= "center", anchor= "center"
            ,padx=10, pady=10
        )

        self.text_filter.place(relx= 0.01, rely= 0.01, relheight= 0.06, relwidth= 0.67)
        self.filtro_rua.place(relx= 0.68, rely= 0.01, relheight= 0.06, relwidth= 0.31)

        self.bt_iniciar.place(relx= 0.04, rely= 0.08, relheight= 0.06, relwidth= 0.28)
        self.bt_limpar.place(relx= 0.36, rely= 0.08, relheight= 0.06, relwidth= 0.28)
        self.bt_documentar.place(relx= 0.68, rely= 0.08, relheight= 0.06, relwidth= 0.28)

        self.tela_principal.place(relx= 0.01, rely= 0.15, relheight= 0.82, relwidth= 0.98)

if __name__ == '__main__':
    Calibrador_v1()