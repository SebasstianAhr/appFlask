from flask import Flask, render_template, request, redirect
import pymongo
from werkzeug.utils import secure_filename
import os
from bson import ObjectId  # Importar ObjectId desde bson

# Se crea el objeto flask
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './static/images'

# Se crea la conexión a mongo
miConexion = pymongo.MongoClient('mongodb://localhost:27017')

# Acceder a la base de datos
baseDatos = miConexion['GESTIONARPRODUCTOS']
productos = baseDatos['PRODUCTOS']
from controladores.controllerProducto import *

if __name__ == '__main__':
    app.run(port=3000, debug=True)


@app.route('/')
def inicio():
    # Obtener la lista de los productos de la colección productos
    listaProductos = productos.find()
    return render_template('listarProductos.html', listaProductos=listaProductos)

@app.route("/agregarProducto", methods=['POST'])
def agregarProducto():
    mensaje = ''
    try:
        # Escribir los valores de la vista en variables locales
        codigo = int(request.form['txtCodigo'])
        nombre = request.form['txtNombre']
        precio = int(request.form['txtPrecio'])  # Corregido el nombre de la clave
        categoria = request.form['cbCategoria']

        # Datos de la imagen
        archivo = request.files['fileFoto']
        nombreArchivo = secure_filename(archivo.filename)
        listaNombreArchivo = nombreArchivo.rsplit('.', 1)
        extension = listaNombreArchivo[1].lower()

        # Crear el objeto de el producto tipo diccionario
        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "categoria": categoria
        }

        # Se valida si existe el producto con codigo
        existe = consultarProductoPorCodigo(codigo)
        if existe:
            mensaje = 'Ya existe un producto con este codigo'
            return render_template('frmAgregarProducto.html', producto=producto, mensaje=mensaje)
        else:
            # Ejecutar consulta de inserción de datos
            resultado = productos.insert_one(producto)
            if resultado.acknowledged:
                mensaje = 'Producto agregado exitosamente'
                # Obtener el id de el producto que se acaba de insertar
                idProducto = resultado.inserted_id
                nuevoNombre = str(idProducto) + '.' + str(extension)
                archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nuevoNombre))
                return redirect('/')
    except pymongo.errors.PyMongoError as error:
        mensaje = str(error)
        return render_template('frmAgregarProducto.html', producto=producto, mensaje=mensaje)


def consultarProductoPorCodigo(codigo):
    try:
        consulta = {'codigo': codigo}
        producto = productos.find_one(consulta)
        if producto is not None:
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as error:
        print(error)
        return False
    

@app.route('/consultar/<string:idProducto>', methods=['GET'])
def consultarPorId(idProducto):  # Corregido el nombre del parámetro
    try:
        idProducto = ObjectId(idProducto)
        consulta = {'_id': idProducto}
        producto = productos.find_one(consulta)
        return render_template('frmEditarProducto.html', producto=producto)
    except pymongo.errors.PyMongoError as error:
        mensaje = str(error)
        listaProductos = productos.find()
        return render_template('listaProductos.html', mensaje=mensaje, listaProductos=listaProductos)

@app.route('/actualizar', methods=['POST'])
def actualizarProducto():
    try:
        # Recibir los valores de la vista en los variables locales
        codigo = int(request.form['txtCodigo'])
        nombre = request.form['txtNombre']
        precio = int(request.form['txtPrecio'])
        categoria = request.form['cbCategoria']
        idProducto = ObjectId(request.form['idProducto'])
        criterio = {'_id': idProducto}
        datosActualizar = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "categoria": categoria
        }

        consulta = {'$set': datosActualizar}
        resultado = productos.update_one(criterio, consulta)
        if resultado.acknowledged:
            mensaje = 'Producto actualizado'
            # Verificar si viene foto para actualizarla
            archivo = request.files['fileFoto']
            if archivo.filename != '':
                nombreArchivo = secure_filename(archivo.filename)
                listaNombreArchivo = nombreArchivo.rsplit('.', 1)
                extension = listaNombreArchivo[1].lower()
                nombreArchivoActualizar = str(idProducto) + '.' + str(extension)
                archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreArchivoActualizar))
    except pymongo.errors.PyMongoError as error:
        mensaje = str(error)
    listaProductos = productos.find()
    return render_template('listaProductos.html', mensaje=mensaje, listaProductos=listaProductos)

@app.route('/eliminar/<string:idProducto>', methods=['GET'])
def eliminarProducto(idProducto):
    try:
        idProducto = ObjectId(idProducto)
        consulta = {'_id': idProducto}
        resultado = productos.delete_one(consulta)
        if resultado.acknowledged:
            mensaje = 'Producto eliminado'
        else:
            mensaje = 'Problemas al eliminar'
    except pymongo.errors.PyMongoError as error:
        mensaje = str(error)
    listaProductos = productos.find()
    return render_template('listaProductos.html', mensaje=mensaje, listaProductos=listaProductos)
