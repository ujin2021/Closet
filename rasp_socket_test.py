import socket
#from .models import RaspberryPi
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoyfQ.mP_IOdB4LEsJIeeUVaxLpG0k4NlnMesaMhU13J6gQ8M'
ip = '220.67.124.66'
# ip ='192.168.1.49'
port = 30000
def sendToken(token, ip, port) :
    print(f'token : {token}, ip : {ip}, port : {port}')
    port = int(port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :
        sock.settimeout(0.5) # 후속 소켓 연산에서 timeout 설정한 시간을 넘어가면 exception 발생
        sock.connect((ip, port))
        print('After connect success')
        
        sock.send(token.encode('utf-8'))
        print('After send token')

        data= sock.recv(1024)
        print(f'recv data : {data}')

        sock.close()

        return True

    except Exception as e :
        print('rasp_socket e: ', e)
        return False
sendToken(token, ip, port)
