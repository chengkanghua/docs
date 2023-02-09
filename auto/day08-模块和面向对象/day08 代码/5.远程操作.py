import paramiko


def upload_file(host, port, user, pwd, local_path, remote_path):
    transport = paramiko.Transport((host, port))
    transport.connect(username=user, password=pwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    transport.close()


def exe_cmd(host, port, user, pwd, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=port, username=user, password=pwd)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read()
    stdout.close()
    print(result)


def run():
    server_list = [
        ("10.211.55.1", 22, 'root', '123'),
        ("10.211.55.1", 22, 'root', '123'),
        ("10.211.55.1", 22, 'root', '123'),
        ("10.211.55.1", 22, 'root', '123'),
    ]
    for item in server_list:
        pass


if __name__ == '__main__':
    run()
