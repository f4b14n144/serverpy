import asyncio
import websockets
import datetime
import os

USUARIOS = {
    "FAMB": "1234",
    "admin": "adminpass"
}

async def manejar_cliente(websocket):
    print("Cliente conectado")
    try:
        async for mensaje in websocket:
            print(f"Mensaje recibido: {mensaje}")

            if mensaje == "GET TIME":
                respuesta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            elif mensaje.startswith("ECO "):
                respuesta = mensaje[4:]

            elif "+" in mensaje:
                try:
                    respuesta = str(eval(mensaje))
                except:
                    respuesta = "Operación inválida."

            elif mensaje.startswith("FILE "):
                filename = mensaje[5:].strip()
                if os.path.isfile(filename):
                    with open(filename, "r") as f:
                        respuesta = f.read(500)
                else:
                    respuesta = "Archivo no encontrado."

            elif ":" in mensaje:
                user, pwd = mensaje.split(":", 1)
                if USUARIOS.get(user) == pwd:
                    respuesta = "LOGIN OK"
                else:
                    respuesta = "LOGIN FAILED"

            else:
                respuesta = "Comando desconocido"

            await websocket.send(respuesta)

    except websockets.exceptions.ConnectionClosed:
        print("Cliente desconectado")

async def main():
    async with websockets.serve(manejar_cliente, "localhost", 8765):
        print("Servidor WebSocket en puerto 8765...")
        await asyncio.Future()  # Mantener el servidor corriendo

if __name__ == "__main__":
    asyncio.run(main())
