import hashlib
import sys




def get_file_hash(path):
    with open(path, 'rb') as binFile:
        hash = hashlib.sha256(binFile.read())
        return hash.hexdigest()

def create_source_tree(current_path):

    tree = {}

    for entry in current_path.iterdir():
        if entry.is_file():
            hash = get_file_hash(entry)
            tree[entry.name] = hash
        elif entry.is_dir():
            tree[entry.name] = create_source_tree(current_path / entry.name)
        else:
            raise FileNotFoundError("An entry isn't marked as file nor directory.")

    return tree



def main():
    PATH_TO_SOURCE = sys.argv[0]
    PATH_TO_REPLICA = sys.argv[1]
    INTERVAL = int(sys.argv[2])
    AMOUNT_OF_SYNCS = int(sys.argv[3])
    PATH_TO_LOG_FILE = sys.argv[4]





if __name__ == "__main__":
    main()