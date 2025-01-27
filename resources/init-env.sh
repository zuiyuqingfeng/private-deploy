

### 初始化containerd 配置
cat > /etc/crictl.yaml <<EOF
runtime-endpoint: unix:///run/containerd/containerd.sock
image-endpoint: unix:///run/containerd/containerd.sock
timeout: 5
debug: false
EOF

containerd config default | tee /etc/containerd/config.toml

sed -i '63s/sandbox_image = "registry.k8s.io\/pause:3.6"/ sandbox_image = "registry.cn-hangzhou.aliyuncs.com\/google_containers\/pause:3.9"/' /etc/containerd/config.toml
sed -i "69s/systemd_cgroup = false/systemd_cgroup = true/" /etc/containerd/config.toml
sed -i '98s/runtime_type = ""/runtime_type = "io.containerd.runtime.v1.linux"/' /etc/containerd/config.toml

systemctl restart containerd
systemctl enable kubelet.service

# 加载内核模块
! lsmod | grep br_netfilter >/dev/null && modprobe br_netfilter && echo 'br_netfilter' | tee -a /etc/modules

# 设置内核参数
echo 1 | sudo  tee /proc/sys/net/bridge/bridge-nf-call-iptables
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

! grep "#add by laiye private deploy script" /etc/sysctl.conf > /dev/null && echo "#add by laiye private deploy script" | sudo tee -a  /etc/sysctl.conf 
! grep "net.bridge.bridge-nf-call-iptables = 1" /etc/sysctl.conf >/dev/null && echo "net.bridge.bridge-nf-call-iptables = 1" |sudo tee -a  /etc/sysctl.conf
! grep "net.ipv4.ip_forward = 1" /etc/sysctl.conf >/dev/null && echo "net.ipv4.ip_forward = 1" |sudo tee -a /etc/sysctl.conf



# 导入k8s 镜像
for i in `ls /tmp/images`; 
do
    echo "ctr -n=k8s.io image import /tmp/images/$i"|bash 
done
