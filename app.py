from flask import Flask, render_template, request
import pymongo
import os
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/imagenes'

miConexion = pymongo.MongoClient('mongodb://localhost:27017/')
baseDatos = miConexion['GESTIONARPRODUCTOS']
productos = baseDatos['PRODUCTOS']
categorias = baseDatos['CATEGORIAS']

@app.route('/')
def inicio():
    listaProductos = productos.find()
    listaP = []
    for p in listaProductos:
        categoria = categorias.find_one({'_id': p['categoria']})  # Cambiado 'categorias' a 'categoria'
        p['nombreCategoria'] = categoria['nombre'] if categoria else "Sin categoría"  # Corrección para manejar el caso en que no haya una categoría
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
            'codigo': codigo,
            'nombre': nombre,
            'precio': precio,
            'categoria': idCategoria,
        }
        resultado = productos.insert_one(producto)
        if (resultado.acknowledged):
            idProducto = resultado.inserted_id  # Corrección: 'insert_id' a 'inserted_id'
            nombreFoto = f'{idProducto}.jpg'
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFoto))
            mensaje = 'Producto agregado correctamente'
            estado = True
        else:
            mensaje = 'No se pudo agregar el producto'
    
    except pymongo.errors.PyMongoError as error:  # Corrección: 'pymongo.errors' en lugar de 'pymongo.errors as error'
        mensaje = str(error)

    return render_template('resultado.html', mensaje=mensaje, estado=estado)  # Agregado: Renderizar un template para mostrar el resultado

@app.route('/vistaAgregarProducto')
def vistaAgregarProducto():
    listaCategorias = categorias.find()
    return render_template('frmAgregarProducto.html', categorias=listaCategorias)

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
