import os
import shutil
import time
import sys
import re

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

KEYWORDS_FILE = resource_path('keywords.txt')

def carregar_keywords():
    if not os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, 'w'): pass
    with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
        return [linha.strip() for linha in f if linha.strip()]

def salvar_keywords(keywords):
    with open(KEYWORDS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(keywords))

def get_output_directory():
    try:
        user = os.getlogin()
        path = os.path.join("C:\\Users", user, "Downloads", "Splitfiles")
        os.makedirs(path, exist_ok=True)
        return path
    except Exception:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop", "Splitfiles")
        os.makedirs(desktop, exist_ok=True)
        return desktop

# ✅ Função melhorada para normalizar nomes com tolerância a hífen, ponto, underline e espaços
def normalizar_nome(nome):
    nome = nome.lower()
    nome = re.sub(r'[\-_\.]', ' ', nome)         # Substitui hífen, underline e ponto por espaço
    nome = re.sub(r'[^a-z0-9 ]', '', nome)       # Remove tudo que não for letra, número ou espaço
    nome = re.sub(r'\s+', ' ', nome).strip()     # Remove espaços duplicados
    return nome

def separar_arquivos_em_pastas(diretorio_origem, keywords, progress_callback=None):
    try:
        arquivos = [f for f in os.listdir(diretorio_origem) if f.lower().endswith('.pdf')]
        total = len(arquivos)
        destino_base = get_output_directory()
        movidos = 0

        # ✅ Prioriza palavras-chave mais específicas
        keywords = sorted(keywords, key=lambda x: len(x), reverse=True)

        for i, nome_arquivo in enumerate(arquivos):
            caminho = os.path.join(diretorio_origem, nome_arquivo)
            nome_base = os.path.splitext(nome_arquivo)[0]
            nome_normalizado = normalizar_nome(nome_base)
            encontrou = False

            for palavra in keywords:
                palavra_normalizada = normalizar_nome(palavra)
                if palavra_normalizada in nome_normalizado:
                    destino = os.path.join(destino_base, palavra)
                    os.makedirs(destino, exist_ok=True)
                    shutil.move(caminho, os.path.join(destino, nome_arquivo))
                    movidos += 1
                    encontrou = True
                    break

            if progress_callback:
                progress_callback((i + 1) / total)
            time.sleep(0.05)

        return total, movidos, destino_base

    except Exception as e:
        print(f"[ERRO] Falha ao separar arquivos: {e}")
        return 0, 0, ""


