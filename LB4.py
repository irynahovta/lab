import socket
import threading
import time

# Echo Server

def echo_server():
    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Echo Server is listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

# Echo Client

def echo_client():
    HOST = '127.0.0.1'
    PORT = 65432

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            while True:
                message = input("Enter message to send (or 'exit' to quit): ")
                if message.lower() == 'exit':
                    break
                s.sendall(message.encode())
                data = s.recv(1024)
                print(f"Received: {data.decode()}")
    except ConnectionRefusedError:
        print("Error: Could not connect to the server. Make sure the server is running.")

# Multi-Client Server

def multi_client_server():
    HOST = '127.0.0.1'
    PORT = 65432

    def handle_client(conn, addr):
        print(f"Connected by {addr}")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Multi-Client Server is listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

# File Server

def file_server():
    HOST = '127.0.0.1'
    PORT = 65433

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"File Server is listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                with open("received_file.txt", "wb") as f:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        f.write(data)
                print("File received and saved as 'received_file.txt'")

# File Client

def file_client():
    HOST = '127.0.0.1'
    PORT = 65433
    FILE_PATH = "file_to_send.txt"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            with open(FILE_PATH, "rb") as f:
                print("Sending file...")
                while chunk := f.read(1024):
                    s.sendall(chunk)
            print("File sent.")
    except ConnectionRefusedError:
        print("Error: Could not connect to the server. Make sure the server is running.")
    except FileNotFoundError:
        print(f"Error: File '{FILE_PATH}' not found.")

# Helper to run servers in background

def run_in_background(target):
    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    time.sleep(1)  # Ensure the server has started before continuing

# Main Function

def main():
    while True:
        print("\nChoose the mode to run:")
        print("1 - Echo Server")
        print("2 - Echo Client")
        print("3 - Multi-Client Server")
        print("4 - File Server")
        print("5 - File Client")
        print("0 - Exit")

        choice = input("Enter your choice (0-5): ")
        if choice == "1":
            run_in_background(echo_server)
            print("Echo Server started in the background.")
        elif choice == "2":
            echo_client()
        elif choice == "3":
            run_in_background(multi_client_server)
            print("Multi-Client Server started in the background.")
        elif choice == "4":
            run_in_background(file_server)
            print("File Server started in the background.")
        elif choice == "5":
            file_client()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
