from app import app, usuarios
from flask import render_template, request, redirect
import pymongo
import yagmail

@app.route('/')
def vistaIniciarSesion():  # Corrección del nombre de la función
    return render_template('frmIniciarSesion.html')

@app.route('/iniciarSesion', methods=['POST'])
def iniciarSesion():  # Corrección del nombre de la función
    mensaje = None
    estado = False
    try:
        usuario = request.form['txtUser']
        password = request.form['txtPassword']
        datosConsulta = {"usuario": usuario, "password": password}
        user = usuarios.find_one(datosConsulta)
        if user:
            email = yagmail.SMTP("msftsebasstian@gmail.com", open(".password").read(), encoding='UTF-8')
            asunto = 'Reporte de ingreso al sistema de usuario'
            mensaje = f"Se informa que el usuario <b>'{user["nombres"]} {user["apellidos"]}'</b> ha ingresado al sistema"  # Corrección en la interpolación de cadenas
            email.send(to=['msftsebasstian@gmail.com', user["correo"]], subject=asunto, contents=mensaje)
            return redirect("/listarProductos")  # Corrección en la redirección
        else:
            mensaje = 'Credenciales no válidas'
    except pymongo.errors.PyMongoError as error:  # Corrección en el manejo de excepciones
        mensaje = error
        
    return render_template('frmIniciarSesion.html', estado=estado, mensaje=mensaje)
