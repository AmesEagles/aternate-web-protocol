#!/usr/bin/env python3
import socket
import os

HOST = "0.0.0.0"
PORT = 6000  # protocol port

def recv_until(sock, delimiter):
    data = b""
    while delimiter not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

def main():
    print(f"ALTERNET server listening on port {PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            with conn:
                header = recv_until(conn, b"END")
                text = header.decode(errors="ignore")

                lines = text.splitlines()
                if not lines or lines[0].strip() != "ALTERNET/1.0":
                    continue

                cmd = None
                filename = None
                size = 0
                data_line = ""

                for line in lines:
                    if line.startswith("COMMAND:"):
                        cmd = line.split(":",1)[1].strip()

                    elif line.startswith("FILENAME:"):
                        filename = line.split(":",1)[1].strip()

                    elif line.startswith("SIZE:"):
                        size = int(line.split(":",1)[1].strip())

                    elif line.startswith("DATA:"):
                        data_line = line.split(":",1)[1].strip()

                if cmd == "TRANS":
                    print(f"[TEXT] {data_line}")

                elif cmd == "MEDTRANS":
                    print(f"[FILE] Receiving {filename} ({size} bytes)")
                    filedata = conn.recv(size)
                    with open(filename, "wb") as f:
                        f.write(filedata)
                    print("File saved.")

main()

