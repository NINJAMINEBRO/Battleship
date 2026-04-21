import socket
import threading
import pickle
import time
import random
import logger as log
import player
import game
import names
import copy

names = names.Names()

def handle_client(conn, addr, game):
    log.success(f"Connected by {addr}")
    command_timeout = 0.1
    last_command_time = time.time()
    my_index = len(game.players)

    name = copy.deepcopy(names.names)
    for p in game.players:
        if p.name in name:
            name.remove(p.name)

    game.add_player(player.Player(random.choice(name), my_index))

    while True:
        if my_index == 0 and len(game.players) == 2 and not game.has_started:
            game.start_game()

        data = conn.recv(2048)
        if not data:
            # If no data is received, the client has disconnected
            log.error(f"Client {addr} disconnected.")
            break

        players = copy.deepcopy(game.players)
        myplayer = players.pop(my_index)
        if players:
            enemy = players.pop(0)
        else:
            enemy = None

        message = data.decode('utf-8')
        if message == "disconnect":
            log.info(f"{game.players[my_index].name} requested disconnection.")
            break
        elif message == "surrender":
            log.info(f"{game.players[my_index].name} surrendered")
            game.game_over = True
        elif message == "a":
            pass  # message to stay connected

        elif time.time() >= last_command_time + command_timeout:
            last_command_time = time.time()
            if message.startswith("shoot"):
                if game.players[my_index].is_my_turn and game.phase == 1:
                    game.shoot_field(game.players[my_index], message)
                    winner = game.check_for_winner()
                    if winner is not None:
                        game.game_over = True
                        log.info(f"{game.players[winner].name} won!")
            elif message.startswith("random place"):
                game.rand_place(game.players[my_index])
            elif message.startswith("place"):
                if game.players[my_index].setup:
                    game.place_ship(game.players[my_index], message)

            elif message.startswith("confirm layout"):
                log.info(f"{game.players[my_index].name} finished their setup")
                game.rand_place(game.players[my_index])
                game.players[my_index].setup = False

        if game.has_started:
            game.change_phase()
            game.time_over(game.players[my_index])

        if game.is_game_over():
            message = pickle.dumps(["Game Over", game.get_game_over_stats()])
        else:
            message = pickle.dumps([myplayer, enemy, game.boardsize])

        conn.sendall(message)

def print_list(l):
    for i in range(len(l)):
        print(l[i])

def start_server(host, port, settings):
    Game = game.Game(settings)

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
            client_handler = threading.Thread(target=handle_client, args=(conn, addr, Game))
            client_handler.start()
