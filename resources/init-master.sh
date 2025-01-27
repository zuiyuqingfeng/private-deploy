#!/bin/bash 

if [ ! -d $HOME/.kube ] ;then
    mkdir -p $HOME/.kube
    sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config
else
    rm -rf $HOME/.kube
    mkdir -p $HOME/.kube
    sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config
fi
# 修改kube-controller-manager.yaml配置文件
# ! grep "allocate-node-cidrs=true" /etc/kubernetes/manifests/kube-controller-manager.yaml >/dev/null && sed -i "13a\    - --allocate-node-cidrs=true" /etc/kubernetes/manifests/kube-controller-manager.yaml
# ! grep "cluster-cidr=10.244.0.0/16" /etc/kubernetes/manifests/kube-controller-manager.yaml >/dev/null && sed -i "14a\    - --cluster-cidr=10.244.0.0/16" /etc/kubernetes/manifests/kube-controller-manager.yaml
# systemctl restart kubelet 

MAX_RETRIES=3
RETRY_COUNT=0

install_flannel(){
    kubectl apply -f /tmp/kube-flannel.yaml
    return $?
    # if [ $? -eq 0 ];then 
    #     return 0
    # else
    #     return 1
    # fi
}

while ! install_flannel; do 
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "达到最大重试次数，命令仍然失败。"
        exit 1
    fi
    echo "命令失败，正在重试...（重试次数：$RETRY_COUNT）"
    sleep 1  # 等待1秒后重试
    ((RETRY_COUNT++))
done


#添加命令补全
#source <(kubectl completion bash)
! grep "kubectl completion bash"  ~/.bashrc && echo "source <(kubectl completion bash)" >> ~/.bashrc

# 安装helm
cp -f /tmp/linux-amd64/helm /usr/local/bin/helm
# 安装istioctl 
cp -f /tmp/istio-1.24.2/bin/istioctl /usr/local/bin/istioctl

# 打包证书
tar -zcf /tmp/ca.tar.gz /etc/kubernetes/admin.conf /etc/kubernetes/pki/ca.* /etc/kubernetes/pki/front-proxy-ca.* /etc/kubernetes/pki/sa.* /etc/kubernetes/pki/etcd/ca.*