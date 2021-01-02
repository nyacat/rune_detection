import os
import shutil
import zipfile

if __name__ == "__main__":
    chunk_size = 300
    pwd = os.path.dirname(os.path.realpath(__file__))
    package_dir = os.path.join(pwd, "package")
    tmp_dir = os.path.join(pwd, "tmp")
    final_dir = os.path.join(pwd, "final")

    for zip_file in os.listdir(package_dir):
        with zipfile.ZipFile(os.path.join(package_dir, zip_file), "r") as zip_ref:
            zip_ref.extractall(tmp_dir)

    for dir_name in os.listdir(tmp_dir):
        dir_name = os.path.join(tmp_dir, dir_name)
        if os.path.isdir(dir_name):
            for file_name in os.listdir(dir_name):
                try:
                    shutil.move(os.path.join(dir_name, file_name), tmp_dir)
                except:
                    continue
            shutil.rmtree(dir_name)

    target_list = []
    for file in os.listdir(tmp_dir):
        if file.endswith(".txt"):
            if os.path.exists(os.path.join(tmp_dir, file.replace(".txt", ".jpg"))):
                target_list.append(file.replace(".txt", ""))

    if os.path.exists(final_dir):
        shutil.rmtree(final_dir)
    os.mkdir(final_dir)

    for file in target_list:
        with open(os.path.join(tmp_dir, file + ".txt"), "r") as ifile:
            data = ifile.readlines()
            if len(data) != 4:
                print(file)
                continue
        shutil.move(os.path.join(tmp_dir, file + ".jpg"), final_dir)
        shutil.move(os.path.join(tmp_dir, file + ".txt"), final_dir)

    # shutil.rmtree(tmp_dir)
