from app import app, usuarios
from flask import render_template

@app.route('/')
def vistaIniciarSesion():  # Corrección del nombre de la función
    return render_template('frmIniciarSesion.html')
