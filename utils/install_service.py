from .paramiko_client import SSH_Client
from .logger import get_logger

logger = get_logger(__name__)


def install_service(conf):
    client = SSH_Client()
    client.connect(ip=conf['master'][0],username=conf['ssh_user'],
                   password=conf['ssh_password'],port=conf['ssh_port'],
                   private_key_path=conf['ssh_private_key_path'])
    cmd = ""
    ret , std = client.exec(f"{cmd}")
    if ret == 0 :
        logger.info(std)
    else:
        logger.error(std)