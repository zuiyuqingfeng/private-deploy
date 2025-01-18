

import yaml,os
from .paramiko_client import SSH_Client
from .logger import get_logger

_init_master=False
logger = get_logger(__name__)

def init_master(conf):
    global _init_master
    client = SSH_Client()
    render_kubeconfig(conf['master'][0])
    send_kubeadm_conf(conf,client)
    load_images(conf,client)

def render_kubeconfig(ip):
    
    tempfile = 'config/template/kubeadm.yaml'
    configfile = 'config/conf/kubeadm.yaml'
    PWD = os.getcwd()
    tempfile_path = os.path.join(PWD,tempfile)
    configfile = os.path.join(PWD,configfile)

    with open(tempfile_path,'r') as f:
        data = list(yaml.safe_load_all(f))
        data[0]['localAPIEndpoint']['advertiseAddress'] = ip
        # for i in data[0]:
        #     if 'localAPIEndpoint' in i and 'advertiseAddress' in i['localAPIEndpoint']:
        #         data[0]['localAPIEndpoint']['advertiseAddress']=ip

    with open (configfile,'w') as f:
        yaml.safe_dump_all(data, f,default_flow_style=False)    

def send_kubeadm_conf(conf,client:SSH_Client):
    client.connect(ip=conf['master'][0],username=conf['ssh_user'],password=conf['ssh_password'],port=conf['ssh_port'],private_key_path=conf['ssh_private_key_path'])
    PWD =os.getcwd()
    local_kubeadm_conf_path= os.path.join(PWD,"config/conf/kubeadm.yaml")
    remote_kubeadm_conf_path = "/tmp/kubeadm.yaml"
    client.send_file(local_file_path=local_kubeadm_conf_path,remote_file_path=remote_kubeadm_conf_path,ip=conf['ips'][0])

def load_images(conf,client:SSH_Client):
    for ip in conf['ips']:
        client.connect(ip=ip,username=conf['ssh_user'],password=conf['ssh_password'],port=conf['ssh_port'],private_key_path=conf['ssh_private_key_path'])
        ret, std = client.exec('bash /tmp/init-master.sh')
        if ret!=0:
            logger.error(std)
        else:
            logger.info(std)


def inti_precheck():
    pass
     

if __name__ == "__main__":

    render_kubeconfig("192.168.2.100")
    