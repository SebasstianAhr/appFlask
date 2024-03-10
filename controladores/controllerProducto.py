from app import app,productos
from flask import Flask,request,render_template,redirect
import pymongo 
from werkzeug.utils import secure_filename
import os   
from bson.objectid import ObjectId

