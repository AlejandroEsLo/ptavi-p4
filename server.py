#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import time

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        """
        handle method of the server class
        """
        archivo = self.rfile.read()# Leer lo que nos envia el cliente
        mensaje_cliente = archivo.decode("utf-8").split(" ")
         
        Ip = self.client_address[0]
        puerto = self.client_address[1]
        metodo = mensaje_cliente[0]
        direccion = mensaje_cliente[1]
        usuario = direccion.split(":")[1]
        expires = int(mensaje_cliente[3].split("\\")[0])
        
        t_inicio = time.strftime("%Y-%m-%d %H:%M:%S", 
                                 time.gmtime(int(time.time())))
        t_expires = time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.gmtime(int(time.time() + expires)))

#        print("El cliente nos manda ", ' '.join(mensaje_cliente))
        #Imprimimos Ip y Puerto del cliente
#        print ("IP: {}".format(Ip) + "  Puerto: {}".format(puerto)+ \
#                    " Metodo: {}".format(metodo) +" Direccion: {}".format(direccion))
        
        if metodo == "REGISTER":
            self.list_serv = {}
            usuarios_expires =[]
            self.list_serv["IP"] = Ip
            self.list_serv["DIRECCION"] = usuario
            self.list_serv["EXPIRES"] = t_expires            
            list_clients[direccion] = self.list_serv
            
            # Eliminamos cliente si expires = 0 
            # O si su tiempo es menor que la hora actual
            for clients in list_clients:
                inf = list_clients[clients]
                if inf["EXPIRES"] <= t_inicio:
                     usuarios_expires.append(clients)
                            
            for usuario in usuarios_expires:
                print(usuario , "EXPIRADO\n")
                del list_clients[usuario]

        self.wfile.write(b"SIP/2.0 200 OK\\r\\n\\r\\n")
            
        print ("Lista clientes: {}".format(list_clients))
        print ("Lista ELIMINADOS: {}\n".format(usuarios_expires))

if __name__ == "__main__":
    
    list_clients ={}
    puerto_servidor = int(sys.argv[1])   
    serv = socketserver.UDPServer(('', puerto_servidor), SIPRegisterHandler) 
    print("Lanzando servidor UDP de eco...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
