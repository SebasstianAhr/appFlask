from app import app, categorias
from flask import Flask, render_template
import pymongo

@app.route('/obtenerCategorias')
def obtenerCategorias():
    listaCategorias = categorias.find()
    return render_template('listarProductos.html', categorias=listaCategorias)