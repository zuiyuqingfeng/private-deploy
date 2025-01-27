#!/bin/bash 

if test -d $HOME/.kube;then
    mkdir -p $HOME/.kube
    sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config

fi
# 修改kube-controller-manager.yaml配置文件
# ! grep "allocate-node-cidrs=true" /etc/kubernetes/manifests/kube-controller-manager.yaml >/dev/null && sed -i "13a\    - --allocate-node-cidrs=true" /etc/kubernetes/manifests/kube-controller-manager.yaml
# ! grep "cluster-cidr=10.244.0.0/16" /etc/kubernetes/manifests/kube-controller-manager.yaml >/dev/null && sed -i "14a\    - --cluster-cidr=10.244.0.0/16" /etc/kubernetes/manifests/kube-controller-manager.yaml
# systemctl restart kubelet 
kubectl apply -f /tmp/kube-flannel.yaml


#添加命令补全
source <(kubectl completion bash)
! grep "kubectl completion bash"  ~/.bashrc && echo "source <(kubectl completion bash)" >> ~/.bashrc

# 安装helm
cp -f /tmp/linux-amd64/helm /usr/local/bin/helm