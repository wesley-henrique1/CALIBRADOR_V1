from fuctions.path_dados import Path_dados
from fuctions.logica import Logicas
from tkinter import messagebox 
import datetime as dt
import tkinter as tk
import threading


class Auxiliar:
    def finalizar_ui(self, sucesso):
        root_janela = self.retorno_label.winfo_toplevel()
        root_janela.config(cursor="")

        self.bt_iniciar.config(state="normal")
        self.bt_limpar.config(state="normal")

        if sucesso:
            messagebox.showinfo("CALIBRADOR", "Processo finalizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Ocorreu um erro. Verifique o arquivo log_erros.txt")
    def processamento(self, list_dep, list_ruas):
        try:
            root_janela = self.retorno_label.winfo_toplevel()
            root_janela.after(0, lambda: self.atualizar_log(list_dep))

            sucesso = self.logica.pipeline(filtro_rua=list_ruas, indice=list_dep)
            root_janela.after(0, lambda: self.finalizar_ui(sucesso))
        except Exception as e:
            self.logica.validar_erro(e, "THREAD_PROCESSAMENTO")
    def atualizar_log(self, indice):
        self.dados_arquivos = self.logica.carregamento(indice= indice)
        conteudo_completo = f"{'ID':^3} | {'ARQUIVO':^40} | {'DATA':^10} | {'HORA':^8}\n"
        conteudo_completo += f"{'-' * 71}\n" 

        if isinstance(self.dados_arquivos, bool) or self.dados_arquivos is None:
            self.retorno_label.config(text="Erro: Arquivos não carregados.", fg="red")
            return
        
        if self.dados_arquivos is None:
            return 

        for item in self.dados_arquivos:
            nome_arq = item['ARQUIVO']
            if len(nome_arq) > 40:
                nome_arq = nome_arq[:35] + "..."
                
            linha = f"{item['CONTADOR']:02d}  | {nome_arq:<40} | {item['DATA']:<10} | {item['HORAS']:<8}\n"
            conteudo_completo += linha

        self.retorno_label.config(
            text=conteudo_completo, 
            justify="left", 
            anchor="nw",
            font=("Consolas", 11) 
        )
    def BT_iniciar(self):
        root_janela = self.retorno_label.winfo_toplevel()
        try:
            inicio_rua = int(self.ent_rua_inicio.get())
            fim_rua = int(self.ent_rua_fim.get())
            list_ruas = list(range(inicio_rua, fim_rua + 1))

            inicio_dep = int(self.ent_dep_inicio.get())
            fim_dep = int(self.ent_dep_fim.get())
            list_dep = list(range(inicio_dep-1, fim_dep))
            
            self.retorno_label.config(text=" PROCESSANDO DADOS... POR FAVOR, AGUARDE.", fg="#EE7600")
            root_janela.config(cursor="watch")
            self.bt_iniciar.config(state="disabled")
            self.bt_limpar.config(state="disabled")

            threading.Thread(
                target=self.processamento, 
                args=(list_dep, list_ruas), 
                daemon=True
            ).start()
        except ValueError:
            messagebox.showwarning("Atenção", "Por favor, insira valores numéricos válidos.")
            root_janela.config(cursor="")
            return
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
        janela_info.geometry("560x460")
        janela_info.configure(bg=self.backgraund)
        try:
            janela_info.iconbitmap(r"style\sloth_icon.ico")
        except:
            pass
        janela_info.resizable(False, False)

        icon_calc = "\U0001F4CA"
        icon_box = "\U0001F4E6"
        icon_search = "\U0001F50D"
        icon_data = "\U0001F4C2"

        docs = (
            f"|{f'{icon_calc} MÉTRICAS DE SUPORTE (BASE)':<50}\n"
            f"|{'-' * 50}\n"
            "|MED_RUA: Média de acessos (giro) da rua analisada.\n"
            "|PR_MEIO: Define o limite físico dos 30% iniciais (Início).\n"
            "|SUG_%: % da Sugestão em relação à Norma Palete.\n"
            "|ATUAL_%: % da Capacidade em relação à Norma Palete.\n"
            "|FREQ_PROD: Qtd. de endereços ocupados pelo produto.\n\n"

            f"|{f'{icon_search} KPIS DE DECISÃO (ALERTAS)':<50}\n"
            f"|{'-' * 50}\n"
            "|SIT_REPOS: Alerta se Ponto Reposição < Giro Dia.\n"
            "|CRIT_CAP: Alerta se Giro Dia >= Capacidade Física.\n"
            "|ALERTA_50: Alerta se Giro > 50% da Capacidade.\n"
            "|ALERTA_MOV: Identifica erro de posicionamento logístico\n"
            "(Lento na ponta OU Rápido no fundo).\n\n"

            f"|{f'{icon_box} STATUS & CLASSIFICAÇÃO':<50}\n"
            f"|{'-' * 50}\n"
            "|MED_ACESSO: Classifica giro (Acima/Abaixo) da média da rua.\n"
            "|STATUS_PROD: INT (Inteiro), DIV (Dividido), VAL (Validar).\n"
            "|STATUS_FINAL: Indicador macro de divergência na rua.\n\n"

            f"|{f'{icon_data} ORIGEM DOS DADOS (COLUNAS NECESSÁRIAS)':<50}\n"
            f"|{'-' * 50}\n"
            "|ROT. 8596 (Endereço): CODPROD, RUA, PREDIO, APTO, CAPACIDADE,\n"
            "PONTOREPOSICAO, QTTOTPAL, QTUNITCX, PK_END\n"
            "|ROT. 8560 (Separação): CODPROD, QTOS, QT\n"
            "|ROT. 286  (Estoque): Estoque, Custo, Qt.Bloq, Avaria\n"
            "|ROT. 8628 (WMS): NIVEL, NIVEL_1, CODROTINA, Tipo O.S."
        )
        txt_info = tk.Text(
            janela_info
            ,font=("Consolas", 12)
            ,fg=self.segunda_cor
            ,bg=self.backgraund
            ,bd=1
            ,highlightthickness=0
            ,wrap="word"
            ,padx=5
            ,pady=5
        )
        txt_info.insert("1.0", docs)
        txt_info.configure(state="disabled")
        txt_info.pack(expand=True, fill="both")
class Calibrador_v1(Auxiliar):
    def __init__(self):
        self.logica = Logicas()

        self.backgraund = "#2F4F4F"
        self.primeira_cor = "#000000"
        self.segunda_cor = "#F0FFFF"

        self.data_atual = dt.date.today()
        self.data_90 = (self.data_atual - dt.timedelta(days=90))
        self.data_30 = (self.data_atual - dt.timedelta(days=30))

        root = tk.Tk()
        root.title("CALIBRADOR_V2")
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
            ,fg=self.segunda_cor
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
            ,fg=self.segunda_cor
            ,bg=self.backgraund
            ,labelanchor="n"
            ,borderwidth= 3
            ,relief="solid"
            ,highlightthickness=0
        )
        self.ent_dep_inicio = tk.Entry(
            self.quadro_deposito
            ,font=("Consolas", 10, "bold")
            ,relief="solid"
            ,borderwidth=3
            ,highlightbackground= self.segunda_cor
        )
        self.ent_dep_fim = tk.Entry(
            self.quadro_deposito
            ,font=("Consolas", 10, "bold")
            ,relief="solid"
            ,borderwidth=3
            ,highlightbackground= self.segunda_cor
        )
        self.text_dep_fim = tk.Label(
            self.quadro_deposito
            ,text="FIM:"
            ,font=("Consolas", 10, "bold")
            ,bg=self.backgraund
            ,fg=self.segunda_cor
            ,anchor= "center"
        )
        self.text_dep_inicio = tk.Label(
            self.quadro_deposito
            , text= "INÍCIO:"
            ,font=("Consolas", 10, "bold")
            ,bg=self.backgraund
            ,fg=self.segunda_cor
            ,anchor= "center"
        )

        self.quadro_ruas = tk.LabelFrame(
            self.filtros_frame
            ,text=" RUAS " 
            ,font=("Consolas", 11, "bold")
            ,fg=self.segunda_cor
            ,bg=self.backgraund
            ,labelanchor="n"
            ,relief="solid"
            ,borderwidth= 3
            ,highlightthickness=0
        )
        self.ent_rua_inicio = tk.Entry(
            self.quadro_ruas
            ,font=("Consolas", 10, "bold")
            ,relief="solid"
            ,borderwidth=3
            ,highlightbackground= self.primeira_cor
        )
        self.ent_rua_fim = tk.Entry(
            self.quadro_ruas
            ,font=("Consolas", 10, "bold")
            ,relief="solid"
            ,borderwidth=3
            ,highlightbackground= self.primeira_cor

        )
        self.text_rua_inicio = tk.Label(
            self.quadro_ruas
            ,text="INÍCIO:"
            ,font=("Consolas", 10, "bold")
            ,bg=self.backgraund
            ,fg=self.segunda_cor
            ,anchor= "center"
        )
        self.text_rua_fim = tk.Label(
            self.quadro_ruas
            ,text= "FIM:"
            ,font=("Consolas", 10, "bold")
            ,fg=self.segunda_cor
            ,bg=self.backgraund
            ,anchor= "center"
        )

        
        self.quadro_sugestao = tk.LabelFrame(
            self.filtros_frame
            ,text=" DATA " 
            ,font=("Consolas", 11, "bold")
            ,fg=self.segunda_cor
            ,bg=self.backgraund
            ,labelanchor="n"
            ,relief="solid"
            ,borderwidth= 3
            ,highlightthickness=0
        )
        self.text_30 = tk.Label(
            self.quadro_sugestao
            ,text=f"30 Dias >> {self.data_30.strftime('%d/%m/%Y')}"
            ,font=("Consolas", 10, "bold")
            ,fg=self.segunda_cor
            ,bg=self.backgraund
            ,anchor="center"
            ,borderwidth=2
            ,relief="groove"
        )
        self.text_90 = tk.Label(
            self.quadro_sugestao
            ,text=f"90 Dias >> {self.data_90.strftime('%d/%m/%Y')}"
            ,font=("Consolas", 10, "bold")
            ,fg=self.segunda_cor
            ,bg=self.backgraund
            ,anchor="center"
            ,borderwidth=2
            ,relief="groove"
        )
        self.retorno_label = tk.Label(
            root
            ,text="Aguardando inicialização..."
            ,font=("Consolas", 11, "bold")
            ,borderwidth=0
            ,highlightthickness=3
            ,highlightbackground=self.primeira_cor
            ,fg=self.segunda_cor
            ,bg=self.segunda_cor
            ,justify="center"
            ,anchor="center"
            ,padx=10
            ,pady=10
        )
    def botoes_layout(self):
        self.bt_iniciar = tk.Button(
            self.filtros_frame
            ,text= "INICIAR"
            ,font=("Consolas", 11, "bold")
            ,cursor="hand2"
            ,fg= self.primeira_cor 
            ,bg= self.segunda_cor
            ,highlightbackground= self.primeira_cor
            ,highlightthickness= 3
            ,command= self.BT_iniciar
            ,
        )
        self.bt_limpar = tk.Button(
            self.filtros_frame
            ,text= "LIMPAR"
            ,font=("Consolas", 11, "bold")
            ,cursor="hand2"
            ,fg= self.primeira_cor 
            ,bg= self.segunda_cor
            ,highlightbackground= self.primeira_cor
            ,highlightthickness= 3
            ,command= self.BT_limpar
        )
        self.bt_documentar = tk.Button(
            self.filtros_frame
            ,text= "INFO"
            ,font=("Consolas", 11, "bold")
            ,cursor="hand2"
            ,fg= self.primeira_cor 
            ,bg= self.segunda_cor
            ,highlightbackground= self.primeira_cor
            ,highlightthickness= 3
            ,command= self.abrir_documentacao
        )      
        
        self.bt_iniciar.bind("<Return>", lambda e: self.bt_iniciar.invoke())
        self.bt_limpar.bind("<Return>", lambda e: self.bt_limpar.invoke())
        self.bt_documentar.bind("<Return>", lambda e: self.bt_documentar.invoke())
    def localizador(self):
        # Painel de Filtros (Topo)
        self.filtros_frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.42)
        self.retorno_label.place(relx=0.01, rely=0.44, relwidth=0.98, relheight=0.54)

        # --- DENTRO DO filtros_frame ---
        self.quadro_deposito.place(relx=0.02, rely=0.05, relwidth=0.25, relheight=0.60)
        self.quadro_ruas.place(relx=0.34, rely=0.05, relwidth=0.25, relheight=0.60)
        self.quadro_sugestao.place(relx=0.66, rely=0.05, relwidth=0.30, relheight=0.60)

        # Quadro Sugestão
        self.text_30.place(relx=0.02, rely=0.10, relwidth=0.98, relheight=0.40)
        self.text_90.place(relx=0.02, rely=0.50, relwidth=0.98, relheight=0.40)

        # Quadro Depósito
        self.ent_dep_inicio.place(relx=0.60, rely=0.10, relwidth=0.30, relheight=0.30)
        self.ent_dep_fim.place(relx=0.60, rely=0.55, relwidth=0.30, relheight=0.30)
        self.text_dep_inicio.place(relx=0.15, rely=0.10, relwidth=0.40, relheight=0.35)
        self.text_dep_fim.place(relx=0.15, rely=0.55, relwidth=0.40, relheight=0.35)

        # Quadro Ruas
        self.ent_rua_inicio.place(relx=0.60, rely=0.10, relwidth=0.30, relheight=0.30)
        self.ent_rua_fim.place(relx=0.60, rely=0.55, relwidth=0.30, relheight=0.30)
        self.text_rua_inicio.place(relx=0.15, rely=0.10, relwidth=0.40, relheight=0.35)
        self.text_rua_fim.place(relx=0.15, rely=0.55, relwidth=0.40, relheight=0.35)

        # Botões
        self.bt_iniciar.place(relx=0.49, rely=0.75, relwidth=0.15, relheight=0.20)
        self.bt_limpar.place(relx=0.65, rely=0.75, relwidth=0.15, relheight=0.20)
        self.bt_documentar.place(relx=0.81, rely=0.75, relwidth=0.15, relheight=0.20)

if __name__ == '__main__':
    Calibrador_v1()
