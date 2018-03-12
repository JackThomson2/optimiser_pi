
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
from bluetooth import *
from sensor import mpu6050
from reader import DataStore
 
class LoggerHelper(object):
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level

    def write(self, message):
        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())

# Main loop
def main():
    store = DataStore()
    
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
                if data == "bgetop":
                    response = "op:%s" % ",".join(operations)
                elif data == b"start":
                    if logging_thread is None:
                        stop = threading.Event()
                        logging_thread = threading.Thread(target=store.log_data,args=(stop,))
                        logging_thread.start()
                    response = b"true"
                elif data == b"stop":
                    if logging_thread is not None:
                        stop.set()
                        logging_thread.join()
                        logging_thread = None
                    response = b"true"
                elif data == b"transaction:init":
                    response = store.init_send()
                elif data == b"transaction:continue":
                    response = store.get_chunk()
                elif data == b"dump":
                    response = store.get_dump()
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


main()
