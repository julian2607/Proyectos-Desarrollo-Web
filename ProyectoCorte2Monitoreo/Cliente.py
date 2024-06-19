# -*- coding: utf-8 -*-
import socket
import psutil
import time
Nombre_Socket = socket.socket()
IP_Servidor='192.168.171.1'
Puerto=1234

# Indicar unidad a monitorear
disk_usage = psutil.disk_usage("C:\\")
def Convertir_Bytes_a_Gigas(bytes):      
    return bytes / 1024**3

try:
    Bandera=True
    Nombre_Socket.connect((IP_Servidor, Puerto))
    print("Conectado")
except ConnectionRefusedError:
    Bandera=False 
    print('Intente conectarse al servidor nuevamente')

while Bandera:
    # LEER PARAMEETROS DEL EQUIPO:
    battery_info = psutil.sensors_battery().percent
    Memoria_Total = psutil.virtual_memory().total
    Memoria_Disponible = psutil.virtual_memory().available
    Memoria_Porsentaje =psutil.virtual_memory().percent
    Usuario = psutil.users()[0].name
    Usuario_Inicio =psutil.users()[0].started
    Memoria_intercambio_Total=psutil.swap_memory().total
    Memoria_intercambio_usado =psutil.swap_memory().used
    Memoria_intercambio_porsentaje=psutil.swap_memory().percent

    Envio=[disk_usage.total,disk_usage.free,disk_usage.used,disk_usage.percent,
            battery_info,Memoria_Total,Memoria_Disponible,Memoria_Porsentaje,
            Usuario,Usuario_Inicio,Memoria_intercambio_Total,Memoria_intercambio_usado,
            Memoria_intercambio_porsentaje]
    texto = str(Envio)
    print(texto)    
    paquete = texto.encode()
    try:
       time.sleep(5)
       Nombre_Socket.send(paquete)
       if(texto=='cerrar'):
           break
    except ConnectionResetError:
        break

print('Termino la aplicación')
Nombre_Socket.close()



# monitoreo linux
# -*- coding: utf-8 -*-
# import socket
# import psutil
# import time
# Nombre_Socket = socket.socket()
# IP_Servidor='192.168.171.1'
# Puerto=1234

# # Indicar unidad a monitorear
# disk_usage = psutil.disk_usage("/")
# def Convertir_Bytes_a_Gigas(bytes):      
#     return bytes / 1024**3

# try:
#     Bandera=True
#     Nombre_Socket.connect((IP_Servidor, Puerto))
#     print("Conectado")
# except ConnectionRefusedError:
#     Bandera=False 
#     print('Intente conectarse al servidor nuevamente')

# while Bandera:
#     # LEER PARAMEETROS DEL EQUIPO:
#     Memoria_Total = psutil.virtual_memory().total
#     Memoria_Disponible = psutil.virtual_memory().available
#     Memoria_Porsentaje =psutil.virtual_memory().percent
#     Usuario = psutil.users()[0].name
#     Usuario_Inicio =psutil.users()[0].started
#     Memoria_intercambio_Total=psutil.swap_memory().total
#     Memoria_intercambio_usado =psutil.swap_memory().used
#     Memoria_intercambio_porsentaje=psutil.swap_memory().percent

#     Envio=[disk_usage.total,disk_usage.free,disk_usage.used,disk_usage.percent,
#             Memoria_Total,Memoria_Disponible,Memoria_Porsentaje,
#                     Usuario,Usuario_Inicio,Memoria_intercambio_Total,Memoria_intercambio_usado,
#             Memoria_intercambio_porsentaje]
#     texto = str(Envio)
#     print(texto)    
#     paquete = texto.encode()
#     try:
#        time.sleep(5)
#        Nombre_Socket.send(paquete)
#        if(texto=='cerrar'):
#            break
#     except ConnectionResetError:
#         break

# print('Termino la aplicación')
# Nombre_Socket.close()