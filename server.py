#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

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
        direccion = mensaje_cliente[1].split(":")
        usuario = direccion[1]
        
        self.wfile.write(b"SIP/2.0 200 OK\\r\\n\\r\\n")
        
#        print("El cliente nos manda ", ' '.join(mensaje_cliente))
        #Imprimimos Ip y Puerto del cliente
#        print ("IP: {}".format(Ip) + "  Puerto: {}".format(puerto)+ \
#                    " Metodo: {}".format(metodo) +" Direccion: {}".format(direccion))

        if metodo == "REGISTER":
            self.list_serv = {}
            self.list_serv["IP"] = Ip
            self.list_serv["DIRECCION"] = usuario
            list_clients[usuario] = self.list_serv
      
        print ("Lista clientes: {}".format(list_clients))
        
if __name__ == "__main__":
    
    list_clients ={}
    puerto_servidor = int(sys.argv[1])   
    serv = socketserver.UDPServer(('', puerto_servidor), SIPRegisterHandler) 
    print("Lanzando servidor UDP de eco...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
