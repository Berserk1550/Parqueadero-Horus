
from flask import Flask, redirect, render_template, request, send_from_directory, session, url_for
import hashlib
from datetime import datetime, timedelta
import re
import mysql.connector

# Nombre del programa
programa = Flask(__name__)

# Conexión directa a la base de datos 'horus'
mi_db = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    database="db_parqueo"
)

programa.secret_key = "super_segura"

# Cursor con resultados en formato diccionario
mi_cursor = mi_db.cursor(dictionary=True)
