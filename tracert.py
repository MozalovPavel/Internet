import socket
import os
import subprocess
import sys
import cmd
import re
import select

HOST = 'whois.ripe.net'
PORT = 43

def as_socket(s,ip_add):
    temp_str = ('%s\r\n' % ip_add)
    b = bytearray(temp_str.encode("utf-8"))
    s.sendall(b)
    while True:
        buf = s.recv(1024).decode("utf-8")
        if len(buf) == 0:
            break
    return buf

def main():
    srt = subprocess.check_output(['tracert', '194.226.235.185'], shell=True).decode(sys.getfilesystemencoding())
    answer = []
    s = socket.create_connection((HOST,PORT))
    match = re.findall('\d+\.\d+\.\d+\.\d+', srt)
    for v in match[1:]:
        answer.append(v)
    res = []
    for v in answer:
        str = as_socket(s, v)
        if (str is None) or (len(str) == 0):
            res.append("нет As")
        else:
            a_sys = re.findall(r'AS\d+', str)
            for e in a_sys:
                res.append(re.findall('\d+', e))

    for e in range(0, len(res)):
        print(answer[e], res[e])


if __name__ == "__main__":
    main()