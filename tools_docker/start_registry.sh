docker run -d -p 5000:5000  --name registry2-noauth --restart=always  \
    -v /usr/local/docker/registry/auth/:/auth/  \
    -v /usr/local/docker/registry/:/var/lib/registry/ \
    registry:2.6.2


# docker tag docker.io/registry:2.6.2  10.168.2.22:5000/registry:2.6.2

# hosts配置： 10.168.2.22 harbor.me


image_name="helloworld"
# 节点1
docker tag $image_name  harbor.me:5000/$image_name
docker push harbor.me:5000/$image_name

# 节点2
# ssh chenjun@10.168.2.22 "docker tag $image_name  harbor.me:5000/$image_name"
# ssh chenjun@10.168.2.22 "docker push harbor.me:5000/$image_name"
docker pull harbor.me:5000/$image_name
docker tag harbor.me:5000/$image_name $image_name
docker rmi harbor.me:5000/$image_name
