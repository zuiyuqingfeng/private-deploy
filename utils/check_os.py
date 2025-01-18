from .paramiko_client import SSH_Client
from .logger import get_logger

# 输入机器硬件要求
cpu_cores = 1
memory_size = 1
disk_capacity = 20


logger = get_logger(__name__)

        
def check(conf):
    for ip in conf['ips']:
        client = SSH_Client()
        client.connect(ip,username=conf['ssh_user'],password=conf['ssh_password'],private_key_path=conf['ssh_private_key_path'],port=conf['ssh_port'])
        check_cpu(client,ip)
        check_memory(client,ip)
    return True

def check_cpu(client:SSH_Client,ip=None):
    cmd = "lscpu|grep 'CPU(s)'|grep -v On-line|awk '{print $2}'"
    ret,cpu_total=client.exec(cmd)
    if ret != 0:
            logger.error(cpu_total)
            exit(127)
    else:
        if int(cpu_total)>=cpu_cores:
            logger.info(f"it's ok for {ip}  cpu check ")
        else:
            logger.error(f"failed to check {ip} cpu_total")
            exit(127)
       

def check_memory(client: SSH_Client,ip =None):
    cmd = "lsmem  |grep 'Total online memory' |awk '{print $NF}'|sed 's/G$//'"
    ret, std =client.exec(cmd)
    mem_total = float(std)
    if ret != 0:
        logger.error(std)
        exit(127)
    else:
        if mem_total>=memory_size:
            logger.info(f"it's ok for {ip} memory check ")
        else:
            logger.error(f"failed to {ip} check memory")
            exit(127)

