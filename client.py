import socket
import logger as log


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        log.success(f"Connected to server at {host}:{port}")
        self.send_message("a")

    def send_message(self, message):
        """
        Sends a message to the server.
        :param message: The message to send (string).
        """
        self.socket.sendall(message.encode('utf-8'))

    def receive_message(self, prev_data):
        import pickle
        try:
            data = self.socket.recv(2048)
            if not data:
                log.error("Server disconnected unexpectedly.")
                return None
            received_message = pickle.loads(data)
        except pickle.UnpicklingError:
            received_message = prev_data
        except ConnectionAbortedError:
            return None
        except Exception as e:
            log.warning(f"Error receiving message: {e}")
            received_message = prev_data
        return received_message

    def disconnect(self):
        import time
        """
        Closes the socket connection to the server.
        """
        self.send_message("disconnect")
        time.sleep(0.1)  # Give the server time to process the disconnection
        self.socket.close()
        log.success("Disconnected from server.")
