import socket
import time

def udp_server(host='192.168.0.104', port=6001):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    
    while True:
        data, addr = sock.recvfrom(1024)
        recv_time = time.time()
        print(f"Received message from {addr} at {recv_time}: {data.decode()}")
        
        sock.sendto(data, addr)

if __name__ == "__main__":
    udp_server()