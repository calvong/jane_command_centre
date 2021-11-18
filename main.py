import socket
import time
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
import numpy as np

import tkinter as tk
from tkinter import simpledialog, messagebox

def run():
    host_ip = ''
    socket_port = 8888
    server_addr = (host_ip, socket_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow socket to be reused immediately
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

            is_outlier, temp  = process_mmt_data(data_msg)
            delim = ","
            msg = str(is_outlier) + delim + str(temp)
            sock_connection.sendall(msg.encode('utf-8'))

            time.sleep(1)


        except socket.error:
            time.sleep(2)
    sock.close()

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

    threshold = 0.10
    
    # analyse the data
    #peaks_idx, _ = find_peaks(data, height=0.02)
    max_val = np.max(data)
    plt.figure()
    plt.plot(ts, data)
    plt.hlines(threshold, np.min(ts), np.max(ts), colors='red', linestyle='dotted')
    plt.show()

    ROOT = tk.Tk()
    ROOT.withdraw()

    temp = 0
    if max_val > threshold:
        msgBox = messagebox.askquestion("Test",
                                        "The analysis algorithm suggest the result is an outlier. Do you want to re run the experiment with a new temperature?",
                                        icon='warning')
        if msgBox == 'yes':
            temp = simpledialog.askinteger(title="Temperature",
                                    prompt="Please enter the new temperature:")
            is_outlier = True
        else:
            temp = 0
            is_outlier = False
    else:
        # Good
        is_outlier = False
        temp = 0
        messagebox.showinfo('Analysis complete', 'Result is good!')

    return is_outlier, temp


if __name__ == '__main__':
    run()
