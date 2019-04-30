import re

from os import path, remove

import main.helpers.file_helper as file_helper
from main.enricher import Enricher

from main.helpers.environment_helper import EnvironmentHelper
from main.helpers.combine_helper import CombineHelper
from main.helpers.print_helper import PrintHelper
from main.helpers.traffic_limit_helper import TrafficLimitHelper


def enrich_file(dirpath, file, enrichment_classes, new_file):
    with \
            open(path.join(dirpath, file), mode="r", encoding='utf-8') as capture, \
            open(path.join(dirpath, new_file), 'w', encoding='utf-8') as output_file:
        csv_reader = file_helper.get_csv_dict_reader(capture)

        loop_through_lines(csv_reader, enrichment_classes, output_file)


def loop_through_lines(csv_reader, enrichment_classes, output_file):
    for index, packet in enumerate(csv_reader):
        ip_enumerate_character = ","
        packet["ip.dst"] = packet["ip.dst"].split(ip_enumerate_character)[0]
        packet["ip.src"] = packet["ip.src"].split(ip_enumerate_character)[0]

        if file_helper.is_header(index):
            default_header = csv_reader.fieldnames
            enrichers = enrichment_classes.enrichers
            helper_headers = [enrichers[helper_key].header for helper_key in enrichers]
            line = CombineHelper.combine_fields(default_header + helper_headers, False)

            # Delete this line if debian has deployed wireshark v3.x In wireshark / tshark v2.x ssl is the search key
            # for encrypted traffic. ssl.* could be deprecated in future releases
            # https://tracker.debian.org/pkg/wireshark
            # https://www.wireshark.org/docs/relnotes/wireshark-3.0.0.html
            line = re.sub(r"ssl\.", r"tls.", line)

        else:
            joined_default_cells = CombineHelper.join_default_cells(packet, csv_reader.fieldnames)
            line = CombineHelper.combine_packet_information(joined_default_cells, enrichment_classes, packet)

        file_helper.write_line(output_file, line)


def main():
    environment_helper = EnvironmentHelper()
    run(environment_helper.get_environment())


def run(environment_variables, print_enrichers=False):
    csv_tmp_path = environment_variables["csv_tmp_path"]
    csv_capture_path = environment_variables["csv_capture_path"]
    pickle_dict_file_path = environment_variables["pickle_dict_file_path"]

    limiter = TrafficLimitHelper(3, 1)
    enrichment_classes = Enricher(limiter)
    stream_enricher = enrichment_classes.enrichers["stream_enricher"]

    if path.isfile(pickle_dict_file_path):
        stream_enricher.stream_ids = file_helper.read_dict_file(pickle_dict_file_path)

    for file_path in file_helper.get_file_paths(csv_tmp_path, file_helper.is_normal_csv_file):
        new_file = re.sub(".csv$", "-enriched.csv", str(file_path["filename"]))
        enrich_file(file_path["path"], file_path["filename"], enrichment_classes, new_file)
        remove(path.join(file_path["path"], file_path["filename"]))

    if print_enrichers:
        PrintHelper.print_enrichers(enrichment_classes.enrichers)

    for file_path in file_helper.get_file_paths(csv_tmp_path, file_helper.is_enriched_csv_file):
        file_helper.move_file(
            path.join(file_path["path"], file_path["filename"]),
            path.join(csv_capture_path, file_path["filename"])
        )

    file_helper.write_dict_file(pickle_dict_file_path, stream_enricher.stream_ids)
    if path.isfile(pickle_dict_file_path):
        stream_enricher.stream_ids = file_helper.read_dict_file(pickle_dict_file_path)


if __name__ == "__main__":
    main()
