# -*- coding: utf-8 -*-
import threading
import socket
import time
from tkinter import *
from tkinter import Tk
from tkinter import ttk

from flask import Flask, request, render_template,jsonify

"""Importar librería del conector de mysql"""
import mysql.connector as mysql
"""Importe la librería SMTP"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# PDF
import pandas as pd
from fpdf import FPDF

# Flask
Pagina = Flask(__name__)

# Cliente Funciones
def Cliente_1():        
    ID_Socket_Cliente1, direccion1 = Nombre_Socket.accept()
    x=0
    while True:
        mensaje_recibidol = ID_Socket_Cliente1.recv(1024)
        texto = mensaje_recibidol.decode("utf-8")
        if texto == 'cerrar':    
            break
        else:  
            Enviado=str(texto)                           
            if Enviado=='':
                if x==0:
                    print("Desconectado")                
                    x=1
            else:                
                print("Mensaje " + str(texto))
                Arreglo = texto.split(",")
                EspacioTotal=format (Convertir_Bytes_a_Gigas(int(Arreglo[0].replace("[",""))))
                EspacioDisponible=format (Convertir_Bytes_a_Gigas(int(Arreglo[1])))
                EspacioUsado=format (Convertir_Bytes_a_Gigas(int(Arreglo[2])))            
                                        
                # Comando guaradr ganador tabla
                BD = mysql.connect(host=ORIGEN, user=USUARIO, passwd=CONTRASENA, db=BASEDATOS)
                Cursor = BD.cursor()
                Comando="insert into monitoreo(Sensor1,Sensor2,Sensor3,Sensor4,Sensor5,Sensor6,Sensor7,Sensor8,Sensor9,Sensor10) values(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s);"        
                Valores=(str(EspacioTotal),str(EspacioDisponible),str(EspacioUsado),str(Arreglo[5]),str(Arreglo[6]),str(Arreglo[7]),str(Arreglo[8]),str(Arreglo[9]),str(Arreglo[10]),str(Arreglo[11]))
                Cursor.execute(Comando,Valores)            
                BD.commit()
                """Cerrar la BD"""
                BD.close()
        
    print ("Terminó la comunicación con el Cliente 1")
    ID_Socket_Cliente1.close()

@Pagina.route('/get_Informacion')
def Actualiza():        
    BD = mysql.connect(host=ORIGEN, user=USUARIO, passwd=CONTRASENA, db=BASEDATOS)
    Cursor = BD.cursor()    
    Cursor.execute("SELECT * FROM MONITOREO")
    MSG = MIMEMultipart()
    html_table=""

    for row in Cursor:
        html_table += "<tr>"
        for value in row:
            html_table += "<td>{}</td>".format(value)
        html_table += "</tr>"
    
    return jsonify({'contador': html_table})
    
# CONVERTIR UNICADES
def Convertir_Bytes_a_Gigas(bytes):      
    return bytes / 1024**3

#ACTIVAR MEDICION
def iniciar():       
    #Hilos Inicio
    Hilo_1=threading.Thread(target=Cliente_1)
    Hilo_1.start()

#Dirección principal
@Pagina.route('/')
def index():
    return render_template('PaginaMonitoreo.html')

@Pagina.route('/PaginaIniciar')
def Respuesta():    
        iniciar()
        return render_template('PaginaMonitoreo.html')
    
@Pagina.route('/PDF')
def PDF():      
    print("Armando PDF")   
    BD = mysql.connect(host=ORIGEN, user=USUARIO, passwd=CONTRASENA, db=BASEDATOS)
    Cursor = BD.cursor()    
    Cursor.execute("SELECT * FROM MONITOREO")
    results=Cursor.fetchall()
    df = pd.DataFrame(results, columns=Cursor.column_names)
    BD.commit()
    """Cerrar la BD"""
    BD.close()    
    
    print(df)
    pdf = FPDF()            
    pdf.add_page(orientation='L')   
    pdf.set_font('Times', '', 12)        
    # Títulos de las columnas
    for col in df.columns:
        pdf.cell(23, 10, col, border=1)
    pdf.ln()

# Datos de la tabla
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):                                      
            pdf.cell(23, 15, str(df.iloc[i, j]) [0:9], border=1)
        pdf.ln()

    #Guardar pdf
    pdf.output('ProyectoCorte2Monitoreo/data.pdf', 'F')     
    return render_template('PaginaMonitoreo.html')


@Pagina.route('/EXCEL')
def EXCEL():    
    print("Armando EXCEL")   
    BD = mysql.connect(host=ORIGEN, user=USUARIO, passwd=CONTRASENA, db=BASEDATOS)
    Cursor = BD.cursor()    
    Cursor.execute("SELECT * FROM MONITOREO")
    results=Cursor.fetchall()
    df = pd.DataFrame(results, columns=Cursor.column_names)
    BD.commit()
    """Cerrar la BD"""
    BD.close()  
    # Guardamos el DataFrame en formato XLS
    df.to_excel('ProyectoCorte2Monitoreo/Excel.xlsx', index=False)
    return render_template('PaginaMonitoreo.html')


'''Función principal'''
if __name__ == "__main__":    
    # Socket
    Nombre_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP_Servidor = "192.168.132.17"
    Puerto = 1234
    Nombre_Socket.bind((IP_Servidor, Puerto))
    Clientes = 1
    Nombre_Socket.listen(Clientes)    

    #CONCEXION BASE DE DATOS 
    """Crear variables con los parámetros de acceso a la BD"""
    ORIGEN="localhost"
    USUARIO="root"
    CONTRASENA="1234"
    BASEDATOS="universidad"
    
    # PaginaWEB
    Pagina.run()

    
