from app import app, productos, categorias  # Si productos y categorias son módulos, entonces esta línea debería ser correcta
from flask import Flask, render_template, request, jsonify, redirect
import pymongo
import os
from bson.objectid import ObjectId
import base64
from PIL import Image
from io import BytesIO
from bson.json_util import dumps

@app.route('/listarProductos')
def inicio():
    listaProductos = productos.find()
    listaP = []
    for p in listaProductos:
        categoria = categorias.find_one({'_id': p['categoria']})
        p['nombreCategoria'] = categoria['nombre']
        listaP.append(p)
    
    return render_template('listarProductos.html', productos=listaP)

@app.route('/agregarProducto', methods=['POST'])  # Corregido: Agregar '/' antes de 'agregarProducto'
def agregarProducto():
    mensaje = None
    estado = False
    try:
        codigo = int(request.form['txtCodigo'])
        nombre = request.form['txtNombre']
        precio = int(request.form['txtPrecio'])
        idCategoria = ObjectId(request.form['cbCategoria'])
        foto = request.files['fileFoto']  # Corregido: Usar 'request.files' para obtener la foto
        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "categoria": idCategoria,
        }
        resultado = productos.insert_one(producto)
        if (resultado.acknowledged):
            idProducto = resultado.inserted_id  # Corrección: 'insert_id' a 'inserted_id'
            nombreFoto = f'{idProducto}.jpg'
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFoto))
            mensaje = 'Producto agregado correctamente'
            estado = True
            return redirect('/listarProductos')
        else:
            mensaje = 'No se pudo agregar el producto'
            return redirect('/vistaAgregarProducto')
        
    
    except pymongo.errors as error:  # Corrección: 'pymongo.errors' en lugar de 'pymongo.errors as error'
        mensaje = error
        return error

def consultarProductoPorCodigo(codigo):
    try:
        consulta = {"codigo":codigo}
        producto = productos.find_one(consulta)
        if(producto is not None):
            return True
        else:
            return False
    except pymongo.errors as error:  # Corrección: 'pymongo.errors' en lugar de 'pymongo.errors as error'
        print(error)
        return False
    
@app.route('/vistaAgregarProducto')
def vistaAgregarProducto():
    listaCategorias = categorias.find()
    return render_template('frmAgregarProducto.html', categorias=listaCategorias)

