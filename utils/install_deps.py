from .paramiko_client import SSH_Client
from .logger import get_logger
import os

resouces_path="./resources/"
remote_path = "/tmp/"
remote_file_path=""
logger = get_logger(__name__)


def install_deps(conf):
    global remote_file_path 
    client = SSH_Client()
    for ip in conf['ips']:
        client.connect(ip,conf['ssh_user'],password=conf['ssh_password'],port=conf['ssh_port'],
                       private_key_path=conf['ssh_private_key_path'])
        for file in os.listdir(resouces_path):
            local_file_path = os.path.join(resouces_path,file)
            remote_file_path= os.path.join(remote_path,file)
            logger.debug(local_file_path+" :"+ remote_path)
            client.send_file(local_file_path,remote_file_path,ip)
            if remote_file_path.endswith(".tar.gz"):
                client.exec(f"tar -zxf {remote_file_path} -C {remote_path}")
        install_rpm(client)
        init_env(client)

def install_rpm(client:SSH_Client):
    cmd = "bash /tmp/install-rpm.sh"
    ret,std = client.exec(cmd)
    if ret!=0:
        logger.warning(std)

def init_env(client:SSH_Client):
    cmd = "bash /tmp/init-env.sh"
    ret, std = client.exec(cmd)
    if ret!=0:
        logger.error(std)


    
