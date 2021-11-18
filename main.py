import socket
import time
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
import numpy as np


def run():
    host_ip = ''
    socket_port = 800
    server_addr = (host_ip, socket_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_addr)
    sock.listen(1)

    while True:
        try:
            sock_connection, sock_addr = sock.accept()

            # keep receiving data until the end
            # TODO: need to handle if msg doesnt start with '$'

            header = sock_connection.recv(2).decode('utf-8')

            data_msg = ""
            if header == '$\n':
                while True:
                    partial_msg = sock_connection.recv(1).decode('utf-8')

                    if partial_msg == '#':
                        data_msg = data_msg[:-1]
                        break
                    else:
                        data_msg += partial_msg
            else:
                print("Error receiving data message")

            process_mmt_data(data_msg)

            time.sleep(1)
        except socket.error:
            time.sleep(2)


def process_mmt_data(data_msg):
    """Take string data message and plot out the result

    :param data_msg: "t1 d1\nt2 d2\n.........."
    :return: 1 or 0: whether the result is an outlier
    """
    print("processing Momentum data")
    data_msg = data_msg.split('\n')
    ts = []
    data = []
    for i in range(len(data_msg)):
        ts.append(float(data_msg[i].split(' ')[0]))
        data.append(float(data_msg[i].split(' ')[1]))

    # analyse the data
    peaks_idx, _ = find_peaks(data, height=0.02)

    plt.figure()
    plt.plot(ts, data)
    plt.show()


if __name__ == '__main__':
    run()

