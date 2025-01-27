

import yaml,os
from .paramiko_client import SSH_Client
from .logger import get_logger

_init_master = False
_join_cmd = None


logger = get_logger(__name__)


def install_k8s(conf):
    global _init_master
    global _join_cmd
    client = SSH_Client()
    # 生成配置文件
    #render_kubeconfig(conf['slb'])
    #send_kubeadm_conf(conf,client)
    # 使用kubeadm 安装master节点
    install_master(conf,client)
    install_worker(conf,client)

def install_master(conf,client:SSH_Client):
    global _init_master
    global _join_cmd
    init_cmd="kubeadm init --control-plane-endpoint {0}:6443 --pod-network-cidr=10.244.0.0/16 --image-repository=registry.cn-hangzhou.aliyuncs.com/google_containers --kubernetes-version=1.28.0 |tee /tmp/kubeadm-init.log"
    for ip in conf['master']:
        if not _init_master:
            client.connect(ip=ip,username=conf['ssh_user'],password=conf['ssh_password'],port=conf['ssh_port'],private_key_path=conf['ssh_private_key_path'])
            
            # 初始化集群 
            # kubeadm init 
            ret, std = client.exec(init_cmd.format(conf["slb"]))
            if ret!=0:
                logger.error(std)
                exit(2)
            else:
                logger.info(std)
                
            _init_master=True

            # 初始化master 节点配置
            ret, std = client.exec("bash  /tmp/init-master.sh")
            if ret == 0 :
                logger.info("init master success")
            else:
                logger.warning("init master failed ,please check.")
            # 生成join cmd
            ret,std = client.exec('kubeadm token create --print-join-command')
            if ret == 0:
                _join_cmd=std 
            else:
                logger.error(f"generate join master cmd error, try to run 'kubeadm token create --print-join-command' on the {ip} server ")
                logger.error(std)


            remote_ca_file="/tmp/ca.tar.gz"
            local_ca_file="./ca.tar.gz"
            client.get_file(remote_ca_file,local_ca_file)

        else:
            if _join_cmd!=None:
                
                local_ca_file="./ca.tar.gz"

                client.connect(ip=ip,username=conf['ssh_user'],password=conf['ssh_password'],port=conf['ssh_port'],private_key_path=conf['ssh_private_key_path'])
                
                client.send_file(local_ca_file,"/tmp/ca.tar.gz",ip=ip)
                
                logger.info(f"send kubernetes CA file to {ip}")

                ret, std = client.exec("tar -zxf /tmp/ca.tar.gz -C /")
                if ret == 0 :
                    logger.info(f"decompress ca file on {ip} succeeded.")
                else:
                    logger.error(f"decompress ca file on {ip} failed ,please check.")

                logger.info(f"join master: exec {_join_cmd} --control-plane on {ip}")
                ret, std = client.exec(_join_cmd+"  --control-plane")
                if ret!=0:
                    logger.error(f'join master {ip} error,please check')
                    logger.error(std)
                else:
                    logger.info(f'join master {ip} success!')
                    logger.info(std)

                # 初始化master 节点配置
                ret, std = client.exec("bash /tmp/init-master.sh")
                if ret == 0 :
                    logger.info("init {ip} success")
                else:
                    logger.warning("init {ip} failed ,please check.")

def install_worker(conf,client):
    global _join_cmd
    if _join_cmd != None:
        for ip in conf['ips']:
            if ip not in conf['master']:
                client.connect(ip=ip,username=conf['ssh_user'],password=conf['ssh_password'],port=conf['ssh_port'],private_key_path=conf['ssh_private_key_path'])
                ret, std = client.exec(_join_cmd)
                if ret!=0:
                    logger.error(f'join worker {ip} error,please check')
                    logger.error(std)
                else:
                    logger.info(f'join worker {ip} success!')
                    logger.info(std)
            else:
                logger.info(f"join worker, skip master {ip}")
    else:
        logger.error('_join_cmd is None,Please check.')

def install_istio():
    pass



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


def init_precheck():
    pass
     

if __name__ == "__main__":

    render_kubeconfig("192.168.2.100")
    