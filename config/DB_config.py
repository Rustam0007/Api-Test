import paramiko

# DB configurate
DATABASE = 'test'
USER = 'autotest'
PASSWORD = 'qwerty@007'
HOST = 'localhost'
HOSTNAME = '192.170.00.101'
PORT = '5440'
SSH = paramiko.RSAKey.from_private_key_file('C:\\Users\\.ssh\\id_rsa')

# ULR for DEV
URL = 'http://192.170.00.101'

# Header configurate for request
HEADER_KEY = 'UserName'
HEADER_VALUE = 'tester'
