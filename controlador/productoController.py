# productoController.py

from flask import abort, session, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import pymongo
import os

from app import app, productos, categorias


@app.route('/listarProductos')
def inicio():
    if 'user' in session:
        try:
            listaProductos = productos.find()
            listaP = []
            for p in listaProductos:
                categoria = categorias.find_one({'_id': p['categoria']})
                p['nombreCategoria'] = categoria['nombre']
                listaP.append(p)

            return render_template('listarProductos.html', productos=listaP)
        except pymongo.errors.PyMongoError as error:
            mensaje = str(error)
            return mensaje
    else:
        mensaje = "Debe ingresar con sus credenciales"
        return render_template('frmIniciarSesion.html', mensaje=mensaje)


@app.route('/agregarProducto', methods=['POST'])
def agregarProducto():
    if 'user' in session:
        try:
            codigo = int(request.form['txtCodigo'])
            nombre = request.form['txtNombre']
            precio = int(request.form['txtPrecio'])
            idCategoria = ObjectId(request.form['cbCategoria'])
            foto = request.files['fileFoto']
            producto = {
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "categoria": idCategoria,
            }
            resultado = productos.insert_one(producto)
            if resultado.acknowledged:
                idProducto = resultado.inserted_id
                nombreFoto = f'{idProducto}.jpg'
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFoto))
                mensaje = 'Producto agregado correctamente'
                return redirect('/listarProductos')
            else:
                mensaje = 'No se pudo agregar el producto'
                return redirect('/vistaAgregarProducto')
        except pymongo.errors.PyMongoError as error:
            mensaje = str(error)
            return mensaje
    else:
        mensaje = "Debe primero iniciar sesión"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)
    
@app.route('/vistaAgregarProducto')
def vistaAgregarProducto():
    if 'user' in session:
        listaCategorias = categorias.find()
        return render_template('frmAgregarProducto.html', categorias=listaCategorias)
    else:
        mensaje = "Debe primero iniciar sesión"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)







@app.route('/editarProducto/<idProducto>', methods=['GET'])
def vistaEditarProducto(idProducto):
    if ("user" in session):
        try:
        
            producto = productos.find_one({"_id": ObjectId(idProducto)})
            if producto is None:
                abort(404)  
            listaCategorias = categorias.find()
            return render_template('frmEditarProducto.html', producto=producto, categorias=listaCategorias)
        except Exception as e:
            return f"Error: {e}"
    else:
        mensaje="Debe primero iniciar sesion"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)


@app.route('/editar', methods=['POST'])
def editar():
    if("user" in session):
        try:
            idProducto = request.form['idProducto']
            codigo = int(request.form['txtCodigo'])
            nombre = request.form['txtNombre']
            precio = int(request.form['txtPrecio'])
            idCategoria = ObjectId(request.form['cbCategoria'])
            foto = request.files['fileFoto'] if 'fileFoto' in request.files else None

           
            productos.update_one(
                {"_id": ObjectId(idProducto)},
                {"$set": {
                    "codigo": codigo,
                    "nombre": nombre,
                    "precio": precio,
                    "categoria": idCategoria
                }}
            )

            if foto:
                nombreFoto = f"{idProducto}.jpg"
                foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))

            return redirect(url_for("inicio"))
        
        except Exception as error:
            return f"Error al editar el producto: {error}"
    else:
        mensaje="Debe primero iniciar sesion"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)

@app.route("/eliminarProducto/<idProducto>", methods=["GET"])
def eliminar_producto(idProducto):
    if ("user" in session):
        try:
            resultado = productos.delete_one({"_id": ObjectId(idProducto)})
            if resultado.deleted_count == 1:
                print ('eliminar')
                return redirect(url_for("inicio"))  
            else:
                return "el producto no existe."
        except pymongo.errors.PyMongoError as error:
            return f"Error al eliminar el producto: {error}"
    else:
        mensaje="Debe primero iniciar sesion"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)


