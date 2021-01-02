import os
import shutil
import zipfile

if __name__ == "__main__":
    chunk_size = 300
    input_dir = "C:\\Users\\R_Tra\\Desktop\\runes_server\\upload_out"
    package_dir = "C:\\Users\\R_Tra\\Desktop\\runes_server\\package"

    file_list = []
    for img_file in os.listdir(input_dir):
        full_path = os.path.join(input_dir, img_file)

        if full_path.endswith(".jpg"):
            file_list.append(full_path)

    file_list = [file_list[x:x+chunk_size] for x in range(0, len(file_list), chunk_size)]

    for chunk in file_list:
        chunk_index = file_list.index(chunk)
        zipFile = zipfile.ZipFile(os.path.join(package_dir, "{}.zip".format(chunk_index)), 'w')
        for file in chunk:
            filename = os.path.basename(file)
            zipFile.write(file, filename, zipfile.ZIP_DEFLATED)
            zipFile.write(file.replace(".jpg", ".txt"), filename.replace(".jpg", ".txt"), zipfile.ZIP_DEFLATED)
        zipFile.write("D:\\Projects\\PycharmProjects\\gms_runes\\runes_cut\\classes.txt", "classes.txt", zipfile.ZIP_DEFLATED)
        zipFile.close()
