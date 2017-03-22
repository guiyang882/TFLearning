import cv2
import tensorflow as tf
import os
import time

cifar10_label_path = "/home/guiyang/Downloads/cifar/labels.txt"
cifar10_test_dir = "/home/guiyang/Downloads/cifar/test/"
cifar10_train_dir = "/home/guiyang/Downloads/cifar/train/"
cifar10_tfrecords_dir = "/home/guiyang/Downloads/cifar/tfrecords/"

def _getFeature(value, outType=None):
    if outType == tf.float32:
        return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))
    if outType == tf.int64:
        return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def CIFAR10_WTFRecord_SingleThread(readDirPath, labelPath, writeFilePath):
    # for cifar10 format: the data is (image_Value, image_label)

    def _build_Label_Dict():
        label_dict = dict()
        cnt = 1
        with open(labelPath, 'r') as handle:
            for line in handle.readlines():
                line = line.strip()
                if line not in label_dict.keys():
                    label_dict[line] = cnt
                    cnt += 1
        return label_dict

    label_dict = _build_Label_Dict()
    filelist = [(name, label_dict[name.split('.')[0].split('_')[1]]) for name in os.listdir(readDirPath) if name.endswith("png") or name.endswith("jpg") or name.endswith("jpeg")]
    writer = tf.python_io.TFRecordWriter(writeFilePath)
    for (imgpath, imglabel) in filelist:
        # print(imgpath, imglabel)
        imgRaw = cv2.imread(readDirPath + imgpath)
        example = tf.train.Example(
            features=tf.train.Features(
                feature={
                    "height":_getFeature(imgRaw.shape[0], tf.int64),
                    "width":_getFeature(imgRaw.shape[1], tf.int64),
                    "depth":_getFeature(imgRaw.shape[2], tf.int64),
                    "label":_getFeature(imglabel, tf.int64),
                    "imgRaw":_getFeature(imgRaw.tobytes())
                }
            )
        )
        writer.write(example.SerializeToString())
    writer.close()

def CIFAR10_RTFRecord_SingleThread(readFile, batch_size, num_epochs):

    def _read_and_decode(filename_queue):
        reader = tf.TFRecordReader()
        _, serialized_example = reader.read(filename_queue)
        features = tf.parse_single_example(
            serialized=serialized_example,
            features={
                "height": tf.FixedLenFeature([], tf.int64),
                "width": tf.FixedLenFeature([], tf.int64),
                "depth": tf.FixedLenFeature([], tf.int64),
                "label": tf.FixedLenFeature([], tf.int64),
                "imgRaw": tf.FixedLenFeature([], tf.string)
            }
        )
        imgRaw = tf.decode_raw(features["imgRaw"], tf.uint8)
        imgHeight = tf.cast(features["height"], tf.int64)
        imgWidth = tf.cast(features["width"], tf.int64)
        imgDepth = tf.cast(features["depth"], tf.int64)
        imgRaw.set_shape((imgHeight, imgWidth, imgDepth))
        imgLabel = tf.cast(features["label"], tf.int64)
        return imgRaw, imgLabel

    with tf.name_scope("input"):
        filename_que = tf.train.string_input_producer(
            string_tensor=[readFile],
            num_epochs=num_epochs
        )
        image, label = _read_and_decode(filename_queue=filename_que)
        images, spare_labels = tf.train.shuffle_batch(
            tensors=[image, label],
            batch_size=batch_size,
            num_threads=2,
            min_after_dequeue=1000
        )
        return images, spare_labels

if __name__ == "__main__":
    def _test_Writer():
        readDirPath = cifar10_train_dir
        labelPath = cifar10_label_path
        writeFilePath = cifar10_tfrecords_dir + "cifar10.train.tfrecords"
        CIFAR10_WTFRecord_SingleThread(readDirPath=readDirPath, labelPath=labelPath, writeFilePath=writeFilePath)

    def _test_Reader():
        with tf.Graph().as_default():
            readFile = "/home/guiyang/Downloads/cifar/tfrecords/cifar10.test.tfrecords"
            batch_size = 32
            num_epochs = 1
            images, labels = CIFAR10_RTFRecord_SingleThread(readFile=readFile, batch_size=batch_size, num_epochs=num_epochs)

            init_op = tf.group(
                tf.global_variables_initializer(),
                tf.local_variables_initializer()
            )
            with tf.Session(config=tf.ConfigProto(
                log_device_placement=True
            )) as sess:
                sess.run(init_op)
                coord = tf.train.Coordinator()
                threads = tf.train.start_queue_runners(
                    sess=sess,
                    coord=coord
                )
                try:
                    with not coord.should_stop():
                        start_time = time.time()
                        print(sess.run([images, labels]))
                        duration = time.time() - start_time
                except tf.errors.OutOfRangeError:
                    print("Done Fetch data sets")
                finally:
                    coord.request_stop()
                coord.join(threads=threads)