import paramiko
import paramiko.ssh_exception
from .logger import get_logger

logger = get_logger(__name__)
remote_ip =None
def progress_callback(transferred, to_be_transferred):
    global remote_ip
    progress = (transferred / to_be_transferred) * 100
    logger.debug(f"Transferred {remote_ip} Progress: {progress:.2f}%")

class SSH_Client():
    client :paramiko.SSHClient
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    
    def connect(self,ip: str,username: str,port: int,password =None,private_key_path=None):
        if private_key_path is not None:
            private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
            self.client.connect(hostname=ip,username=username,port=port,pkey=private_key)
        else:
            self.client.connect(hostname=ip,username=username,password=password,port=port)

    def exec(self,cmd):
        _ ,stdout,stderr =self.client.exec_command(cmd)
        ret=stdout.channel.recv_exit_status()
        if ret ==0:
            std = stdout.readline().strip()
        else:
            std = stderr.readline().strip()
        logger.debug(f"exec_cmd:{cmd},ret:{ret},std,{std}")
        return ret,std

    def send_file(self,local_file_path,remote_file_path,ip=None):
        global remote_ip 
        remote_ip=ip
        sftp = self.client.open_sftp()
        sftp.put(local_file_path,remote_file_path,progress_callback,confirm=True)
        sftp.close()


    def close_client(self):
        self.client.close()
        
    
