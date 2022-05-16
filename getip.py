import socket

# 获取计算机名称
hostname = socket.gethostname()
# 获取本机IP
ip = socket.gethostbyname(hostname)
print(ip)
