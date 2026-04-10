import socket
import threading
import pickle
import time
import random
import logger as log


def handle_client(conn, addr):
    """
    Handles a single client connection.
    Receives data from the client and echoes it back.
    """
    log.success(f"Connected by {addr}")
    command_timeout = 0.2
    last_command_time = time.time()
    enemy_player = None

    while True:
        # Receive data from the client (buffer size 1024 bytes)
        data = conn.recv(2048)
        if not data:
            # If no data is received, the client has disconnected
            log.error(f"Client {addr} disconnected.")
            break

        message = data.decode('utf-8')
        if message == "disconnect":
            log.info(f"Client {addr} requested disconnection.")
            break
        elif message == "surrender":
            log.info(f"Client {addr} surrendered")

        message = pickle.dumps(["a"])

        conn.sendall(message)


def start_server(host, port):
    """
    Starts the server, binds to the specified host and port,
    and listens for incoming client connections.
    Each new connection is handled in a separate thread.
    """

    # Create a socket object using IPv4 and TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Bind the socket to the host and port
            s.bind((host, port))
            # Listen for incoming connections (allow up to 2 queued connections)
            s.listen(2)
            log.info(f"Server listening on {host}:{port}")
        except OSError:
            log.warning("Coudn't start server, if the port is already in use, you will join the server, if the ip or port is invalid, then please correct it.")
            return
        except OverflowError:
            log.error("The port must be 0-65535")
            return

        while True:
            # Accept a new connection
            # conn is a new socket object usable to send and receive data
            # addr is the address of the client
            conn, addr = s.accept()
            # Start a new thread to handle the client connection
            client_handler = threading.Thread(target=handle_client, args=(conn, addr))
            client_handler.start()
