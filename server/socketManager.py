import json
import struct

class SocketManager:
    def __init__(self, socket):
        self.socket = socket
    
    def send_dict_to_json(self,  data):
        self.socket.send(json.dumps(data).encode('utf-8'))
    
    def send_integer(self,  data):
        self.socket.sendall(struct.pack("!I", data))

    def send_string(self,  data):
        self.socket.send(data.encode('utf-8'))

    def send_by_package_dict_to_json(self,  data, package_size_kb=1):
        #? transformar o data em um json - (array or dict)
        data_json = json.dumps(data)
        #? transformar o json em bytes
        bin_data = data_json.encode('utf-8')

        package_size = 1024*package_size_kb
        i = 0
        while i < len(bin_data):
            #? Divide o json em pacotes
            package = bin_data[i:i+package_size]
            #? Envia o tamanho do pacote
            self.send_integer(len(package))
            #? Envia o pacote
            self.socket.sendall(package)
            i += package_size
        #? informa que o envio foi concluído
        self.send_integer( 0)

    def receive_json_to_dict(self,  package_size=1024):
        data = self.socket.recv(package_size).decode('utf-8')
        return json.loads(data)

    def receive_integer(self):
        return struct.unpack("!I", self.socket.recv(4))[0]
    
    def receive_string(self,  package_size=1024):
        return self.socket.recv(package_size).decode('utf-8')
    
    def receive_by_package_json_to_dict(self):
        def recvall(sock, n):
            packages = []
            total = 0

            while total < n:
                package = sock.recv(n - total)
                if not package:
                    return None
                packages.append(package)
                total += len(package)
            return b''.join(packages)
        
        data_bytes = bytearray()
        while True:
            tamanho_pacote = recvall(self.socket, 4)
            if not tamanho_pacote:
                break

            tamanho = struct.unpack("!I", tamanho_pacote)[0]
            if tamanho == 0:
                break

            package_data = recvall(self.socket, tamanho)
            if not package_data:
                break

            data_bytes.extend(package_data)

        received_json = data_bytes.decode('utf-8')
        return json.loads(received_json)