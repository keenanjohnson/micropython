# TLS PSK Server Example
# This example demonstrates how to use TLS PSK authentication in MicroPython

import socket
import tls

# PSK identity and key
PSK_IDENTITY = "client1"
PSK_KEY = b"secret-key"

# Create a socket
s = socket.socket()

# Bind to address and port
s.bind(('0.0.0.0', 8443))

# Listen for connections
s.listen(5)
print("Server listening on port 8443...")

# Create an SSL context
context = tls.SSLContext(tls.PROTOCOL_TLS_SERVER)

# Configure PSK
context.set_psk_identity(PSK_IDENTITY)
context.set_psk_key(PSK_KEY)
context.set_ciphers("PSK")  # Enable PSK mode

while True:
    # Accept connection
    client, addr = s.accept()
    print("Client connected from:", addr)
    
    try:
        # Wrap the socket with SSL
        ssl_sock = context.wrap_socket(client, server_side=True)
        
        # Receive and send data
        data = ssl_sock.read(1024)
        print("Received:", data)
        ssl_sock.write(b"Hello from server!")
        
        # Close the connection
        ssl_sock.close()
    except Exception as e:
        print("Error:", e)
    finally:
        client.close()