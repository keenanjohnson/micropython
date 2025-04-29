# TLS PSK Support in MicroPython

This document describes the TLS Pre-Shared Key (PSK) support in MicroPython.

## Overview

TLS PSK (Pre-Shared Key) is a mode of TLS that uses symmetric keys instead of certificates for authentication. This can be useful in resource-constrained environments or when certificate management is impractical.

MicroPython supports TLS PSK through the `tls` module, which is based on mbedtls.

## Usage

### Setting up PSK on an SSLContext

```python
import tls

# Create an SSL context
context = tls.SSLContext(tls.PROTOCOL_TLS_CLIENT)  # or tls.PROTOCOL_TLS_SERVER

# Set PSK identity and key
context.set_psk_identity("client1")  # Identity is a string
context.set_psk_key(b"secret-key")   # Key is a bytes object

# Enable PSK mode
context.set_ciphers("PSK")

# Use the context to wrap a socket
ssl_sock = context.wrap_socket(sock, server_hostname="example.com")
```

### Client Example

```python
import socket
import tls

# Create a socket and connect
s = socket.socket()
s.connect(('example.com', 8443))

# Set up PSK
context = tls.SSLContext(tls.PROTOCOL_TLS_CLIENT)
context.set_psk_identity("client1")
context.set_psk_key(b"secret-key")
context.set_ciphers("PSK")

# Wrap socket and communicate
ssl_sock = context.wrap_socket(s, server_hostname="example.com")
ssl_sock.write(b"Hello")
data = ssl_sock.read(1024)
ssl_sock.close()
```

### Server Example

```python
import socket
import tls

# Create a socket and listen
s = socket.socket()
s.bind(('0.0.0.0', 8443))
s.listen(5)

# Set up PSK
context = tls.SSLContext(tls.PROTOCOL_TLS_SERVER)
context.set_psk_identity("client1")
context.set_psk_key(b"secret-key")
context.set_ciphers("PSK")

# Accept connections
client, addr = s.accept()
ssl_sock = context.wrap_socket(client, server_side=True)
data = ssl_sock.read(1024)
ssl_sock.write(b"Response")
ssl_sock.close()
```

## API Reference

### `SSLContext.set_psk_identity(identity)`

Sets the PSK identity to be used for authentication.

- `identity`: A string containing the PSK identity.

### `SSLContext.set_psk_key(key)`

Sets the PSK key to be used for authentication.

- `key`: A bytes object containing the PSK key.

### `SSLContext.set_ciphers("PSK")`

Enables PSK mode and configures the context to use PSK ciphersuites.

## Notes

- Both the client and server must use the same PSK identity and key.
- The PSK identity is transmitted in plaintext, but the key is not.
- PSK mode is more efficient than certificate-based authentication, making it suitable for resource-constrained devices.
- For security reasons, use strong, random keys and keep them secret.

## Example Files

Complete examples can be found in the `examples/network/` directory:
- `tls_psk_client.py`: A client example using TLS PSK
- `tls_psk_server.py`: A server example using TLS PSK