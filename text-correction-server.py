#!/usr/bin/env python3

import jamspell
import socket




HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


corrector = jamspell.TSpellCorrector()

if corrector.LoadLangModel('model_gds2.bin'):
    print('corrector ready')




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
                
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                words = data.decode('utf8').split(' ')
                for i in range(len(words)):
                    print(words[i],corrector.GetCandidates(words,i))
                # print()
                conn.sendall(corrector.FixFragment(data.decode('utf8')).encode())


