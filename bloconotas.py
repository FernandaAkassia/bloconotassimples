import tkinter as tk
from tkinter import Menu, filedialog, messagebox
import os
import sys

# Variável para armazenar o caminho do arquivo atualmente aberto
# Começa como None, indicando que é um arquivo "Novo"
arquivo_atual = None


#==========================================================
# LICENÇA MIT
#==========================================================
LICENCA_MIT = """
Licença MIT

Copyright (c) [2025] [Rafaela Gondim/Fernanda Akassia]

A permissão é concedida, gratuitamente, a qualquer pessoa que obtenha uma cópia
deste software e arquivos de documentação associados (o "Software"), para lidar
com o Software sem restrição, incluindo, sem limitação, os direitos
de usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender
cópias do Software, e para permitir que as pessoas a quem o Software é
fornecido o façam, sujeito às seguintes condições:

O aviso de copyright acima e este aviso de permissão devem ser incluídos em
todas as cópias ou partes substanciais do Software.

O SOFTWARE É FORNECIDO "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA
OU IMPLÍCITA, INCLUINDO, MAS NÃO SE LIMITANDO ÀS GARANTIAS DE COMERCIALIZAÇÃO,
ADEQUAÇÃO A UM FIM ESPECÍFICO E NÃO VIOLAÇÃO. EM NENHUM CASO OS
AUTORES OU DETENTORES DOS DIREITOS AUTORAIS SERÃO RESPONSÁVEIS POR QUALQUER
REIVINDICAÇÃO, DANOS OU OUTRAS RESPONSABILIDADES, SEJA EM UMA AÇÃO DE CONTRATO,
DELITO OU DE OUTRA FORMA, DECORRENTES DE, FORA DE OU EM CONEXÃO COM O
SOFTWARE OU O USO OU OUTRAS NEGOCIAÇÕES NO SOFTWARE.
"""

#Funções do Menu ARQUIVO

def novo_arquivo():
    """Limpa a área de texto e redefine o arquivo atual."""
    global arquivo_atual

    #Pergunta se o usuário deseja salvar antes de criar um novo
    if messagebox.askyesno("Novo Arquivo", "Deseja salvar as alterações?"):
        salvar_arquivo()

    #Tenta salvar

    janela.title("Bloco de Notas Simples")
    caixa_texto.delete("1.0", tk.END)
    arquivo_atual = None


def abrir_arquivo():
    """Abre uma caixa de diálogo para selecionar e carregar um arquivo de texto."""
    global arquivo_atual

    caminho_arquivo = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Arquivos de Texto", ".txt"), ("Todos os Arquivos", ".*")]
    )

    if caminho_arquivo:
        try:
            with open(caminho_arquivo, "r") as arquivo:
                conteudo = arquivo.read()

            caixa_texto.delete("1.0", tk.END)
            caixa_texto.insert("1.0", conteudo)

            arquivo_atual = caminho_arquivo
            # Atualiza o título da janela para mostrar o nome do arquivo
            janela.title(f"Bloco de Notas Simples - {os.path.basename(caminho_arquivo)}")

        except Exception as e:
            messagebox.showerror("Erro ao Abrir", f"Não foi possível abrir o arquivo: {e}")


def salvar_arquivo():
    """Salva o conteúdo do texto no arquivo atual. Se for um arquivo novo, chama salvar_como()."""
    global arquivo_atual

    if arquivo_atual:
        try:
            with open(arquivo_atual, "w") as arquivo:
                # Obtém o conteúdo de 1.0 (início) até o final (tk.END) menos o caractere de nova linha
                conteudo = caixa_texto.get("1.0", tk.END + "-1c")
                arquivo.write(conteudo)
                janela.title(f"Bloco de Notas Simples - {os.path.basename(arquivo_atual)}")
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar o arquivo: {e}")
    else:
        salvar_como()


def salvar_como():
    """Abre uma caixa de diálogo para salvar o conteúdo com um novo nome/caminho."""
    global arquivo_atual

    caminho_arquivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Arquivos de Texto", ".txt"), ("Todos os Arquivos", ".*")]
    )

    if caminho_arquivo:
        arquivo_atual = caminho_arquivo
        salvar_arquivo()  # Chama a função salvar_arquivo que agora usará o novo caminho

def sair_aplicacao():
    """Sai do aplicativo."""
    if messagebox.askyesno("Sair", "Tem certeza que deseja sair?"):
        janela.destroy()
        sys.exit()  # Boa prática para garantir que o processo Python seja encerrado


def listar_arquivos():
    """Permite ao usuário selecionar um diretório e exibe uma lista de arquivos nele."""
    diretorio = filedialog.askdirectory(title="Selecionar Diretório")

    if diretorio:
        try:
            # Lista os arquivos no diretório selecionado
            arquivos = os.listdir(diretorio)

            # Filtra apenas os arquivos (ignorando diretórios, se possível)
            lista_arquivos = [f for f in arquivos if os.path.isfile(os.path.join(diretorio, f))]

            if lista_arquivos:
                lista_formatada = "\n".join(lista_arquivos)
                messagebox.showinfo(f"Arquivos em {os.path.basename(diretorio)}", lista_formatada)
            else:
                messagebox.showinfo("Listar Arquivos", "Nenhum arquivo encontrado neste diretório.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível listar os arquivos do diretório: {e}")


#Funções do Menu EDITAR

def copiar_texto(event=None):
    """Copia o texto selecionado para a área de transferência."""
    try:
        janela.clipboard_clear()
        texto_selecionado = caixa_texto.get(tk.SEL_FIRST, tk.SEL_LAST)
        janela.clipboard_append(texto_selecionado)
    except tk.TclError:
        pass


def colar_texto(event=None):
    """Cola o texto da área de transferência na posição do cursor."""
    try:
        caixa_texto.insert('', janela.clipboard_get())
    except tk.TclError:
        pass


def recortar_texto(event=None):
    """Recorta o texto selecionado para a área de transferência."""
    try:
        copiar_texto()
        if caixa_texto.tag_ranges(tk.SEL):
            caixa_texto.delete(tk.SEL_FIRST, tk.SEL_LAST)
    except tk.TclError:
        pass


#Funções de Undo/Redo
# O widget tk.Text já suporta nativamente, basta chamar os métodos

def desfazer():
    """Desfaz a última ação."""
    try:
        caixa_texto.edit_undo()
    except tk.TclError:
        pass


def refazer():
    """Refaz a última ação desfeita."""
    try:
        caixa_texto.edit_redo()
    except tk.TclError:
        pass


#Função do Menu SOBRE
def mostrar_licenca():
    """Exibe o texto da Licença MIT em uma caixa de diálogo."""
    messagebox.showinfo("Licença MIT", LICENCA_MIT)  

def caminho_arquivo(nome_arquivo):
    if getattr(sys, 'frozen', False):
        pasta_base = sys._MEIPASS
    else:
        pasta_base = os.path.dirname(__file__)
    return os.path.join(pasta_base, nome_arquivo)

#Configuração da janela principal
janela = tk.Tk()
#janela.iconbitmap(caminho_arquivo("icone.ico"))
janela.title("Bloco de Notas Simples")
janela.geometry("600x460")

#caminho do ícone
caminho_icone = os.path.join(os.path.dirname(__file__), "icone.ico")

#ícone superior esquerdo da janela


#Define a função de saída ao fechar a janela
janela.protocol("WM_DELETE_WINDOW", sair_aplicacao)

#Criação do widget de texto
caixa_texto = tk.Text(janela, wrap=tk.WORD, undo=True)
caixa_texto.pack(expand=True, fill=tk.BOTH)

#Criação da barra de menu
barra_menu = Menu(janela)
janela.config(menu=barra_menu) 

#Criação da barra de rolagem
barra_rolagem = tk.Scrollbar(caixa_texto)
barra_rolagem.pack(side=tk.RIGHT, fill=tk.Y) 
barra_rolagem.config(command=caixa_texto.yview)
caixa_texto.config(yscrollcommand=barra_rolagem.set)

#MENU ARQUIVO

menu_arquivo = Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Arquivo", menu=menu_arquivo)

menu_arquivo.add_command(label="Novo", command=novo_arquivo, accelerator="Ctrl+N")
menu_arquivo.add_command(label="Abrir...", command=abrir_arquivo, accelerator="Ctrl+O")
menu_arquivo.add_command(label="Salvar", command=salvar_arquivo, accelerator="Ctrl+S")
menu_arquivo.add_command(label="Salvar Como...", command=salvar_como)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Listar Arquivos...", command=listar_arquivos)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=sair_aplicacao)

#MENU EDITAR

menu_editar = Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Editar", menu=menu_editar)

#MENU SOBRE

menu_sobre = Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Sobre", menu=menu_sobre)

# ADICIONANDO A OPÇÃO DA LICENÇA NO MENU SOBRE
menu_sobre.add_command(label="Licença MIT", command=mostrar_licenca)


#Adicionar Undo/Redo
menu_editar.add_command(label="Desfazer", command=desfazer, accelerator="Ctrl+Z")
menu_editar.add_command(label="Refazer", command=refazer, accelerator="Ctrl+Y")
menu_editar.add_separator()
#Adicionar Comandos Recortar/Copiar/Colar
menu_editar.add_command(label="Recortar", command=recortar_texto, accelerator="Ctrl+X")
menu_editar.add_command(label="Copiar", command=copiar_texto, accelerator="Ctrl+C")
menu_editar.add_command(label="Colar", command=colar_texto, accelerator="Ctrl+V")

#Vincular atalhos de teclado (Ctrl + N/O/S/Z/Y/X/C/V)
caixa_texto.bind("<Control-n>", lambda event: novo_arquivo())
caixa_texto.bind("<Control-o>", lambda event: abrir_arquivo())
caixa_texto.bind("<Control-s>", lambda event: salvar_arquivo())
caixa_texto.bind("<Control-z>", lambda event: desfazer())
caixa_texto.bind("<Control-y>", lambda event: refazer())
caixa_texto.bind("<Control-x>", recortar_texto)
caixa_texto.bind("<Control-c>", copiar_texto)
caixa_texto.bind("<Control-v>", colar_texto)

#Iniciar o loop principal da aplicação
janela.mainloop()