# Author: Nirvana Nursimulu

from argparse import ArgumentParser

def read_db_to_other_identifiers(filename):

    db_to_id1_to_id2 = {}
    with open(filename) as reader:
        for line in reader:
            line = line.strip()
            if line == "":
                continue
            db = line.split(":")[0]
            id1 = line.split()[0].split(":")[1]
            id2 = line.split()[1]
            if db not in db_to_id1_to_id2:
                db_to_id1_to_id2[db] = {}
            if id1 not in db_to_id1_to_id2[db]:
                db_to_id1_to_id2[db][id1] = set()
            db_to_id1_to_id2[db][id1].add(id2)
    return db_to_id1_to_id2


def write_map(id1_to_id2, output_file):

    with open(output_file, "w") as writer:
        for id1, id2_s in id1_to_id2.items():
            for id2 in id2_s:
                writer.write(id1 + "\t" + id2 + "\n")


if __name__ == '__main__':

    parser = ArgumentParser(description="Splits individual database identifiers mapping to separate files.")
    parser.add_argument("--parsed-info", type=str, help="Folder that contains the parsed info from MetaNetX.")
    parser.add_argument("--parsed-split-rxn-info", type=str, help="Folder that contains parsed reaction info" + \
        " that is also split per database.")
    parser.add_argument("--parsed-split-met-info", type=str, help="Folder that contains parsed metabolite info" + \
        " that is also split per database.")

    args = parser.parse_args()
    parsed_info_folder = args.parsed_info
    parsed_split_rxn_folder = args.parsed_split_rxn_info
    parsed_split_met_folder = args.parsed_split_met_info

    rxn_mapping_file = parsed_info_folder + "/PARSED_reaction_mapping.out"
    met_mapping_file = parsed_info_folder + "/PARSED_metabolite_mapping.out"

    rxn_db_to_id1_to_id2 = read_db_to_other_identifiers(rxn_mapping_file)
    met_db_to_id1_to_id2 = read_db_to_other_identifiers(met_mapping_file)
    for rxn_db, id1_to_id2 in rxn_db_to_id1_to_id2.items():
        output_file = parsed_split_rxn_folder + "/MAP_" + rxn_db + ".out"
        write_map(id1_to_id2, output_file)
    for met_db, id1_to_id2 in met_db_to_id1_to_id2.items():
        output_file = parsed_split_met_folder + "/MAP_" + met_db + ".out"
        write_map(id1_to_id2, output_file)