# Author: Nirvana Nursimulu

from argparse import ArgumentParser
import utils

if __name__ == '__main__':

    parser = ArgumentParser(description="Splits individual database identifiers mapping to separate files.")
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

    rxn_db_to_id1_to_id2 = utils.read_db_to_other_identifiers(rxn_mapping_file)
    met_db_to_id1_to_id2 = utils.read_db_to_other_identifiers(met_mapping_file)

    #TODO