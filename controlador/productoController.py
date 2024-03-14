from app import app, productos, categorias
from flask import Flask, render_template, request, jsonify
import pymongo
import os
from bson.objectid import ObjectId
import base64
from PIL import Image
from io import BytesIO
from bson.json_util import dumps
