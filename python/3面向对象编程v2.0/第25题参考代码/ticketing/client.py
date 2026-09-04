import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8001))
print("门票预定系统")
while True:
    txt = input(">>>")  # 景区  or  景区-用户-asd
    client.sendall(txt.encode('utf-8'))
    if txt.upper() == 'Q':
        break
    reply = client.recv(1024)
    print(reply.decode("utf-8"))

client.close()
