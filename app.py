from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
app = Flask(__name__)

app.secret_key = '1234'
BD = 'datos.db'

def crear_tabla():
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contenido(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT, 
                entrada TEXT,
                texto TEXT,
                urlimagen TEXT
                )
            """)
        conn.commit()
        
crear_tabla()

def obtener_nombres_campos(tabla):
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({tabla})")
        campos = [row[1] for row in cursor.fetchall()]
    return campos



@app.route('/')
def index():
    
    campos = obtener_nombres_campos('contenido')
    return render_template('index.html',campos=campos)


    
@app.route('/muestra/')
def muestra():
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM contenido
            """)
        datos=cursor.fetchall()
        return render_template('muestra.html',data=datos)


@app.route('/api')
def genJson():
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM contenido"
        cursor.execute(query)
        datos = cursor.fetchall()
        json = []
        for dato in datos:
            json.append({
                'titulo':dato[1],
                'entrada':dato[2],
                'urlimagen':dato[4]
                })
        return jsonify(json) 

@app.route('/insertar',methods=['POST'])
def insertar():
    if request.method=='POST':
        nombre=request.form['titulo']
        entrada=request.form['entrada']
        texto=request.form['texto']
        urlimagen=request.form['urlimagen']
        with sqlite3.connect(BD) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO contenido(titulo, entrada, texto, urlimagen) VALUES (?, ?, ?, ?)
            """, (nombre, entrada, texto, urlimagen))
            conn.commit()
            flash('Los datos se han insertado correctamente', 'success')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)