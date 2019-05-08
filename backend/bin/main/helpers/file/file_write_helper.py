import pickle


def write_line(output_file, line):
    output_file.write(line + "\n")


def write_dict_file(file, dictionary):
    with open(file, "wb") as dict_file:
        pickle.dump(dictionary, dict_file, )
