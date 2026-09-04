import socket

client = socket.socket()
client.connect(('localhost',8001))
info = client.recv(1024)
print(info.decode('utf-8'))

while True:
    cmd = input('please cmd :')
    if not cmd:
        continue
    client.sendall(cmd.encode('utf-8'))
    if cmd.upper() == 'Q':
        break
    server_data = client.recv(1024)
    print(server_data.decode('utf-8'))

client.close()