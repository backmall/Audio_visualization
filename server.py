"""
Server for audio_visualization.

This is to be run on a RaspPi waiting for the client
(device with audio playback) to get the data stream of audio
"""
import socket


PORT = 42069


def run_server():
    address_port = ("", PORT)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Starting server with params: {address_port}")

        s.bind(address_port)
        s.listen()

        connection, address = s.accept()

        with connection:
            print(f"Connected by {address}")

            try:
                while True:
                    data = connection.recv(1024)  # Receive 1024 bytes
                    #print(data)
                    # TODO: Do visualization with the data

                    if not data:
                        break

            except Exception as error:
                print(f"EXCEPTION: {error}")

    print("Server closed")


if __name__ == "__main__":
    run_server()
