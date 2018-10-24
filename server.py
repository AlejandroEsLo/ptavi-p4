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
        archivo = self.rfile.read()
        mensaje_cliente = archivo.decode("utf-8").split(" ")
         
        Ip = self.client_address[0]
        Puerto = self.client_address[1]
        Metodo = mensaje_cliente[0]
        Direccion = mensaje_cliente[1].split(":")
        
        self.wfile.write(b"Hemos recibido tu peticion")
        #for line in self.rfile:
        print("El cliente nos manda ", ' '.join(mensaje_cliente))
        #Imprimimos Ip y Puerto del cliente
        print ("IP: {}".format(Ip) + "  Puerto: {}".format(Puerto)+ \
                    " Metodo: {}".format(Metodo) +" Direccion: {}".format(Direccion))
      

if __name__ == "__main__":
    
    List_Clients ={}
    Puerto_Servidor = int(sys.argv[1])   
    serv = socketserver.UDPServer(('', Puerto_Servidor), SIPRegisterHandler) 
    print("Lanzando servidor UDP de eco...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
