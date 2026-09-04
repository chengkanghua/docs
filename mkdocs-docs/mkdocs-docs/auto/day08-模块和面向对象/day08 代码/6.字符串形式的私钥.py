import paramiko
from io import StringIO

key_str = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIB37Le5SbLDddwCNxGlBzbpBa0=
-----END RSA PRIVATE KEY-----"""

private_key = paramiko.RSAKey(file_obj=StringIO(key_str))

transport = paramiko.Transport(('10.0.1.40', 22))
transport.connect(username='wupeiqi', pkey=private_key)

ssh = paramiko.SSHClient()
ssh._transport = transport

stdin, stdout, stderr = ssh.exec_command('df')
result = stdout.read()

transport.close()

print(result)
