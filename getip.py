import socket

# 获取计算机名称
hostname = socket.gethostname()
# 获取ip地址
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('baidu.com', 80))
print(s.getsockname()[0])
s.close()
