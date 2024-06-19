# -*- coding: utf-8 -*-

import threading
import socket
import time
from tkinter import *
from tkinter import Tk
from tkinter import ttk
import mysql.connector as mysql

from flask import Flask, request, render_template,jsonify


"""Importar librería del conector de mysql"""
import mysql.connector as mysql
"""Importe la librería SMTP"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
"""Crear variables con los parámetros de acceso a la BD"""
ORIGEN="localhost"
USUARIO="root"
CONTRASENA="1234"
BASEDATOS="universidad"
# Flask
Pagina = Flask(__name__)
global turno
turno = "turno"

"""Funciones"""
def Cliente_1():
    global TextoGlobal1,ID_Socket_Cliente1,ID_Socket_Cliente2,mensaje_recibidol,mensaje_recibido2,Control1
    ID_Socket_Cliente1, direccion1 = Nombre_Socket.accept()
    while True:
        mensaje_recibidol = ID_Socket_Cliente1.recv(1024)
        texto = mensaje_recibidol.decode("utf-8")
        if texto == 'cerrar':    
            break
        else:  
            if Control1==True:          
                TextoGlobal1=texto
                salida = ValidarJuego(texto,1)
                print(salida)
                if salida=='PosicionG':
                    texto=salida
                    ID_Socket_Cliente1.sendall(texto.encode())
                    ID_Socket_Cliente1.sendall(mensaje_recibidol)    
                ID_Socket_Cliente2.sendall(texto.encode())
                ID_Socket_Cliente2.sendall(mensaje_recibidol)
            else:                
                text = "posicionX"
                print(text)
                ID_Socket_Cliente1.sendall(text.encode())
                ID_Socket_Cliente1.sendall(mensaje_recibidol)
          
    print ("Terminó la comunicación con el Cliente 1")
    ID_Socket_Cliente1.close()

def Cliente_2():
    global TextoGlobal2,ID_Socket_Cliente1,ID_Socket_Cliente2,mensaje_recibidol,mensaje_recibido2,Control2
    ID_Socket_Cliente2, direccion2 = Nombre_Socket.accept()
    while True:         
        mensaje_recibido2 = ID_Socket_Cliente2.recv(1024)
        texto = mensaje_recibido2.decode("utf-8")
        if texto == 'cerrar':
             break
        else:          
            if Control2==True:
                TextoGlobal2=texto
                salida = ValidarJuego(texto,2)
                print(salida)
                if salida=='PosicionG':
                    texto=salida
                    ID_Socket_Cliente2.sendall(texto.encode())
                    ID_Socket_Cliente2.sendall(mensaje_recibido2)                    
                ID_Socket_Cliente1.sendall(texto.encode())
                ID_Socket_Cliente1.sendall(mensaje_recibido2)            
            else:
                text = "posicionX"
                print(text)
                ID_Socket_Cliente2.sendall(text.encode())
                ID_Socket_Cliente2.sendall(mensaje_recibido2)  
                
                
    print ("Terminó la comunicación con el Cliente 2")
    ID_Socket_Cliente2.close()


@Pagina.route('/get_contador')
def Actualiza():
    global turno
    juegos=[0,0,"False",'']    
    BD = mysql.connect(host=ORIGEN, user=USUARIO, passwd=CONTRASENA, db=BASEDATOS)
    Cursor = BD.cursor()    
    Cursor.execute("SELECT * FROM GANADORTRICKI")
    MSG = MIMEMultipart()
    for row in Cursor:
        juegos[0]+=row[2]
        juegos[1]+=row[3]   

    if juegos[0]>juegos[1]:
        juegos[2]="True"        
    else:
        juegos[2]="False"
    juegos[3]=turno
    return jsonify({'contador': juegos})
    


def ValidarJuego(opcion,jugador):    
    global a,b,c,d,e,f,g,h,i,NumeroJuego
    global a2,b2,c2,d2,e2,f2,g2,h2,i2
    print(opcion)
    
    if "posicion1" in opcion:        
        if jugador == 1:
            a=1        
        else:
            a2=1
    if 'posicion2'in opcion:
        if jugador == 1:
            b=1        
        else:
            b2=1
    if 'posicion3'in opcion:
        if jugador == 1:
            c=1        
        else:
            c2=1
    if 'posicion4'in opcion:
        if jugador == 1:
            d=1        
        else:
            d2=1
    if 'posicion5'in opcion:
        if jugador == 1:
            e=1        
        else:
            e2=1
    if 'posicion6'in opcion:
        if jugador == 1:
            f=1        
        else:
            f2=1
    if 'posicion7'in opcion:
        if jugador == 1:
            g=1        
        else:
            g2=1
    if 'posicion8'in opcion:
        if jugador == 1:
            h=1        
        else:
            h2=1
    if 'posicion9'in opcion:
        if jugador == 1:
            i=1        
        else:
            i2=1
        
    if (a==1 and b==1 and c==1) or (a==1 and e==1 and i==1) or (a==1 and d==1 and g==1) or (d==1 and e==1 and f==1) or (g==1 and h==1 and i==1) or (b==1 and e==1 and h==1) or (c==1 and e==1 and g==1) or (c==1 and f==1 and i==1):
        print("GanadorJugador1")
        NumeroJuego+=1
        ConteoJuego = "# Partidas: " + str(NumeroJuego)   
        if paginaActiva==0:
            SalidaConteo.config(text=ConteoJuego) 
        a = b = c = d = e = f = g = h = i = 0
        a2 = b2 = c2 = d2 = e2 = f2 = g2 = h2 = i2 =0       
        # Comando guaradr ganador tabla
        BD = mysql.connect(host=ORIGEN, user=USUARIO, passwd=CONTRASENA, db=BASEDATOS)
        Cursor = BD.cursor()
        Comando="INSERT INTO  GanadorTricki(fecha,jugador1, jugador2) VALUES(now(),%s, %s);"
        Valores=(str(1),str(0))
        Cursor.execute(Comando,Valores)
        BD.commit()
        """Cerrar la BD"""
        BD.close()
        # MSG = MIMEMultipart()
        # Mensaje = "GANADOR JUGADOR1"""
        # Contrasena     = "bagi oxoj zdav lntm "
        # MSG['From']    = "felipecarrion2000@gmail.com"
        # MSG['To']      = "jfcarrionp@udistrital.edu.co"
        # MSG['Subject'] = "GANADORES JUEGO TRICKI"
        # MSG.attach(MIMEText (Mensaje, 'plain'))

        return "PosicionG"  
    else:
        if (a2==1 and b2==1 and c2==1) or (a2==1 and e2==1 and i2==1) or (a2==1 and d2==1 and g2==1) or (d2==1 and e2==1 and f2==1) or (g2==1 and h2==1 and i2==1) or (b2==1 and e2==1 and h2==1) or (c2==1 and e2==1 and g2==1) or (c2==1 and f2==1 and i2==1):
            print("Ganador Jugador 2")
            NumeroJuego+=1
            ConteoJuego = "# Partidas: " + str(NumeroJuego) 
            if paginaActiva==0:       
                SalidaConteo.config(text=ConteoJuego) 
            a = b = c = d = e = f = g = h = i = 0
            a2 = b2 = c2 = d2 = e2 = f2 = g2 = h2 = i2 =0       
            # Comando guaradr ganador tabla
            BD = mysql.connect(host=ORIGEN, user=USUARIO, passwd=CONTRASENA, db=BASEDATOS)
            Cursor = BD.cursor()
            Comando="INSERT INTO  GanadorTricki(fecha,jugador1, jugador2) VALUES(now(),%s, %s);"
            Valores=(str(0),str(1))
            Cursor.execute(Comando,Valores)
            BD.commit()
            """Cerrar la BD"""
            BD.close()            
            # MSG = MIMEMultipart()
            # Mensaje = "GANADOR JUGADOR2"""
            # Contrasena     = "bagi oxoj zdav lntm "
            # MSG['From']    = "felipecarrion2000@gmail.com"
            # MSG['To']      = "jfcarrionp@udistrital.edu.co"
            # MSG['Subject'] = "GANADORES JUEGO TRICKI"
            # MSG.attach(MIMEText (Mensaje, 'plain'))
            
            return "PosicionG"  
        else:
            return"PosicionR"     
            
def Controlador():
    global TiempoGlobal,TextoGlobal1,TextoGlobal2,Cont,Control1,Control2,turno   
    while True:        
        if Cont==0:
            turno='Turno 1'
            print("Turno 1")
            Control1 = True
            Control2 = False
        
        if Cont==TiempoGlobal:
            turno='Turno 2'
            print("Turno 2")
            Control1 = False
            Control2 = True
        
        if Cont==(TiempoGlobal*2):
            turno='Turno 1'
            print("Turno 1")
            Control1 = True
            Control2 = False
            Cont=0

        if Control1:                            
            if TextoGlobal1 !="":
                print("Jugador1: " + TextoGlobal1)                                               
                TextoGlobal1 =""
                Cont=TiempoGlobal-1

        if Control2:                        
            if TextoGlobal2 !="":
                print("Jugador2: " + TextoGlobal2)                
                TextoGlobal2 =""
                Cont=-1

        Cont+=1
        time.sleep(1)

#ACTIVAR JUEGO
def iniciar():   
    global TiempoGlobal,ID_Socket_Cliente1,ID_Socket_Cliente2,NumeroJuego,paginaActiva,Tpagina    
    if paginaActiva==0:
        TiempoGlobal=int(C_Entrada.get())    
    else:
        TiempoGlobal=int(Tpagina)
    print("Tiempo = "+str(TiempoGlobal) + " Segundos")    
    NumeroJuego=1 

    #Hilos Inicio
    Hilo_1=threading.Thread(target=Cliente_1)
    Hilo_1.start()
    Hilo_2=threading.Thread(target=Cliente_2)
    Hilo_2.start()
    Hilo_Control=threading.Thread(target=Controlador) 
    Hilo_Control.start()
    
def correo():
    BD = mysql.connect(host=ORIGEN, user=USUARIO, passwd=CONTRASENA, db=BASEDATOS)
    Cursor = BD.cursor()    
    Cursor.execute("SELECT * FROM CorreoEmpleados")
    MSG = MIMEMultipart()
    for row in Cursor:
        Mensaje = "Bienvenido al curso Automatica III"""
        Contrasena     = "bagi oxoj zdav lntm "
        MSG['From']    = "felipecarrion2000@gmail.com"
        MSG['To']      = str(row[3])
        MSG['Subject'] = "CorreoPruebaMysql"
        MSG.attach(MIMEText (Mensaje, 'plain'))
        print("Envio a correo:"+row[3])
        

#Dirección principal
@Pagina.route('/')
def index():
    return render_template('Principal.html')

#Dirección particular
@Pagina.route('/Pagina', methods = ['GET', 'POST'])
def Respuesta():
    global paginaActiva,Tpagina,Var1 
    if request.method== 'POST':
        Valores_pagina = request.form 
        Var1=Valores_pagina    
        juego=[0,0]   
        paginaActiva=1
        Tpagina=Valores_pagina['Tiempo']
        print("Tiempo paina:"+Tpagina)
        iniciar()
        return render_template('Pagina.html',Var=Valores_pagina,Variable=juego)
    

'''Función principal'''
if __name__ == "__main__":
    global Control1,Control2,TiempoGlobal,Cont,NumeroJuego
    global a,b,c,d,e,f,g,h,i
    global a2,b2,c2,d2,e2,f2,g2,h2,i2
    global paginaActiva
    """Socket"""
    Nombre_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP_Servidor = "192.168.50.17"
    Puerto = 1234
    Nombre_Socket.bind((IP_Servidor, Puerto))
    Clientes = 2
    Nombre_Socket.listen(Clientes)    
    Cont=0
    NumeroJuego=0
    TextoGlobal1=""
    TextoGlobal2=""
    paginaActiva=0
    a = b = c = d = e = f = g = h = i = 0
    a2 = b2 = c2 = d2 = e2 = f2 = g2 = h2 = i2 =0       
    
    
    #Aplicacion
    Aplicacion=Tk()
    Aplicacion.geometry("400x200")
    Aplicacion.title("Caracteristicas")
    TiempoGlobal=0

    ConteoJuego = "# Partidas: "+ str(NumeroJuego); 
    etiqueta=Label(Aplicacion,text="JUEGO 3 EN LINEA",width= 50,bg='Red', fg='White')
    SalidaConteo=Label(Aplicacion,text=ConteoJuego,width= 20,bg='Black', fg='White')
    boton=Button(Aplicacion,text="Iniciar", width=10, height=2, bg='Green',fg='White', anchor="center",command=iniciar)
    botonCorreo=Button(Aplicacion,text="EnviarCorreo", width=10, height=2, bg='Blue',fg='White', anchor="center",command=correo)
    C_Entrada=Entry(Aplicacion, textvariable="",width=25)

    etiqueta.pack(pady=10)
    C_Entrada.pack()
    SalidaConteo.pack(pady=20)
    boton.pack()
    botonCorreo.pack()
    
    #Front Antiguo
    """Bucle infinito"""
    Aplicacion.mainloop()

    # PaginaWEB
    Pagina.run()
