import socket
import pickle
import threading

HOST = "192.168.1.103"  
PORT = 65432
def handle_data(conn:socket.socket,data):
    try:
        data = pickle.loads(data)
    except:
        reply = {"status":400,"message":"You haven't send data or data is invalid"}
    else:
        if data['status'] == "CLOSE":
            print(f"Closing connection with {addr[0]}:{addr[1]}")
            conn.close()
        elif data['status'] == "AUTH":
            ID = data['id']
            PASS = data['pass']
            reply = {"status":"AUTH-200"}
        else:
            reply = {"status":200,"message":"All is right"}
            print("[CLIENT]:",data["message"])
    finally:
       conn.sendall(pickle.dumps(reply))
def handler(c:socket.socket):
    print("Handling...")
    while True:
        try:
            recv = c.recv(1024*4)
            print(f"Reciving data from {addr[0]}:{addr[1]}")
        except:
            continue
        else:
            print(f"Recived data from {addr[0]}:{addr[1]}")
            handle_data(c,recv)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print("Server is running!")
s.listen()
while True:
    conn, addr = s.accept()
    print("Connected to ",addr[0],":",addr[1],sep="")
    thread = threading.Thread(target=handler,args=(conn,))
    thread.start()