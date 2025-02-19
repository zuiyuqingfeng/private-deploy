for service in `jq '.services | to_entries[] | "registry.cn-zhangjiakou.aliyuncs.com/laiye-tech/\(.key):\(.value)"' version_map.json`;
do 
    echo ""$service
done


