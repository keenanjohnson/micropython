import socket

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 8000))

# Create a client socket
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send test data
test_data = b'test data'
c.sendto(test_data, ('127.0.0.1', 8000))

# Test MSG_PEEK
# First peek at the data
buf = bytearray(32)
n = s.recvfrom(len(buf), socket.MSG_PEEK)
print('Peek received:', n[0])
print('Peek from:', n[1])

# Now actually receive the data
n = s.recvfrom(len(buf))
print('Actual received:', n[0])
print('Actual from:', n[1])

# The data should be the same
print('Data matches:', n[0] == test_data)

s.close()
c.close() 