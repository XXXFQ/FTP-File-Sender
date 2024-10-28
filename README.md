# FTP File Sender

This Python script is used to send files to a server using the FTP protocol. 
It supports configurable options for server address, file path, port, timeout, and authentication.

## Features

- Connects to an FTP server using provided host address and port.
- Sends a specified file to a target folder on the server.
- Supports configurable timeout and authentication (username and password).
- Command-line interface for ease of use.

## Requirements

- Python 3.x
- `argparse`, `ftplib`, `pathlib`, and `logging` (standard Python libraries)

## Installation

No external packages are required as the script relies on Python's standard library.

## Usage

The script can be executed from the command line with the following arguments:

### Required Arguments
- `host`: The address of the FTP server (e.g., 192.168.1.3)
- `path`: The path to the file you want to send (e.g., ./example_file.txt)

### Optional Arguments
- `-f`, `--folder`: The destination folder on the server where the file will be saved (default: current directory "./").
- `-p`, `--port`: The port number for the FTP connection (default: 5000).
- `-t`, `--timeout`: The timeout in seconds for the connection (default: 30.0).
- `-u`, `--username`: Username for FTP login (default: None for anonymous login).
- `-pw`, `--password`: Password for FTP login (default: None).

### Example

```bash
python ftp_file_sender.py 192.168.1.3 ./example_file.txt -f /uploads -p 21 -t 15 -u myuser -pw mypassword
```

This example connects to the FTP server at `192.168.1.3` on port `21`, logs in using `myuser` and `mypassword`, and uploads `example_file.txt` to the `/uploads` directory on the server with a timeout of `15` seconds.

## License

This project is licensed under the MIT License.
