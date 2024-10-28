# Allow direct execution
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ftp_file_sender

if __name__ == '__main__':
    HOST_ADDRESS = "192.168.11.16"
    PORT = 5000
    TIME_OUT = 30.0
    target_folder = "./"
    source_file_path = "./devscripts/test.txt"

    ftp_file_sender.send_file_over_ftp(HOST_ADDRESS, source_file_path, target_folder, PORT, TIME_OUT)