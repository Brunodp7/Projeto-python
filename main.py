import sqlite3
from tkinter import *

# Criando a janela principal
root = Tk()
root.title('Cadastro de Usuários')

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('usuarios.db')
c = conn.cursor()

# Criando a tabela se não existir
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    idade INTEGER
)''')

# Função para adicionar um novo usuário ao banco de dados
def adicionar_usuario():
    nome = entry_nome.get()
    idade = entry_idade.get()

    c.execute("INSERT INTO usuarios (nome, idade) VALUES (?, ?)", (nome, idade))
    conn.commit()
    entry_nome.delete(0, END)
    entry_idade.delete(0, END)
    ler_usuarios()

# Função para ler e exibir os usuários cadastrados
def ler_usuarios():
    c.execute("SELECT * FROM usuarios")
    registros = c.fetchall()

    # Limpa a exibição anterior
    for widget in frame_registros.winfo_children():
        widget.destroy()

    for registro in registros:
        label = Label(frame_registros, text=f"ID: {registro[0]} | Nome: {registro[1]} | Idade: {registro[2]}")
        label.pack()

def selecionar_usuario():
    usuario_id = entry_id.get()
    c.execute("SELECT * FROM usuarios WHERE id=?", (usuario_id))

    registro = c.fetchone()

    if registro:
        entry_nome.delete(0,END)
        entry_idade.delete(0,END)
        entry_nome.insert(0, registro[1])
        entry_idade.insert(0, registro[2])

def atualizar_usuario():
    usuario_id = entry_id.get()
    novo_nome = entry_nome.get()
    nova_idade = entry_idade.get()
    c.execute("UPDATE usuarios SET nome  = ?, idade = ? WHERE id = ?", (novo_nome, nova_idade, usuario_id))
    conn.commit()
    entry_nome.delete(0, END)
    entry_idade.delete(0, END)
    ler_usuarios()

def deletar_usuario():
     usuario_id = entry_id.get()
     c.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id))
     conn.commit()
     entry_nome.delete(0, END)
     entry_idade.delete(0, END)
     ler_usuarios()
     
# Campos de entrada
Label(root, text="id").pack(pady=5)
entry_id = Entry(root)
entry_id.pack(pady=5)

Label(root, text="Nome").pack(pady=5)
entry_nome = Entry(root)
entry_nome.pack(pady=5)

Label(root, text="Idade").pack(pady=5)
entry_idade = Entry(root)
entry_idade.pack(pady=5)

# Botão para adicionar usuário
btn_add = Button(root, text="Adicionar Usuário", command=adicionar_usuario)
btn_add.pack(pady=10)

btn_selection = Button(root, text="selecionar Usuário", command=selecionar_usuario)
btn_selection.pack(pady=10)

btn_update = Button(root, text="atualizar Usuário", command=atualizar_usuario)
btn_update.pack(pady=10)

btn_delete = Button(root, text="deletar Usuário", command=deletar_usuario)
btn_delete.pack(pady=10)



# Frame para exibir os usuários cadastrados
frame_registros = Frame(root)
frame_registros.pack(pady=20)

# Exibir os usuários ao iniciar
ler_usuarios()

# Executando a janela
root.mainloop()

# Fechando a conexão com o banco de dados ao fechar a aplicação
conn.close()