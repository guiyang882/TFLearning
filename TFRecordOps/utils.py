import cv2
import tensorflow as tf
import os

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

def CIFAR10_RWTFRecord_SingleThread(readDirPath, labelPath, writeFilePath):
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

if __name__ == "__main__":
    readDirPath = cifar10_train_dir
    labelPath = cifar10_label_path
    writeFilePath = cifar10_tfrecords_dir + "cifar10.train.tfrecords"
    CIFAR10_RWTFRecord_SingleThread(readDirPath=readDirPath, labelPath=labelPath, writeFilePath=writeFilePath)
