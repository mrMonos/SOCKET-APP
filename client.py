import socket
import pickle
import sys

HOST = "192.168.1.103"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
def starting_process(s:socket.socket):
    print("Connecting...")
    try:
        s.connect((HOST, PORT))
    except:
        sys.exit("Failed to connect!")
    else:
        print("Successfully connected")
        data = {'status':"200",'message':"Successfully connected"}
        s.send(pickle.dumps(data))
        while True:
            try:
                recv = s.recv(1024)
            except:
                continue
            else:
                try:
                    data = pickle.loads(recv)
                except EOFError:
                    reply = {"status":400,"message":"You haven't send data"}
                    s.sendall(pickle.dumps(reply))
                    break
                except:
                    reply = {"status":400,"message":"There is a problem"}
                    s.sendall(pickle.dumps(reply))
                    break    
                else:
                    print("[SERVER]:",data["message"])
                    break
        ID = "192.168.1.113-1-3"
        PASS = "admin"
        data = {'status':"AUTH",'id':ID,'pass':PASS}
        s.send(pickle.dumps(data))
        print("Authorizing...")
        while True:
            try:
                recv = s.recv(1024)
            except:
                continue
            else:
                try:
                    data = pickle.loads(recv)
                except EOFError:
                    reply = {"status":400,"message":"You haven't send data"}
                    s.sendall(pickle.dumps(reply))
                    break
                except:
                    reply = {"status":400,"message":"There is a problem"}
                    s.sendall(pickle.dumps(reply))
                    break
                else:
                    if data['status'] == "AUTH-200":
                        print("Successfully authorized!")
                        break
                    else:
                        print("Failed to authorize!")
                        break
def main_loop(conn:socket.socket):
    while True:
        try:
            recv = conn.recv(1024)
        except:
            continue
        else:
            handle_data(conn,recv)
def handle_data(conn:socket.socket,data):
    try:
        data = pickle.loads(data)
    except EOFError:
        reply = {"status":400,"message":"You haven't send data"}
        conn.sendall(pickle.dumps(reply))
    except:
        reply = {"status":400,"message":"There is a problem"}
        conn.sendall(pickle.dumps(reply))
    else:
        print("[SERVER]:",data["message"])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    starting_process(s)
    main_loop(s)