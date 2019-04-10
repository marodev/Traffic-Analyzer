from os import path

from main.helpers.combine_helper import CombineHelper
import main.helpers.file_helper as file_helper


def calculate_hex(hex_pair):
    hex_list = hex_pair.split(",")
    first_value = int(hex_list[0], 16) * pow(16, 2)
    second_value = int(hex_list[1], 16)
    return first_value + second_value


def combine_information(row):
    cipher_suite_number = calculate_hex(row["Value"])
    description = row["Description"]
    recommended = row["Recommended"]
    line = CombineHelper.combine_fields([cipher_suite_number, description, recommended])
    return line


def write_row(output_file, row):
    try:
        line = combine_information(row)
        file_helper.write_line(output_file, line)
    except ValueError:
        pass


def main():
    destination_file = path.join("..", "..", "files", "cipher_suites.csv")
    run(destination_file)


def run(destination_file):
    url = "https://www.iana.org/assignments/tls-parameters/tls-parameters-4.csv"
    filename = file_helper.download_file(url)

    with \
            open(filename, mode="r", encoding='utf-8') as csv_file, \
            open(destination_file, mode='w', encoding='utf-8') as output_file:
        header = "cipher_suite_number,description,recommended"
        file_helper.write_download_file(write_row, csv_file, output_file, header)

    file_helper.remove_file(filename)


if __name__ == "__main__":
    main()