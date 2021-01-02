import os
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    TARGET_NAME = "runes"
    pwd = os.path.abspath(os.path.dirname(__file__))
    dataset_dir = os.path.join(pwd, "final")

    file_list = []
    for file_name in os.listdir(dataset_dir):
        if file_name.endswith(".txt"):
            if os.path.isfile(os.path.join(dataset_dir, file_name.replace(".txt", ".jpg"))):
                file_list.append(file_name.replace(".txt", ".jpg"))
    # with open(os.path.join(data_dir, "train-" + TARGET_NAME + ".txt"), "w") as train_file:
    #     for train_name in file_list:
    #         train_file.write("data/" + TARGET_NAME + "/" + train_name + "\n")
    train_list, test_list = train_test_split(file_list, test_size=0.2)
    print(len(train_list))
    print(len(test_list))
    with open("train-" + TARGET_NAME + ".txt", "w") as train_file:
        for train_name in train_list:
            train_file.write("data/" + TARGET_NAME + "/" + train_name + "\n")
    with open("test-" + TARGET_NAME + ".txt", "w") as test_file:
        for test_name in test_list:
            test_file.write("data/" + TARGET_NAME + "/" + test_name + "\n")
