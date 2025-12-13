#!/usr/bin/env python3
"""
Alternet client program (compatible with provided alternet_server.py)

Usage:
  alternet trans "hello world" rec:123.456.78.9

Protocol format sent over TCP:

ALTERNET/1.0\n
COMMAND: TRANS\n
SIZE: <len>\n
DATA: <text>\n
END
"""

import sys
import socket

ALTERNET_PORT = 6000  # Must match server PORT


def usage():
    print("Usage:")
    print("  alternet trans \"message\" rec:<receiver_ip>")
    sys.exit(1)


def parse_args(argv):
    if len(argv) < 4:
        usage()

    command = argv[1].lower()
    message = argv[2]
    receiver = argv[3]

    if command != "trans":
        print(f"Unknown command: {command}")
        usage()

    if not receiver.startswith("rec:"):
        print("Receiver must be specified as rec:<ip>")
        usage()

    receiver_ip = receiver.split(":", 1)[1]
    return command, message, receiver_ip


def build_packet(message: str) -> bytes:
    """
    Build text transfer packet that the server expects.
    """
    msg_bytes = message.encode("utf-8")

    header = (
        "ALTERNET/1.0\n"
        "COMMAND: TRANS\n"
        f"SIZE: {len(msg_bytes)}\n"
        f"DATA: {message}\n"
        "END"
    )

    return header.encode("utf-8")


def send_packet(receiver_ip: str, packet: bytes):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((receiver_ip, ALTERNET_PORT))
        sock.sendall(packet)


def main():
    _, message, receiver_ip = parse_args(sys.argv)
    packet = build_packet(message)

    print(f"[alternet] Sending text to {receiver_ip}:{ALTERNET_PORT}")
    send_packet(receiver_ip, packet)
    print("[alternet] Transfer complete")


if __name__ == "__main__":
    main()

