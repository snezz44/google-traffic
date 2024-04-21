import paramiko
import os

#vm connect-------------------------------------------------------
def execute_ssh_command(hostname, username, password, command):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        #connect
        ssh_client.connect(hostname, username=username, password=password)
        #command
        stdin, stdout, stderr = ssh_client.exec_command(command)
        #read
        for line in stdout:
            print(line.strip())

        for line in stderr:
            print(line.strip())

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        # close ssh
        ssh_client.close()


if __name__ == "__main__":
    hostname = "188.68.247.171"
    username = "root"
    password = "PzPwr.pl"

    command = "cd google-traffic && python3 read_db_into_heatmap.py"
    execute_ssh_command(hostname, username, password, command)

#open and download file--------------------------------------------------------------------------------
def download_file_from_vm(host, username, password, remote_path, local_path):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        #connect
        ssh_client.connect(host, username=username, password=password)
        #scp
        with ssh_client.open_sftp() as sftp:
            #download
            sftp.get(remote_path, local_path)

        print(f"Plik {remote_path} został pobrany pomyślnie do {local_path}")
    except Exception as e:
        print(f"Wystąpił błąd podczas pobierania pliku: {e}")
    finally:
        #close ssh connection
        ssh_client.close()

def open_image_file(file_path):
    os.system(f'start {file_path}')


hostname = "188.68.247.171"
username = "root"
password = "PzPwr.pl"

file_path = r'D:\google-traffic-master\google-traffic-master\heatmap.png'
remote_path = '/root/google-traffic/heatmap.png'
local_path = 'heatmap.png'
download_file_from_vm(hostname, username, password, remote_path, local_path)
open_image_file(file_path)