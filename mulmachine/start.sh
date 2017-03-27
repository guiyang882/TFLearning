#! /bin/bash

#ps 节点执行： 
CUDA_VISIBLE_DEVICES='' python3 ./mnist_replica.py \
		--ps_hosts=10.18.103.52:2222 \
		--worker_hosts=10.18.103.52:2224,10.18.103.154:2224 \
		--job_name=ps \
		--task_index=0

#worker 节点执行:
CUDA_VISIBLE_DEVICES='' python3 ./mnist_replica.py \
		--ps_hosts=10.18.103.52:2222 \
		--worker_hosts=10.18.103.52:2224,10.18.103.154:2224 \
		--job_name=worker \
		--task_index=0

CUDA_VISIBLE_DEVICES='' python3 ./mnist_replica.py \
		--ps_hosts=10.18.103.52:2222 \
		--worker_hosts=10.18.103.52:2224,10.18.103.154:2224 \
		--job_name=worker \
		--task_index=1

#要按顺序来，ps是参数服务器，可以是多个。worker就是训练集群。 
#CUDA_VISIBLE_DEVICES=0 表示使用CUDA 
#CUDA_VISIBLE_DEVICES=‘’ 表示使用CPU
