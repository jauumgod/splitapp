import os
import shutil
import time

import sys
import os

def resource_path(relative_path):
    """Retorna o caminho absoluto do recurso, compatível com dev e executável"""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
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

def separar_arquivos_em_pastas(diretorio, keywords, progress_callback=None):
    arquivos = [f for f in os.listdir(diretorio) if f.lower().endswith('.pdf')]
    total = len(arquivos)

    for i, nome_arquivo in enumerate(arquivos):
        caminho = os.path.join(diretorio, nome_arquivo)
        for palavra in keywords:
            if palavra.lower() in nome_arquivo.lower():
                destino = os.path.join(diretorio, palavra)
                os.makedirs(destino, exist_ok=True)
                shutil.move(caminho, os.path.join(destino, nome_arquivo))
                break

        if progress_callback:
            progress_callback((i + 1) / total)
        time.sleep(0.05)
