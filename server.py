import socket
import threading
import datetime
import os

USUARIOS = {
    "FAMB": "1234",
    "admin": "adminpass"
}

def manejar_cliente(conn, addr):
    print(f"Conectado con {addr}")
    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            print(f"[{addr}] Mensaje recibido: {data}")

            if data == "GET TIME":
                respuesta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            elif data.startswith("ECO "):
                respuesta = data[4:]

            elif "+" in data:
                try:
                    respuesta = str(eval(data))
                except:
                    respuesta = "Operación inválida."

            elif data.startswith("FILE "):
                filename = data[5:].strip()
                if os.path.isfile(filename):
                    with open(filename, "r") as f:
                        respuesta = f.read(500)  # Máx 500 caracteres
                else:
                    respuesta = "Archivo no encontrado."

            elif ":" in data:  # Login
                user, pwd = data.split(":", 1)
                if USUARIOS.get(user) == pwd:
                    respuesta = "LOGIN OK"
                else:
                    respuesta = "LOGIN FAILED"

            else:
                respuesta = "Comando desconocido"

            conn.sendall((respuesta + '\n').encode())


        except Exception as e:
            print(f"Error con {addr}: {e}")
            break

    conn.close()
    print(f"Desconectado {addr}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1234))
    server.listen()
    print("Servidor escuchando en puerto 1234...")

    while True:
        conn, addr = server.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()

if __name__ == "__main__":
    main()
