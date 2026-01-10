from fuctions.path_dados import Path_dados
from fuctions.logica import Logicas
from tkinter import messagebox 
import datetime as dt
import tkinter as tk


class Auxiliar:
    def atualizar_log(self, indice):
    
        self.dados_arquivos = self.logica.carregamento(indice= indice)
        conteudo_completo = f"{'ID':^3} | {'ARQUIVO':^41} | {'DATA':^10} | {'HORA':^8}\n"
        conteudo_completo += f"{'-' * 71}\n"        
        if isinstance(self.dados_arquivos, bool) or self.dados_arquivos is None:
            self.retorno_label.config(text="Erro: Arquivos não carregados.", fg="red")
            return
    
        if self.dados_arquivos is None:
            return 

        for item in self.dados_arquivos:
            nome_arq = item['ARQUIVO']
            if len(nome_arq) > 41:
                nome_arq = nome_arq[:39] + "..."
                
            linha = f"{item['CONTADOR']:02d}  | {nome_arq:<41} | {item['DATA']:<10} | {item['HORAS']:<8}\n"
            conteudo_completo += linha

        self.retorno_label.config(
            text=conteudo_completo, 
            justify="left", 
            anchor="nw",
            font=("Consolas", 10) 
        )
    def BT_iniciar(self):
        root_janela = self.retorno_label.winfo_toplevel()
        self.retorno_label.config(text=" PROCESSANDO DADOS... POR FAVOR, AGUARDE.", fg="#FF640A")
        root_janela.config(cursor="watch")
        root_janela.update_idletasks()
        try:
            inicio_rua = int(self.ent_rua_inicio.get())
            fim_rua = int(self.ent_rua_fim.get())
            
            list_ruas = list(range(inicio_rua, fim_rua + 1))
        except ValueError:
            list_ruas = []

        try:
            inicio_dep = int(self.ent_dep_inicio.get())
            fim_dep = int(self.ent_dep_fim.get())

            list_dep = list(range(inicio_dep-1, fim_dep))
        except ValueError:
            list_dep = []


        self.atualizar_log(list_dep)
        sucesso = self.logica.pipeline(filtro_rua= list_ruas, indice= list_dep)
        if sucesso:
            messagebox.showinfo("CALIBRADOR", "Processo finalizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Ocorreu um erro. Verifique o arquivo log_erros.txt")
        root_janela.config(cursor="")
    def BT_limpar(self):
        self.ent_dep_inicio.delete(0, tk.END)
        self.ent_dep_fim.delete(0, tk.END)
        self.ent_rua_inicio.delete(0, tk.END)
        self.ent_rua_fim.delete(0, tk.END)

        self.retorno_label.config(
            text="Aguardando nova entrada..."
            ,justify= "center"
            ,anchor= "center"
            ,font=("Consolas", 16, "bold")
)
        self.ent_dep_inicio.focus_set()
    def abrir_documentacao(self):
        janela_info = tk.Toplevel()
        janela_info.title("Documentação - Regras de Negócio")
        janela_info.geometry("500x400")
        janela_info.configure(bg=self.backgraund)
        try:
            janela_info.iconbitmap(r"style\sloth_icon.ico")
        except:
            pass
        janela_info.resizable(False, False)

        # Definição dos ícones em Unicode
        icon_calc = "\U0001F4CA"   # Gráfico de barras
        icon_box = "\U0001F4E6"    # Caixa/Pacote
        icon_search = "\U0001F50D" # Lupa

        docs = (
            f"|{f"{icon_calc} REGRAS DE CÁLCULO":<50}\n"
            f"|{'-' * 50}\n"
            "|SUG_%: Sugestão / Norma Palete\n"
            "|ATUAL_%: Capacidade / Norma Palete\n"
            "|SIT_REPOS: 'AJUSTAR' se Ponto Reposição < Giro Dia\n"
            "|CRIT_CAP: 'AJUSTAR' se Giro Dia >= Capacidade\n"
            "|ALERTA_50: 'CAP MENOR' se Giro > 50% da Capacidade\n\n"

            f"|{f"{icon_box} STATUS DO PRODUTO (STATUS_PROD)":<50}\n"
            f"|{'-' * 50}\n"
            "|INT (Inteiro): Até 2 prédios em estruturas\n"
            "|específicas (1.90m ou 2.55m).\n"
            "|DIV (Dividido): Mais de 3 prédios ocupados.\n"
            "|VAL (Validar): Casos intermediários ou fora do padrão.\n\n"

            f"|{f"{icon_search} ANÁLISE DE OCUPAÇÃO":<50}\n"
            f"|{'-' * 50}\n"
            "|FREQ_PROD: Quantidade de prédios onde o produto\n"
            "|foi localizado no mapeamento atual."
        )

        lbl_info = tk.Label(
            janela_info, text=docs, 
            font=("Consolas", 12), 
            fg=self.text_color,
            bg=self.backgraund, 
            justify="left", 
            padx=25, pady=25
        )
        lbl_info.pack(expand=True)
class Calibrador_v1(Auxiliar):
    def __init__(self):
        self.logica = Logicas()

        self.text_color = "#000000"
        self.backgraund = "#87CEFA"
        self.color_segundaria = "#F0FFFF"
        self.borda_color = "#000000"

        self.data_atual = dt.date.today()
        self.data_90 = (self.data_atual - dt.timedelta(days=90))
        self.data_30 = (self.data_atual - dt.timedelta(days=30))

        root = tk.Tk()
        root.title("CALIBRADOR_V1")
        root.geometry("600x400")
        root.iconbitmap(Path_dados.icone)
        root.configure(bg=  self.backgraund)
        root.resizable(False,False)


        self.componente(root)
        self.botoes_layout()
        self.localizador()
        root.mainloop()

    def componente(self, root):
        self.filtros_frame = tk.LabelFrame(
            root
            ,text=" PAINEL DE FILTROS "
            ,font=("Consolas", 11, "bold")
            ,fg=self.text_color
            ,bg=self.backgraund
            ,labelanchor="nw"
            ,relief="solid"
            ,borderwidth=3
            ,highlightthickness=0
        )

        self.quadro_deposito = tk.LabelFrame(
            self.filtros_frame
            ,text=" DEPOSITO "
            ,font=("Consolas", 11, "bold")
            ,fg=self.text_color
            ,bg=self.backgraund
            ,labelanchor="n"
            ,borderwidth= 3
            ,relief="solid"
            ,highlightthickness=0
        )
        self.ent_dep_inicio = tk.Entry(
            self.quadro_deposito
            ,font=("Consolas", 11, "bold")
            ,relief="solid"
            ,borderwidth=3
            ,highlightbackground= self.text_color
        )
        self.ent_dep_fim = tk.Entry(
            self.quadro_deposito
            ,font=("Consolas", 11, "bold")
            ,relief="solid"
            ,borderwidth=3
            ,highlightbackground= self.text_color
        )
        self.text_dep_fim = tk.Label(
            self.quadro_deposito
            ,text="FIM:"
            ,font=("Consolas", 11, "bold")
            ,bg=self.backgraund
            ,fg=self.text_color
            ,anchor= "center"
        )
        self.text_dep_inicio = tk.Label(
            self.quadro_deposito
            , text= "INÍCIO:"
            ,font=("Consolas", 11, "bold")
            ,bg=self.backgraund
            ,fg=self.text_color
            ,anchor= "center"
        )

        self.quadro_ruas = tk.LabelFrame(
            self.filtros_frame
            ,text=" RUAS " 
            ,font=("Consolas", 11, "bold")
            ,fg=self.text_color
            ,bg=self.backgraund
            ,labelanchor="n"
            ,relief="solid"
            ,borderwidth= 3
            ,highlightthickness=0
        )
        self.ent_rua_inicio = tk.Entry(
            self.quadro_ruas
            ,font=("Consolas", 11, "bold")
            ,relief="solid"
            ,borderwidth=3
            ,highlightbackground= self.text_color
        )
        self.ent_rua_fim = tk.Entry(
            self.quadro_ruas
            ,font=("Consolas", 11, "bold")
            ,relief="solid"
            ,borderwidth=3
            ,highlightbackground= self.text_color

        )
        self.text_rua_inicio = tk.Label(
            self.quadro_ruas
            ,text="INÍCIO:"
            ,font=("Consolas", 11, "bold")
            ,bg=self.backgraund
            ,fg=self.text_color
            ,anchor= "center"
        )
        self.text_rua_fim = tk.Label(
            self.quadro_ruas
            ,text= "FIM:"
            ,font=("Consolas", 11, "bold")
            ,fg=self.text_color
            ,bg=self.backgraund
            ,anchor= "center"
        )

        self.retorno_label = tk.Label(
            root
            ,text="Aguardando inicialização..."
            ,font=("Consolas", 11, "bold")
            ,borderwidth=0
            ,highlightthickness=3
            ,highlightbackground=self.text_color
            ,fg=self.text_color
            ,bg=self.color_segundaria
            ,justify="center"
            ,anchor="center"
            ,padx=10
            ,pady=10
        )
        
        self.quadro_sugestao = tk.LabelFrame(
            root
            ,font=("Consolas", 11, "bold")
            ,fg=self.text_color
            ,bg=self.backgraund
            ,labelanchor="n"
            ,borderwidth= 3
            ,relief="solid"
            ,highlightthickness=0

        )
        texto_datas = (
            f"90 DIAS: {self.data_90.strftime('%d/%m/%Y')} até {self.data_atual.strftime('%d/%m/%Y')} | "
            f"30 DIAS: {self.data_30.strftime('%d/%m/%Y')} até {self.data_atual.strftime('%d/%m/%Y')}"
        )
        self.lb_info_datas = tk.Label(
            self.quadro_sugestao
            ,text=texto_datas
            ,font=("Consolas", 10, "bold")
            ,bg=self.backgraund, fg=self.text_color
        )
        # self.lb_info_datas.pack(pady=5)
    def botoes_layout(self):
        self.bt_iniciar = tk.Button(
            self.filtros_frame
            ,text= "INICIAR"
            ,font=("Consolas", 11, "bold")
            ,cursor="hand2"
            ,fg= self.text_color 
            ,bg= self.color_segundaria
            ,highlightbackground= self.text_color
            ,highlightthickness= 3
            ,command= self.BT_iniciar
        )
        self.bt_limpar = tk.Button(
            self.filtros_frame
            ,text= "LIMPAR"
            ,font=("Consolas", 11, "bold")
            ,cursor="hand2"
            ,fg= self.text_color
            ,bg= self.color_segundaria
            ,highlightbackground= self.text_color
            ,highlightthickness= 3
            ,command= self.BT_limpar
        )
        self.bt_documentar = tk.Button(
            self.filtros_frame
            ,text= "INFO"
            ,font=("Consolas", 11, "bold")
            ,cursor="hand2"
            ,fg= self.text_color
            ,bg= self.color_segundaria
            ,highlightbackground= self.text_color
            ,highlightthickness= 3
            ,command= self.abrir_documentacao
        )      
    def localizador(self):
        # Painel de Filtros (Topo)
        self.filtros_frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.35)

        # Sugestão (Divisor central) - Ajustei a altura para 0.05 para economizar espaço
        self.quadro_sugestao.place(relx=0.01, rely=0.37, relwidth=0.98, relheight=0.05)
        self.lb_info_datas.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

        # Retorno (Base) - Ajustei o relheight para 0.56 para caber exatamente na tela (0.44 + 0.56 = 1.0)
        self.retorno_label.place(relx=0.01, rely=0.44, relwidth=0.98, relheight=0.54)

        # --- DENTRO DO filtros_frame ---

        # Quadro Depósito (Ocupando 40%)
        self.quadro_deposito.place(relx=0.02, rely=0.05, relwidth=0.40, relheight=0.80)
        # Ajuste interno (Labels um pouco menores, Entries maiores)
        self.text_dep_inicio.place(relx=0.05, rely=0.10, relwidth=0.30, relheight=0.35)
        self.ent_dep_inicio.place(relx=0.40, rely=0.10, relwidth=0.55, relheight=0.35)
        self.text_dep_fim.place(relx=0.05, rely=0.55, relwidth=0.30, relheight=0.35)
        self.ent_dep_fim.place(relx=0.40, rely=0.55, relwidth=0.55, relheight=0.35)

        # Quadro Ruas (Começa em 0.44 -> 0.40 do anterior + 0.02 de gap + 0.02 margem)
        self.quadro_ruas.place(relx=0.44, rely=0.05, relwidth=0.40, relheight=0.80)
        # Ajuste interno igual ao anterior
        self.text_rua_inicio.place(relx=0.05, rely=0.10, relwidth=0.30, relheight=0.35)
        self.ent_rua_inicio.place(relx=0.40, rely=0.10, relwidth=0.55, relheight=0.35)
        self.text_rua_fim.place(relx=0.05, rely=0.55, relwidth=0.30, relheight=0.35)
        self.ent_rua_fim.place(relx=0.40, rely=0.55, relwidth=0.55, relheight=0.35)

        # Botões (Mantidos na direita, mas levemente alargados para 0.14)
        self.bt_iniciar.place(relx=0.85, rely=0.05, relwidth=0.14, relheight=0.28)
        self.bt_limpar.place(relx=0.85, rely=0.36, relwidth=0.14, relheight=0.28)
        self.bt_documentar.place(relx=0.85, rely=0.67, relwidth=0.14, relheight=0.28)

        self.bt_iniciar.place(relx=0.86, rely=0.02, relwidth=0.13, relheight=0.28)
        self.bt_limpar.place(relx=0.86, rely=0.36, relwidth=0.13, relheight=0.28)
        self.bt_documentar.place(relx=0.86, rely=0.67, relwidth=0.13, relheight=0.28)


if __name__ == '__main__':
    Calibrador_v1()
