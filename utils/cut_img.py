import os
import cv2
import shutil
import pathlib

if __name__ == "__main__":
    ROOT_DIR = pathlib.Path(__file__).parent.parent.absolute()
    orig_dataset = os.path.join(ROOT_DIR, "runes_orig")
    dest_dataset = os.path.join(ROOT_DIR, "runes_cut")
    if os.path.isdir(dest_dataset):
        shutil.rmtree(dest_dataset)
        os.mkdir(dest_dataset)
    else:
        os.mkdir(dest_dataset)

    for img_file in os.listdir(orig_dataset):
        img_filename = os.path.basename(img_file)
        if img_filename.endswith(".jpg"):
            img = cv2.imread(os.path.join(orig_dataset, img_filename))
            img_h, img_w, img_c = img.shape

            w_mid = int(img_w / 3)
            target_img = img[0:int(img_h / 2), int(img_w / 3):int(img_w / 3 * 2)]

            cv2.imwrite(os.path.join(dest_dataset, img_filename), target_img)
