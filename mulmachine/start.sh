#! /bin/bash

ps.machine.com=192.168.1.100
worker01.machine.com=192.168.1.100
worker02.machine.com=192.168.1.100
#ps 节点执行： 
CUDA_VISIBLE_DEVICES='' python distribute.py \
		--ps_hosts=ps.machine.com:2222 \
		--worker_hosts=worker01.machine.com:2224,worker02.machine.com:2225 \
		--job_name=ps \
		--task_index=0

#worker 节点执行:
CUDA_VISIBLE_DEVICES='' python distribute.py \
		--ps_hosts=ps.machine.com:2222 \
		--worker_hosts=worker01.machine.com:2224,worker02.machine.com:2225 \
		--job_name=worker \
		--task_index=0

CUDA_VISIBLE_DEVICES='' python distribute.py \
		--ps_hosts=ps.machine.com:2222 \
		--worker_hosts=worker01.machine.com:2224,worker02.machine.com:2225 \
		--job_name=worker \
		--task_index=1 

#要按顺序来，ps是参数服务器，可以是多个。worker就是训练集群。 
#CUDA_VISIBLE_DEVICES=0 表示使用CUDA 
#CUDA_VISIBLE_DEVICES=‘’ 表示使用CPU