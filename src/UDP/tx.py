import socket
import time

def udp_client(server_ip, server_port=6001):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    for i in range(10):
        send_time = time.time()
        message = f"Message {i} sent at {send_time}"
        sock.sendto(message.encode(), (server_ip, server_port))
        
        data, addr = sock.recvfrom(1024)
        recv_time = time.time()
        
        rtt = recv_time - send_time
        print(f"Round-trip time: {rtt:.6f} seconds\n")
        
        time.sleep(1)

if __name__ == "__main__":
    server_ip = '192.168.0.104'
    udp_client(server_ip)