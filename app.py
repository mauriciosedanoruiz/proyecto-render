from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# 🔑 DATABASE DESDE RENDER
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# 🗄️ CREAR TABLA AUTOMÁTICAMENTE
def crear_tabla():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personas (
        id SERIAL PRIMARY KEY,
        dni VARCHAR(20) NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        direccion TEXT,
        telefono VARCHAR(20)
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()

# Ejecutar al iniciar
crear_tabla()

# 🏠 FORMULARIO
@app.route('/')
def index():
    return render_template('index.html')

# ➕ GUARDAR
@app.route('/guardar', methods=['POST'])
def guardar():
    try:
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO personas (dni, nombre, apellido, direccion, telefono)
            VALUES (%s, %s, %s, %s, %s)
        """, (dni, nombre, apellido, direccion, telefono))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/')

    except Exception as e:
        return f"ERROR: {e}"

# 📋 LISTAR
@app.route('/administrar')
def administrar():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM personas")
    personas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('administrar.html', personas=personas)

# ❌ ELIMINAR
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM personas WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/administrar')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)