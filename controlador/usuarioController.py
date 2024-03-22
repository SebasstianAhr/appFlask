from app import app, usuarios, session
from flask import render_template, request, redirect
import pymongo
import yagmail
import threading

@app.route('/')
def vistaIniciarSesion(): 
    return render_template('frmIniciarSesion.html')

@app.route('/iniciarSesion', methods=['POST'])
def iniciarSesion():
    mensaje = None
    estado = False
    try:
        usuario = request.form['txtUser']
        password = request.form['txtPassword']
        datosConsulta = {"usuario": usuario, "password": password}
        print(datosConsulta)
        user = usuarios.find_one(datosConsulta)
        if user:
            session['user']= usuario
            email = yagmail.SMTP("msftsebasstian@gmail.com", open(".password").read(), encoding='UTF-8')
            asunto = 'Reporte de ingreso al sistema de usuario'
            mensaje = f"Se informa que el usuario <b>'{user["nombres"]} {user["apellidos"]}'</b> ha ingresado al sistema" 
            
            thread = threading.Thread(target=enviarCorreo, args=(email, ["msftsebasstian@gmail.com" , user [ 'correo' ]], asunto, mensaje ))
            thread. start()
            estado = True

            return redirect("/listarProductos") 
        else:
            mensaje = 'Credenciales no válidas'
            
            
    except pymongo.errors.PyMongoError as error:
        mensaje = error
        
    return render_template('frmIniciarSesion.html', estado=estado, mensaje=mensaje)

def enviarCorreo(email=None, destinatario=None, asunto=None, mensaje=None):
    email. send (to=destinatario, subject=asunto, contents=mensaje)

@app.route('/salir')
def salir():
    session.clear()
    mensaje= "Ha cerrado la sesion"
    return render_template('frmIniciarSesion.html', mensaje=mensaje)

