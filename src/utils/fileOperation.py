import os


def file_list_in_folder(folder_path):
    """
    Get the list of files in the folder
    :param folder_path:
    :return: list of files in the folder
    """
    return os.listdir(folder_path)


def file_read(file_path):
    """
    Read the content of the file
    :param file_path:
    :return:
    """
    with open(file_path, 'r') as file:
        return file.readlines()
