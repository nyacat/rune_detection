import os
import cv2
import json
import base64
import shutil
import numpy as np
import codecs
from sklearn.model_selection import train_test_split


def convert_box(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert(json_path, saved_images_path, saved_labels_path):
    for filename in os.listdir(json_path):
        if filename.endswith("json"):
            file_prefix = filename.replace(".json", "")

            # open the label file
            _label_file = open(os.path.join(saved_labels_path, file_prefix + ".txt"), "w")

            # load json file
            with open(os.path.join(json_path, filename), "r") as json_file:
                json_data = json.load(json_file)

            # load image
            image = cv2.imdecode(np.frombuffer(base64.b64decode(json_data["imageData"]), np.uint8), -1)
            height, width, channels = image.shape

            # save image
            cv2.imwrite(os.path.join(saved_images_path, file_prefix + ".jpg"), image)

            for shape in json_data["shapes"]:
                points = np.array(shape["points"])
                xmin = min(points[:, 0])
                xmax = max(points[:, 0])
                ymin = min(points[:, 1])
                ymax = max(points[:, 1])
                label = shape["label"]
                if label not in classes:
                    continue
                if xmax <= xmin or ymax <= ymin:
                    pass
                else:
                    box = (float(xmin), float(xmax), float(ymin), float(ymax))
                    bb = convert_box((width, height), box)
                    cls_id = classes.index(label)
                    _label_file.write("{} {}\n".format(str(cls_id), " ".join([str(a) for a in bb])))
            _label_file.close()


def split_set(root_path, root_labels_path):
    # just work code :P
    dir_structure = "../dataset-bbs/images/"
    total_files = [dir_structure + _label_file.replace(".txt", ".jpg") for _label_file in os.listdir(root_labels_path)]
    train_files, val_files = train_test_split(total_files, train_size=0.8, test_size=0.2)

    with open(os.path.join(root_path, dataset_name + "_trainval.txt"), "w") as train_file:
        train_file.write("\n".join(total_files))
    with open(os.path.join(root_path, dataset_name + "_train.txt"), "w") as train_file:
        train_file.write("\n".join(train_files))
    with open(os.path.join(root_path, dataset_name + "_val.txt"), "w") as train_file:
        train_file.write("\n".join(val_files))


if __name__ == "__main__":
    dataset_name = "gms"
    labelme_json_path = os.path.join(os.path.abspath(".."), "images")

    darknet_path = os.path.join(os.path.abspath(".."), "dataset-bbs")
    darknet_images_path = os.path.join(darknet_path, "images")
    darknet_labels_path = os.path.join(darknet_path, "labels")

    if os.path.exists(darknet_path):
        shutil.rmtree(darknet_path)
    os.mkdir(darknet_path)
    os.mkdir(darknet_images_path)
    os.mkdir(darknet_labels_path)
    classes = ["colabear", "jester_scarlion"]

    convert(labelme_json_path, darknet_images_path, darknet_labels_path)
    split_set(darknet_path, darknet_labels_path)

    with open(os.path.join(darknet_path, dataset_name + ".names"), "w") as name_file:
        name_file.write("\n".join(classes))

    with open(os.path.join(darknet_path, dataset_name + ".data"), "w") as data_file:
        # I know it sucks, just work
        raw_str = "classes={}\n".format(len(classes))
        raw_str += "train=./dataset-bbs/{}_trainval.txt\n".format(dataset_name)
        raw_str += "valid=./dataset-bbs/{}_val.txt\n".format(dataset_name)
        raw_str += "names=./dataset-bbs/{}.names\n".format(dataset_name)
        raw_str += "backup=backup/\n"
        raw_str += "eval=coco"
        data_file.write(raw_str)
