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
        root.configure(bg= "#061857")
        root.iconbitmap(r"style\sloth_icon.ico")

        self.tela(root)
        root.mainloop()


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
    def BT_limpar(self):
        self.filtro_rua.delete(0, tk.END)
        self.tela_principal.config(text="Aguardando nova entrada...")
        self.filtro_rua.focus_set()


    def tela(self, root):
        self.filtro_rua = tk.Entry(
            root,bg= self.primaria
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
        self.tela_principal = tk.Label(
            root, bg= self.primaria, text="Aguardando inicialização..."
            ,font=("Consolas", 10)
            ,highlightthickness= 2
            ,highlightbackground=self.segundaria
            ,justify= "center"
            ,anchor= "center"
            ,padx=10, pady=10
        )


        self.filtro_rua.place(relx= 0.01, rely= 0.02, relheight= 0.10, relwidth= 0.65)
        self.bt_iniciar.place(relx= 0.68, rely= 0.02, relheight= 0.10, relwidth= 0.15)
        self.bt_limpar.place(relx= 0.84, rely= 0.02, relheight= 0.10, relwidth= 0.15)
        self.tela_principal.place(relx= 0.01, rely= 0.15, relheight= 0.82, relwidth= 0.98)

if __name__ == '__main__':
    Calibrador_v1()