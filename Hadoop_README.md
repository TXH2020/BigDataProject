# Hadoop

In my opinion, there are two ways to operate a hadoop cluster: with and without containerization. Container images encapsulate the cluster components and their respective configurations. Hence, it is much simpler to setup a pseudo-distributed cluster on docker than a real preudo-distributed cluster. Morover, they provide the advantages of containerization: isolation and portability. However, one issue was found. The datanode URL is not resolvable by the docker host. It can be resolved only by the namenode container. Thus, if we try to expose the namenode port and access the namenode UI through a browser, the link present for the datanode will not work. For resolving this issue, we need to add a host-IP mapping in the /etc/hosts file of the docker host. Here, the hostname is the one displayed in the URL while the IP is the IP address of the datanode container.

## Hadoop Pseudo-Distributed(single node) Cluster Setup:
1. Follow https://github.com/apache/hadoop/tree/docker-hadoop-3.4
2. I was working on a VM with no UI. Hence I had to do this on my VM to be able to see the datanode UI:
   
    ``sudo iptables -t nat -A PREROUTING -p tcp --dport 9864 -j DNAT --to-destination 172.18.0.4:9864``
   
    ``sudo iptables -A FORWARD -p tcp -d 172.18.0.4 --dport 9864 -j ACCEPT``
   
    where 172.8.0.4 is the IP of the datanode container, obtained using the docker inspect command. So on my computer hosting the VM, I have to open a browser, goto <VN_IP>:9864.



## Hadoop Guide

Link: https://www.isical.ac.in/~acmsc/WBDA2015/slides/hg/Oreilly.Hadoop.The.Definitive.Guide.3rd.Edition.Jan.2012.pdf


