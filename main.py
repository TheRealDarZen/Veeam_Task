import hashlib
import sys
from pathlib import Path
from time import sleep
import shutil

LOG_PATH = Path("/")

def get_file_hash(path):
    with open(path, 'rb') as binFile:
        hash = hashlib.sha256(binFile.read())
        return hash.hexdigest()


def create_tree(path):
    tree = {}

    for entry in path.iterdir():
        if entry.is_file():
            hash = get_file_hash(entry)
            tree[entry.name] = hash
        elif entry.is_dir():
            tree[entry.name] = create_tree(path / entry.name)
        else:
            raise FileNotFoundError("An entry isn't marked as file nor directory.")

    return tree


def delete_file_from_replica(path):
    global LOG_PATH
    with open(LOG_PATH, 'w') as log:
        log.write("Deleting " + str(path))

    if path.is_file():
        path.unlink()
    elif path.is_dir():
        path.rmdir()
    else:
        raise FileNotFoundError("An entry isn't marked as file nor directory.")


def copy_file_to_replica(path_to_file, path_to_destination):
    global LOG_PATH
    with open(LOG_PATH, 'w') as log:
        log.write("Copying file " + str(path_to_file) + " to " + str(path_to_destination))

    shutil.copy2(path_to_file, path_to_destination)


def copy_dir_to_replica(path_to_dir, path_to_destination):
    global LOG_PATH
    with open(LOG_PATH, 'w') as log:
        log.write("Copying directory " + str(path_to_dir) + " to " + str(path_to_destination))

    shutil.copytree(path_to_dir, path_to_destination)


def sync(source_path, replica_path, source_tree, replica_tree):

    # Check if any files are missing in replica or have been modified since the last synchronization
    for child in source_tree.keys():

        if type(source_tree[child]) is str: # type -> file
            if child in replica_tree.keys(): # file with the same name exists in replica folder
                if replica_tree[child] != source_tree[child]: # different file hash (different file contents)
                    delete_file_from_replica(replica_path / child)
                    copy_file_to_replica(source_path / child, replica_path / child)


            else: # file with the same name does not exist in replica folder
                copy_file_to_replica(source_path / child, replica_path / child)

        elif type(source_tree[child]) is dict: # type -> directory
            if child in replica_tree.keys(): # directory with the same name exists in replica folder
                sync(source_path / child, replica_path / child, source_tree[child], replica_tree[child])

            else: # directory with the same name does not exist in replica folder
                copy_dir_to_replica(source_path / child, replica_path / child)

        else: # shouldn't happen
            raise TypeError("Element is not a file nor a directory.")

    # Check if any files have been deleted since the last synchronization
    for child in replica_tree.keys():
        if child not in source_tree.keys():
            delete_file_from_replica(replica_path / child)


def main():
    PATH_TO_SOURCE = Path(sys.argv[0])
    PATH_TO_REPLICA = Path(sys.argv[1])
    INTERVAL = int(sys.argv[2])
    AMOUNT_OF_SYNCS = int(sys.argv[3])
    PATH_TO_LOG_FILE = Path(sys.argv[4])

    LOG_PATH = PATH_TO_LOG_FILE

    replica_tree = {}

    for _ in range(AMOUNT_OF_SYNCS):
        sleep(INTERVAL)
        source_tree = create_tree(PATH_TO_SOURCE / 'source')
        sync(PATH_TO_SOURCE, PATH_TO_REPLICA, source_tree, replica_tree)
        replica_tree = source_tree.copy()



if __name__ == "__main__":
    main()