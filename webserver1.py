import socket
 
HOST, PORT = '', 8888

def CanBeIgnored(c):
    if c == '\n' or c == '\r' or c == ' ':
        return True
    return False

def find(sub, str):
    index, len_sub, len_str = 0, len(sub), len(str)
    while index < len_str - len_sub:
        if str[index:index+len_sub] == sub:
            return index
        index += 1

    return -1

def ParseName(str):
    name = ''
    len_str = len(str)
    index = find('name', str)
    if(index != -1):
        index += 5
        while index < len_str and str[index] != '&':
            name = str[index]
            index += 1

    return name

def ParseAge(str):
    age = ''
    len_str = len(str)
    index = find('age', str)
    if index != -1:
        index += 4
        while index < len_str and str[index] <= '9' and str[index] >='0':
            age = str[index]
            index += 1

    return age

def ParsePost(sub, str):
    data = ''
    len_str = len(str)
    len_sub = len(sub)
    index = find(sub, str)
    if index != -1:
        index += len_sub + 1
        while CanBeIgnored(str[index]):
            index += 1
        end = index
        while not CanBeIgnored(str[end]):
            end += 1
        data = str[index:end]

    return data

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    http_response = """
"""
    print request
    if "hello" in request:
        http_response += "hello, world\n" 
    elif "age=" in request:
        http_response += 'hello,I\'m %s and %s years old.' % (ParseName(request), ParseAge(request))
    else:
        http_response += 'I\'m %s and my password is %s\n' % (ParsePost('username', request), ParsePost('password', request))

    client_connection.sendall(http_response)
    client_connection.close()
