# private deploy services on kubernetes


#### 这个项目用于一键化部署k8s 1.28.0版本
```
cat > config.yaml <<EOF
ips: 
  - "192.168.3.1"
  - "192.168.3.2"
  - "192.168.3.3"
  - "192.168.3.4"
  - "192.168.3.5"
  - "192.168.3.6"
ssh_user: "root"
ssh_password: "123456"
ssh_port: 22
ssh_private_key_path: 
master:
  - "192.168.3.1"
slb: "192.168.3.100"
EOF


bash main.sh
```

#### 
- 如果配置ssh_private_key_path 路径，则优先使用密钥登陆，密钥为空时使用密码登陆
- 需要提前在slb 上配置6443端口到master节点的转发，单机部署时可以直接填master-01的地址