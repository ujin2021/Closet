import socket

def sendToken(token, ip, port) :
    print(f'token : {token}, ip : {ip}, port : {port}')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.sendall(token.encode('utf-8'))
    # token 전송
    # rasp table status 1로 변경(연결 되었다는 뜻)
    sock.close()

    return True