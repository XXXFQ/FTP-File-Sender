import argparse
import ftplib
from pathlib import Path

from .utils import Logger

logger = Logger.getLogger(__name__)

def send_file_over_ftp(
    host: str,
    source_file_path: str,
    target_folder: str='./',
    port: int=5000,
    timeout: float=30.0,
    username: str=None,
    password: str=None):
    '''
    Send a file to a server via FTP.

    Parameters
    ----------
    host : str
        Address of the FTP server
    source_file_path : str
        Path to the file to be sent
    target_folder : str
        Target folder path on the server (default is current directory)
    port : int
        Port number to connect to (default is 5000)
    timeout : float
        Timeout in seconds (default is 30.0)
    username : str, optional
        Username for FTP login (default is None for anonymous login)
    password : str, optional
        Password for FTP login (default is None)
    '''
    logger.info("Attempting to send file via FTP...")

    # Validate file path to prevent directory traversal attacks
    source_path = Path(source_file_path).resolve()
    if not source_path.is_file():
        logger.error(f"Source file '{source_file_path}' does not exist or is not a file.")
        return
    
    # Construct target file path on the server
    target_file_path = Path(target_folder) / source_path.name 
    
    # Initialize and connect to FTP server with a context manager to ensure disconnection
    try:
        with ftplib.FTP() as ftp_client:
            ftp_client.connect(host, port, timeout)
            logger.info(f"Connected to {host} on port {port}")
            logger.info(f"Server response: {ftp_client.getwelcome()}")
            
            # Login with provided credentials or use anonymous login
            if username and password:
                ftp_client.login(user=username, passwd=password)
                logger.info("Login successful with provided credentials")
            else:
                ftp_client.login()
                logger.info("Anonymous login successful")
            
            # Send the file using context manager for file opening
            logger.info(f"Sending file '{source_file_path}' to '{target_folder}' on the server")
            with open(source_file_path, "rb") as file:
                ftp_client.storbinary(f"STOR {target_file_path}", file)
            logger.info(f"File '{source_file_path}' sent successfully to '{target_folder}'")
    
    except ftplib.all_errors as e:
        logger.error(f"FTP error occurred: {e}")
    except OSError as e:
        logger.error(f"File handling error: {e}")
    finally:
        logger.info("FTP connection closed")

def _init_parser() -> argparse.ArgumentParser:
    '''
    Initialize the parser for command-line arguments.

    Returns
    -------
    parser : argparse.ArgumentParser
        Configured argument parser
    '''
    parser = argparse.ArgumentParser(description='FTP File Sender')
    
    # Adding arguments
    parser.add_argument('host', type=str, nargs='?', help='Host address of the destination server (e.g., 192.168.1.3)')
    parser.add_argument('path', type=str, nargs='?', help='Path to the file to be sent (e.g., ./example_file.txt)')
    parser.add_argument('-f', '--folder', type=str, help='Destination folder path on the server (default is current directory: ./)', default='./')
    parser.add_argument('-p', '--port', type=int, help='Port number for server connection (default is 5000)', default=5000)
    parser.add_argument('-t', '--timeout', type=float, help='Connection timeout in seconds (default is 30.0 seconds)', default=30.0)
    parser.add_argument('-u', '--username', type=str, help='Username for FTP login (default is None for anonymous login)', default=None)
    parser.add_argument('-pw', '--password', type=str, help='Password for FTP login (default is None)', default=None)
    
    return parser

def _check_args(args: argparse.Namespace) -> bool:
    '''
    Check if the required arguments are provided.
    
    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments from the command line
    
    Returns
    -------
    bool
        True if all required arguments are provided, False otherwise
    '''
    # ホストアドレスが指定されているか
    if not args.host:
        logger.error('Host address is required')
        return False
    
    # ファイルパスが指定されているか
    if not args.path:
        logger.error('File path is required')
        return False
    
    return True

def main(argv=None):
    '''
    Main function to send a file over FTP.
    '''
    parser = _init_parser()
    args = parser.parse_args(argv)
    
    # 引数が正しいかチェック
    if not _check_args(args):
        parser.print_usage()
        logger.error("Please provide the required arguments")
        return

    # ファイルを送信
    send_file_over_ftp(args.host, args.path, args.folder, args.port, args.timeout)

__all__ = [
    'main'
]