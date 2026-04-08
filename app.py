from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# 🔑 TU BASE DE DATOS (YA CONFIGURADA)
DATABASE_URL = "postgresql://personas_user:8wDXqXYNcMxMUc1XPYvvKpNDzvGvoeLs@dpg-d7bc4th4tr6s73ai5bo0-a.oregon-postgres.render.com/personas_db_g1rv"

def get_connection():
    return psycopg2.connect(DATABASE_URL)

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