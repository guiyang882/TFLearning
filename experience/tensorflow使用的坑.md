## 主要用来记录在tensorflow使用的日常中遇到的那些坑
### Tensorflow设置显存自适应，显存比例
对于tensorlfow一运行，显存就满了，该如何处理
- 按照比例操作
```bash
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.4
session = tf.Session(config=config, ...)
```
- 按照需求增长
```bash
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config, ...)
```