import hashlib
import sys
from pathlib import Path
from time import sleep


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
    pass


def copy_file_to_replica(path_to_file, path_to_destination):
    pass


def copy_dir_to_replica(path_to_dir, path_to_destination):
    pass

# TODO: Logging
def sync(source_path, replica_path, source_tree, replica_tree, log_path):

    # Check if any files are missing in replica or have been modified since the last synchronization
    for child in source_tree.keys():

        if type(source_tree[child]) is str: # type -> file
            if child in replica_tree.keys(): # file with the same name exists in replica folder
                if replica_tree[child] != source_tree[child]: # different file hash (different file contents)
                    delete_file_from_replica(replica_path / child)
                    copy_file_to_replica(source_path / child, replica_path)

            else: # file with the same name does not exist in replica folder
                copy_file_to_replica(source_path / child, replica_path)

        elif type(source_tree[child]) is dict: # type -> directory
            if child in replica_tree.keys(): # directory with the same name exists in replica folder
                sync(source_path / child, replica_path / child, source_tree[child], replica_tree[child], log_path)

            else: # directory with the same name does not exist in replica folder
                copy_dir_to_replica(source_path / child, replica_path)

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

    replica_tree = {}

    for _ in range(AMOUNT_OF_SYNCS):
        sleep(INTERVAL)
        source_tree = create_tree(PATH_TO_SOURCE / 'source')
        sync(PATH_TO_SOURCE, PATH_TO_REPLICA, source_tree, replica_tree, PATH_TO_LOG_FILE)
        replica_tree = source_tree.copy()



if __name__ == "__main__":
    main()