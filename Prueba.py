# -*- coding: utf-8 -*-
# from flask import Flask, request, render_template
# Pagina = Flask(__name__)
#Dirección principal
# @Pagina.route('/')
# def index():
#     return render_template('Principal.html')

# #Dirección particular
# @Pagina.route('/Pagina', methods = ['GET', 'POST'])
# def Respuesta():
#     if request.method== 'POST':
#         Valores_pagina = request.form        
#         return render_template('Pagina.html',Var=Valores_pagina)

# if __name__ =='__main__':
#    Pagina.run(debug=True)

from flask import Flask, render_template, jsonify
import threading
import time

app = Flask(__name__)

# Variable global para almacenar el contador
contador = 0

def contar():
    global contador
    while True:
        time.sleep(1)  # Esperar 1 segundo
        contador += 1  # Incrementar el contador

# Crear un hilo para ejecutar la función contar en segundo plano
hilo_contador = threading.Thread(target=contar)
hilo_contador.daemon = True
hilo_contador.start()

@app.route('/')
def index():
    return render_template('contador.html')

@app.route('/get_contador')
def get_contador():
    return jsonify({'contador': contador})

if __name__ == '__main__':
    app.run(debug=True)



   
   