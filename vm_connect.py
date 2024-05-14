import paramiko
import os

#dane do połączenia z vm
hostname = "188.68.247.171"
username = "root"
password = "PzPwr.pl"
#połączenie z vm i uruchomienie skryptu (read_db_into_heatmap) zmieniającego dane z bazy do postaci heatmap
def execute_ssh_command(hostname, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    command = "cd google-traffic && python3 read_db_into_heatmap.py"
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
        print(f"error: {e}")
    finally:
        # close ssh connection
        ssh_client.close()

#download_file_from_vm tworzy połączenie ssh i pobiera heatmape, jeżeli wystąpi błąd, to o tym powiadamia
def download_file_from_vm(host, username, password):
    #klient ssh
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        #connect
        ssh_client.connect(host, username=username, password=password)
        #scp
        with ssh_client.open_sftp() as sftp:
            #download
            for i in range(5):
                remote_path = rf'/root/google-traffic/heatmap{i + 1}.png'
                local_path = rf'D:\google-traffic-master\google-traffic-master\heatmap{i + 1}.png'
                sftp.get(remote_path, local_path)

        print(f" {remote_path} pobrany do {local_path}")
    except Exception as e:
        print(f"error: {e}")
    finally:
        #close ssh connection
        ssh_client.close()

#funckja do otwarcia heatmapy, QoL, żeby ułatwić sprawdzenie poprawności działania
def open_image_file(file_path):
    os.system(f'start {file_path}')

#uruchomienie skryptu
execute_ssh_command(hostname, username, password)

#wywołanie pobierania oraz prosta pętla do odczytu heatmap
download_file_from_vm(hostname, username, password)
for i in range (5):
    open_image_file(rf'D:\google-traffic-master\google-traffic-master\heatmap{i+1}.png')