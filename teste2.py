import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Configurações
PASTA_IMAGENS = "imagens"
LARGURA_IMAGEM = 200
ALTURA_IMAGEM = 300 

# Base de dados
dados = {
    "Filmes": {
        "Ação": ["Vingadores", "John Wick", "Mad Max"],
        "Terror": ["O Exorcista", "Invocação do Mal", "IT: A Coisa"],
        "Comédia": ["Gente Grande", "As Branquelas", "Se Beber, Não Case"],
        "Ficção Científica": ["Interestelar", "Matrix", "Duna"],
    },
    "Séries": {
        "Ação": ["Demolidor", "Jack Ryan", "The Punisher"],
        "Terror": ["Stranger Things", "The Haunting of Hill House", "Marianne"],
        "Comédia": ["Brooklyn Nine-Nine", "Friends", "The Office"],
        "Ficção Científica": ["Dark", "Black Mirror", "Westworld"],
    },
}

# Variável global
tipo_escolhido = None

def carregar_imagem(nome):
    try:
        nome = nome.strip()
        caminho = os.path.commonprefix(['C:/Users/JUNIORDASILVAAMORIM/Desktop/teste/imagens/'f"{nome}.jpg"])
        print(f"Tentando carregar: {caminho}") # Debug 
        
        imagem = Image.open(caminho)
        img = imagem.resize((LARGURA_IMAGEM, ALTURA_IMAGEM), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Erro ao carregar {nome}.jpg: {e}")
        return None

def mostrar_detalhes(titulo, imagem):
    if not imagem:
        messagebox.showerror("Erro", "Imagem não encontrada!")
        return

    janela_detalhes = tk.Toplevel()
    janela_detalhes.title(titulo)
    label_imagem = tk.Label(janela_detalhes, image=imagem)
    label_imagem.image = imagem
    label_imagem.pack(pady=10)
    tk.Button(janela_detalhes, text="Fechar", command=janela_detalhes.destroy).pack(pady=5)

def escolher_genero(tipo):
    global tipo_escolhido
    tipo_escolhido = tipo
    genero_label.config(text="Escolha um gênero:")
    for widget in frame_genero.winfo_children():
        widget.destroy()
    for genero in dados[tipo]:
        tk.Button(
            frame_genero, 
            text=genero, 
            font=("Arial", 12),
            command=lambda g=genero: mostrar_recomendacoes(g)
        ).pack(pady=5)

def mostrar_recomendacoes(genero):
    global tipo_escolhido
    if not tipo_escolhido:
        messagebox.showerror("Erro", "Selecione um tipo primeiro!")
        return

    janela_rec = tk.Toplevel()
    janela_rec.title(f"Recomendações de {genero}")
    frame_principal = tk.Frame(janela_rec)
    frame_principal.pack(pady=10)

    for titulo in dados[tipo_escolhido][genero]:
        frame = tk.Frame(frame_principal)
        frame.pack(side=tk.LEFT, padx=10)

        img_tk = carregar_imagem(titulo)
        if img_tk:
            tk.Button(
                frame, 
                image=img_tk, 
                text=titulo, 
                compound=tk.TOP,
                command=lambda t=titulo, i=img_tk: mostrar_detalhes(t, i)
            ).pack()
        else:
            tk.Label(frame, text=titulo).pack()

# Interface principal
janela = tk.Tk()
janela.title("Recomendador de Filmes e Séries")
janela.geometry("500x400")
janela.configure(bg="#f0f0f0")

# Widgets
tk.Label(janela, text="Bem-vindo ao Recomendador!", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)
tk.Label(janela, text="Você quer recomendações de Filmes ou Séries?", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)

frame_escolha = tk.Frame(janela, bg="#f0f0f0")
frame_escolha.pack(pady=10)
tk.Button(frame_escolha, text="Filmes", font=("Arial", 12), bg="#4a90e2", fg="white", width=15,
          command=lambda: escolher_genero("Filmes")).pack(side=tk.LEFT, padx=10)
tk.Button(frame_escolha, text="Séries", font=("Arial", 12), bg="#50b83c", fg="white", width=15,
          command=lambda: escolher_genero("Séries")).pack(side=tk.RIGHT, padx=10)

genero_label = tk.Label(janela, text="", font=("Arial", 12), bg="#f0f0f0")
genero_label.pack(pady=10)

frame_genero = tk.Frame(janela, bg="#f0f0f0")
frame_genero.pack()

janela.mainloop()
