import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from .separador import carregar_keywords, salvar_keywords, separar_arquivos_em_pastas, get_output_directory
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Separador de PDFs")
        self.geometry("600x500")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.selected_folder = ""
        self.keywords = carregar_keywords()

        self._setup_ui()

    def _setup_ui(self):
        self.label = ctk.CTkLabel(self, text="Selecione a pasta com os PDFs:")
        self.label.pack(pady=10)

        self.select_button = ctk.CTkButton(self, text="Selecionar Pasta", command=self.selecionar_pasta)
        self.select_button.pack()

        self.folder_label = ctk.CTkLabel(self, text="Nenhuma pasta selecionada", text_color="gray")
        self.folder_label.pack(pady=5)

        self.run_button = ctk.CTkButton(self, text="Executar Separação", command=self.executar_em_thread)
        self.run_button.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.set(0)
        self.progress.pack(pady=10)

        self.kw_label = ctk.CTkLabel(self, text="Palavras-chave:")
        self.kw_label.pack(pady=10)

        self.kw_listbox = ctk.CTkTextbox(self, width=400, height=150)
        self.kw_listbox.pack()
        self.atualizar_lista_keywords()

        self.save_button = ctk.CTkButton(self, text="Salvar Lista", command=self.salvar_lista_keywords)
        self.save_button.pack(pady=5)

        self.remove_button = ctk.CTkButton(self, text="Remover Selecionada", command=self.remover_keyword)
        self.remove_button.pack(pady=5)

        self.abrir_pasta_button = ctk.CTkButton(self, text="Abrir Pasta de Destino", command=self.abrir_pasta_destino)
        self.abrir_pasta_button.pack(pady=5)

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.selected_folder = pasta
            self.folder_label.configure(text=pasta, text_color="green")
        else:
            self.folder_label.configure(text="Nenhuma pasta selecionada", text_color="red")

    def executar_em_thread(self):
        if not self.selected_folder:
            messagebox.showwarning("Aviso", "Selecione uma pasta primeiro.")
            return
        threading.Thread(target=self.executar_tarefa).start()

    def executar_tarefa(self):
        total, movidos, destino = separar_arquivos_em_pastas(self.selected_folder, self.keywords, self.progress.set)
        self.progress.set(0)

        if total == 0:
            messagebox.showinfo("Concluído", "Nenhum arquivo PDF encontrado.")
        else:
            restantes = total - movidos
            msg = f"{total} arquivos PDF encontrados.\n{movidos} movidos com sucesso."
            if restantes > 0:
                msg += f"\n{restantes} não foram classificados."
            msg += f"\n\nArquivos salvos em:\n{destino}"
            messagebox.showinfo("Resumo da Separação", msg)

    def abrir_pasta_destino(self):
        destino = get_output_directory()
        if os.path.exists(destino):
            os.startfile(destino)
        else:
            messagebox.showerror("Erro", "Pasta de destino não encontrada.")

    def atualizar_lista_keywords(self):
        self.kw_listbox.delete("0.0", "end")
        for k in self.keywords:
            self.kw_listbox.insert("end", k + "\n")

    def salvar_lista_keywords(self):
        texto = self.kw_listbox.get("0.0", "end").strip()
        nova_lista = [linha.strip() for linha in texto.splitlines() if linha.strip()]
        if nova_lista:
            self.keywords = nova_lista
            salvar_keywords(self.keywords)
            self.atualizar_lista_keywords()
            messagebox.showinfo("Salvo", "Lista de palavras-chave atualizada com sucesso!")
        else:
            messagebox.showwarning("Aviso", "A lista está vazia.")

    def remover_keyword(self):
        selecionada = self.kw_listbox.get("insert linestart", "insert lineend").strip()
        if selecionada in self.keywords:
            self.keywords.remove(selecionada)
            salvar_keywords(self.keywords)
            self.atualizar_lista_keywords()
