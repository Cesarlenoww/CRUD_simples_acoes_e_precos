from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('stocks.db')
    conn.row_factory = sqlite3.Row
    return conn

# Função para inicializar o banco de dados com a tabela de ações
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )''')
    conn.commit()
    conn.close()

init_db()

# Rota principal - Exibe a lista de ações
@app.route('/')
def index():
    conn = get_db_connection()
    stocks = conn.execute('SELECT * FROM stocks').fetchall()
    conn.close()
    return render_template('index.html', stocks=stocks)

# Rota para criar um novo registro de ação
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']

        if not name or not price:
            flash('Nome da ação e preço são obrigatórios!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO stocks (name, price) VALUES (?, ?)', (name, float(price)))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

# Rota para editar uma ação existente
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    stock = conn.execute('SELECT * FROM stocks WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']

        if not name or not price:
            flash('Nome da ação e preço são obrigatórios!')
        else:
            conn.execute('UPDATE stocks SET name = ?, price = ? WHERE id = ?', (name, float(price), id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', stock=stock)

# Rota para deletar uma ação
@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM stocks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
