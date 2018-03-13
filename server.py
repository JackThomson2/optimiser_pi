
#!/usr/bin/python

import logging
import logging.handlers
import argparse
import sys
import os
import time
import threading
import json
import math
import re
from bluetooth import *
from record_manager import record_manager

# Main loop
def main():
    manager = record_manager()
    
    print("Waiting for bluetooth")
    # We need to wait until Bluetooth init is done
    time.sleep(10)

    # Make device visible
    os.system("hciconfig hci0 piscan")

    # Create a new server socket using RFCOMM protocol
    server_sock = BluetoothSocket(RFCOMM)
    # Bind to any port
    server_sock.bind(("", PORT_ANY))
    # Start listening
    server_sock.listen(1)

    # Get the port the server socket is listening
    port = server_sock.getsockname()[1]

    # The service UUID to advertise
    uuid = "7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d"

    # Start advertising the service
    advertise_service(server_sock, "SuspOptimiser",
                      service_id=uuid,
                      service_classes=[uuid, SERIAL_PORT_CLASS],
                      profiles=[SERIAL_PORT_PROFILE])

    # These are the operations the service supports
    # Feel free to add more
    operations = ["ping", "example"]

    # Main Bluetooth server loop
    while True:

        print(f"Waiting for connection on RFCOMM channel {port}")

        try:
            client_sock = None

            # This will block until we get a new connection
            client_sock, client_info = server_sock.accept()
            print(f"Accepted connection from {client_info}")

            stop = threading.Event()
            logging_thread = None

            while True:

                # Read the data sent by the client
                data = client_sock.recv(1024)
                if len(data) == 0:
                    continue

                print(f"Received {data}")

                # Handle the request
                if data == b"start":
                    if logging_thread is None:
                        stop = threading.Event()
                        logging_thread = threading.Thread(target=manager.start_new_recording,args=(stop,))
                        logging_thread.start()
                    response = b"true"
                elif data == b"stop":
                    if logging_thread is not None:
                        stop.set()
                        logging_thread.join()
                        logging_thread = None
                        response = manager.get_last_data()
                    else:
                        response = b"false"
                elif info = get_transaction_continue(manager, info):
                    response = info
                elif info = get_transaction_init(manager, info):
                    response = info
                elif data == b"transaction:continue":
                    response = manager.get_chunk()
                elif data == "example":
                    response = b"This is an example"
                # Insert more here
                else:
                    response = b"Not supported"

                client_sock.send(response)

        except IOError:
            pass

        except KeyboardInterrupt:
            if client_sock is not None:
                client_sock.close()
            server_sock.close()
            print("Server going down")
            break

# Extract the name from the string and get the inital sent string
def get_transaction_init(manager, text):
    file_name = re.search(b'filename:(.+?),', text)
    if not file_name:
        return False

    name = file_name.group(1)

    return manager.get_initial_request(name)

# Extract the file name then find out which chunk should be returned
def get_transaction_continue(manager, text):
    file_name = re.search(b'filename:(.+?),', text)
    if not file_name:
        return False

    name = file_name.group(1)

    chunk_numb = re.search(b'chunk:(.+?),', text)
    if not chunk_numb:
        return False

    chunk = int(chunk_numb.group(1))

    return manager.get_send_chunk(name, chunk)

main()
