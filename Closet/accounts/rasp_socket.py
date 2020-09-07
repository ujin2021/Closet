import socket
from .models import RaspberryPi

def sendToken(token, user_id, ip, port) :
    try :
        print(f'token : {token}, user_id : {user_id}, ip : {ip}, port : {port}')
        port = int(port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((ip, port))
        print('After connect success')

        sock.send(token.encode('utf-8'))
        print('After send token')

        data= sock.recv(1024)
        print(f'recv data : {data}')

        sock.close()

        rasp = RaspberryPi.objects.get(ip=ip, port=port, user_id=user_id)
        rasp.status = 1
        rasp.save()

        return True
        
    except Exception as e :
        print('rasp_socket e: ', e)
        return False