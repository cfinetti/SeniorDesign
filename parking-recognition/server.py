import socket
import time
hostname = socket.gethostname()
HOST= socket.gethostbyname(hostname)
PORT = 64623
verificationCode = ""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Request Recieved From {addr}")
            fileDat = b""
            initTime = time.time()
            while True:
                data = conn.recv(1048576)
                if not data:
                    break
                elif verificationCode=="":
                    verificationCode = data.decode()
                    if verificationCode != "sugmaballsorsomething":
                        verificationCode=""
                        continue
                    conn.sendall(b"Recieved")
                else:
                    fileDat+=data
                
            print(time.time()-initTime)
            filePath = "./currentcount.dat"
            verificationCode=""
            result = open(filePath, mode="wb")
            result.write(fileDat)
            result.close()