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

            # Menú numérico
            if data == "1":
                respuesta = "Has seleccionado 'Eco'. Escribe: ECO tu_mensaje"
            elif data == "2":
                respuesta = "Has seleccionado 'Sumar'. Escribe una suma, por ejemplo: 4+5"
            elif data == "3":
                respuesta = datetime.datetime.now().strftime("Hora del servidor: %Y-%m-%d %H:%M:%S")
            elif data == "4":
                respuesta = "Has seleccionado 'Leer archivo'. Escribe: FILE nombre_archivo.txt"
            elif data == "5":
                respuesta = "Has seleccionado 'Login'. Escribe: usuario:clave"
            elif data == "6":
                respuesta = "Has seleccionado 'Crear archivo'. Escribe: CREATE nombre_archivo.txt contenido"
            elif data == "0":
                respuesta = "Gracias por usar el sistema. Hasta luego."
                conn.sendall((respuesta + '\n').encode())
                break

            # Comandos reales
            elif data == "GET TIME":
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

            elif data.startswith("CREATE "):
                try:
                    partes = data[7:].strip().split(" ", 1)
                    if len(partes) != 2:
                        respuesta = "Formato incorrecto. Usa: CREATE nombre_archivo.txt contenido"
                    else:
                        nombre_archivo, contenido = partes
                        with open(nombre_archivo, "w") as f:
                            f.write(contenido)
                        respuesta = f"Archivo '{nombre_archivo}' creado correctamente."
                except Exception as e:
                    respuesta = f"Error al crear archivo: {e}"

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
