import socket
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoyfQ.mP_IOdB4LEsJIeeUVaxLpG0k4NlnMesaMhU13J6gQ8M'
ip = '220.67.124.185'
port = 30000

def sendToken(token, ip, port) :
    print(f'token : {token}\nip : {ip}\nport : {port}')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((ip, port))
    print('After connect success')

    sock.send(token.encode('utf-8'))
    print('After send token')

    # rasp table status 1로 변경코드 넣기(연결 되었다는 뜻)

    data= sock.recv(1024)
    print(f'recv data : {data}')
    
    # sock.close()
    # return True

sendToken(token, ip, port)
