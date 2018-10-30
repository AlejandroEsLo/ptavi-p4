#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""

import socketserver
import sys
import time
import json


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""

    list_clients = {}

    def handle(self):
        """handle method of the server class."""
        self.json2registered()
        archivo = self.rfile.read()  # Leer lo que nos envia el cliente
        mensaje_cliente = archivo.decode("utf-8").split(" ")
        # print("El cliente nos manda ", ' '.join(mensaje_cliente))

        Ip = self.client_address[0]
        metodo = mensaje_cliente[0]
        direccion = mensaje_cliente[1]
        usuario = direccion.split(":")[1]
        expires = int(mensaje_cliente[3].split("\\")[0])
        # Cogemos localtime para que sea conformea nuestra hora local
        t_inicio = time.strftime("%Y-%m-%d %H:%M:%S",
                                 time.localtime(int(time.time())))
        t_expires = time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime(int(time.time() + expires)))

        if metodo == "REGISTER":
            self.list_serv = {}
            usuarios_expires = []
            self.list_serv["IP"] = Ip
            self.list_serv["EXPIRES"] = t_expires
            self.list_clients[direccion] = self.list_serv
            print(usuario, "REGISTRADO\n")
            # Eliminamos cliente si expires = 0
            # O si su tiempo es menor que la hora actual
            for clients in self.list_clients:
                inf = self.list_clients[clients]
                if inf["EXPIRES"] <= t_inicio:
                    usuarios_expires.append(clients)

            for usuario in usuarios_expires:
                print(usuario.split(":")[-1], "EXPIRADO\n")
                del self.list_clients[usuario]

        self.register2json()
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

        print("Lista clientes: {}".format(self.list_clients))
        print("Lista ELIMINADOS: {}\n".format(usuarios_expires))

    def register2json(self):
        """Guardar los clientes en un fichero registro Json."""
        json.dump(self.list_clients, open("registered.json", "w"))

    def json2registered(self):
        """Cargar fichero Json si existe para utilizarlo en el servidor."""
        try:
            registered_json = open("registered.json", "r")
            self.list_clients = json.load(registered_json)

        except FileNotFoundError:
            pass


if __name__ == "__main__":

    puerto_servidor = int(sys.argv[1])
    # Ponemos '' para que pueda cojer cualquier  direccion ip
    serv = socketserver.UDPServer(('', puerto_servidor), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
