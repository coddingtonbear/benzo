import pickle


def read_session(path):
    with open(path, 'r') as inf:
        return pickle.load(inf)


def write_session(path, data):
    with open(path, 'w') as out:
        pickle.dump(data, out)
