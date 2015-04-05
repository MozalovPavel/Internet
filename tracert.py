import socket
import subprocess
import sys
import re

HOST = 'whois.ripe.net'
PORT = 43


def as_socket(s, ip_add):
    temp_str = ('%s\r\n' % ip_add)
    b = bytearray(temp_str.encode("utf-8"))
    s.sendall(b)
    buf = bytes()
    while True:
        buf = s.recv(1024).decode("utf-8")
        if len(buf):
            break
    return buf


def main():
    srt = subprocess.check_output(['tracert', '194.226.235.185'], shell=True).decode(sys.getfilesystemencoding())
    answer = []
    sock = socket.create_connection((HOST, PORT))
    match = re.findall('\d+\.\d+\.\d+\.\d+', srt)
    answer.extend(match[1:])
    res = []
    for ip in answer:
        received = as_socket(sock, ip)
        if (received is None) or (len(received) == 0):
            res.append("нет As")
        else:
            auto_sys = re.findall(r'AS\d+', received)
            for match in auto_sys:
                res.append(re.findall('\d+', match))
    for i in range(0, len(res)):
        print(answer[i], res[i])


if __name__ == "__main__":
    main()