# TLS PSK Client Example
# This example demonstrates how to use TLS PSK authentication in MicroPython

import socket
import tls

# PSK identity and key
PSK_IDENTITY = "client1"
PSK_KEY = b"secret-key"

# Create a socket
s = socket.socket()

# Connect to the server
s.connect(('example.com', 8443))

# Create an SSL context
context = tls.SSLContext(tls.PROTOCOL_TLS_CLIENT)

# Configure PSK
context.set_psk_identity(PSK_IDENTITY)
context.set_psk_key(PSK_KEY)
context.set_ciphers("PSK")  # Enable PSK mode

# Wrap the socket with SSL
ssl_sock = context.wrap_socket(s, server_hostname="example.com")

# Send and receive data
ssl_sock.write(b"Hello, world!")
data = ssl_sock.read(1024)
print("Received:", data)

# Close the connection
ssl_sock.close()
s.close()