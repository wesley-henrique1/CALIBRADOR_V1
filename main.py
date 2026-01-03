from logica import Logicas
from tkinter import messagebox 
import tkinter as tk

class Auxiliar:
    def atualizar_log(self):
        itens_movi = [0]
        itens_sug = [0]
        self.dados_arquivos = self.logica.carregamento(itens_movi, itens_sug)
        conteudo_completo = f"{'ID':^3} | {'ARQUIVO':^41} | {'DATA':^10} | {'HORA':^8}\n"
        conteudo_completo += f"{'-' * 71}\n"
        
        if self.dados_arquivos is None:
            return 

        for item in self.dados_arquivos:
            nome_arq = item['ARQUIVO']
            if len(nome_arq) > 30:
                nome_arq = nome_arq[:27] + "..."
                
            linha = f"{item['CONTADOR']:02d}  | {nome_arq:<41} | {item['DATA']:<10} | {item['HORAS']:<8}\n"
            conteudo_completo += linha

        self.retorno_label.config(
            text=conteudo_completo, 
            justify="left", 
            anchor="nw",
            font=("Consolas", 10) 
        )
    def BT_iniciar(self):
        self.atualizar_log()

        entrada_user = self.filtro_rua.get()
        list_ruas = entrada_user.split()
        sucesso = self.logica.pipeline(list_ruas)
        if sucesso:
            messagebox.showinfo("CALIBRADOR", "Processo finalizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Ocorreu um erro. Verifique o arquivo log_erros.txt")
    def BT_limpar(self):
        self.filtro_rua.delete(0, tk.END)
        self.retorno_label.config(text="Aguardando nova entrada...")
        self.filtro_rua.focus_set()
    def abrir_documentacao(self):
        # Cria a janela pop-up
        janela_info = tk.Toplevel()
        janela_info.title("Documentação - Regras de Negócio")
        janela_info.geometry("500x400")
        janela_info.configure(bg=self.primaria)
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
            fg=self.terceiria,
            bg=self.primaria, 
            justify="left", 
            padx=25, pady=25
        )
        lbl_info.pack(expand=True)
class Calibrador_v1(Auxiliar):
    def __init__(self):
        self.logica = Logicas()

        self.primaria = "#f5eded"
        self.segundaria = "#0a0a0a"
        self.terceiria = "#061857"

        root = tk.Tk()
        root.title("CALIBRADOR_V1")
        root.geometry("540x400")
        root.configure(bg=  self.terceiria)
        root.iconbitmap(r"style\sloth_icon.ico")
        root.resizable(False,False)

        self.componente(root)
        self.botoes_layout()
        
        root.mainloop()

    def componente(self, root):
        """
        Mudar a forma de consultas, vou criar dois entry para inicio e fim, depois separar com o loop
        ADD outras duas entry para filtrar o depositos e seguir a mesma logica
        """
        self.filtros_frame = tk.LabelFrame(
            root, 
            text=" PAINEL DE FILTROS ", 
            font=("Consolas", 10, "bold"),
            fg=self.primaria,          # Cor do texto (corta a borda)
            bg=self.terceiria,         # Cor de fundo interna
            labelanchor="nw",          
            
            # Configuração correta para a borda com texto:
            borderwidth= 3,             # A espessura da linha que o texto corta
            relief="groove",           # Estilo que permite ver a borda claramente
            highlightthickness=0       # Removemos o highlight para não sobrepor o texto
        )
        # Labels e Entrys para o intervalo de depósitos
        self.text_dep_inicio = tk.Label(
            self.filtros_frame, text= "DEP. INÍCIO:"
            ,font=("Consolas", 9)
            ,bg=self.terceiria, fg=self.primaria
        )
        self.ent_dep_inicio = tk.Entry(
            self.filtros_frame, font=("Consolas", 11)
        )
        self.text_dep_fim = tk.Label(
            self.filtros_frame, text="DEP. FIM:"
            ,font=("Consolas", 9)
            ,bg=self.terceiria, fg=self.primaria
        )
        self.ent_dep_fim = tk.Entry(
            self.filtros_frame, font=("Consolas", 11)
        )
        self.text_rua_inicio = tk.Label(
            self.filtros_frame, text="RUA INÍCIO:"
            ,font=("Consolas", 9)
            ,bg=self.terceiria, fg=self.primaria
        )
        self.ent_rua_inicio = tk.Entry(
            self.filtros_frame, font=("Consolas", 11)
        )
        self.text_rua_fim = tk.Label(
            self.filtros_frame, text="RUA FIM:"
            ,font=("Consolas", 9)
            ,bg=self.terceiria, fg=self.primaria
        )
        self.ent_rua_fim = tk.Entry(
            self.filtros_frame, font=("Consolas", 11)
        )
        self.retorno_label = tk.Label(
            root, bg= self.primaria, text="Aguardando inicialização..."
            ,font=("Verdana", 10), fg= self.segundaria
            ,highlightthickness= 3, highlightbackground=self.segundaria
            ,justify= "center", anchor= "center"
            ,padx=10, pady=10
        )
    

        #  LOCALIZAÇÃO
        self.filtros_frame.place(relx= 0.01, rely= 0.01, relheight= 0.30, relwidth= 0.98)

        self.text_dep_inicio.place(relx=0.01, rely=0.05,relheight=0.22, relwidth=0.20)
        self.ent_dep_inicio.place(relx=0.01, rely=0.25,relheight=0.22, relwidth=0.20)

        self.text_rua_inicio.place(relx=0.01, rely=0.47,relheight=0.22, relwidth=0.20)
        self.ent_rua_inicio.place(relx=0.01, rely=0.65,relheight=0.22, relwidth=0.20)

        self.text_dep_fim.place(relx=0.25, rely=0.05,relheight=0.22, relwidth=0.20)
        self.ent_dep_fim.place(relx=0.25, rely=0.25,relheight=0.22, relwidth=0.20)

        self.text_rua_fim.place(relx=0.25, rely=0.47, relheight=0.22, relwidth=0.20)
        self.ent_rua_fim.place(relx=0.25, rely=0.65, relheight=0.22, relwidth=0.20)


        self.retorno_label.place(relx= 0.01, rely= 0.40, relheight= 0.58, relwidth= 0.98)
    def botoes_layout(self):
        self.bt_iniciar = tk.Button(
            self.filtros_frame, bg= self.primaria
            ,cursor="hand2", command= self.BT_iniciar
            ,text= "INICIAR",fg= self.terceiria 
            ,highlightthickness= 2, highlightbackground= self.segundaria
        )
        self.bt_limpar = tk.Button(
            self.filtros_frame, bg= self.primaria
            ,cursor="hand2", command= self.BT_limpar
            ,text= "LIMPAR", fg= self.terceiria
            ,highlightthickness= 2, highlightbackground= self.segundaria
        )
        self.bt_documentar = tk.Button(
            self.filtros_frame, bg= self.primaria
            ,cursor="hand2", command= self.abrir_documentacao
            ,text= "INFO", fg= self.terceiria
            ,highlightthickness= 2, highlightbackground= self.segundaria
        )
    
        self.bt_iniciar.place(relx=0.77, rely=0.17, relheight=0.24, relwidth=0.22)
        self.bt_limpar.place(relx=0.77, rely=0.46, relheight=0.24, relwidth=0.22)
        self.bt_documentar.place(relx=0.77, rely=0.75, relheight=0.24, relwidth=0.22)

if __name__ == '__main__':
    Calibrador_v1()