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


def sync(source_path, replica_path, source_tree, replica_tree, log_path):
    pass



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