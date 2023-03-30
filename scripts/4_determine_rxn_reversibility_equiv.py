# Author: Nirvana Nursimulu

from argparse import ArgumentParser
import utils

if __name__ == '__main__':

    parser = ArgumentParser(description="Determines reaction reversibility equivalencies.")
    parser.add_argument("--parsed-info", type=str, help="Folder that contains the parsed info from MetaNetX.")

    args = parser.parse_args()
    parsed_info_folder = args.parsed_info

    rxn_mapping_file = parsed_info_folder + "/PARSED_reaction_mapping.out"
    met_mapping_file = parsed_info_folder + "/PARSED_metabolite_mapping.out"

    # 0a. Parse mapping of reaction and metabolite from one database to another.
    rxn_db_to_id1_to_id2 = utils.read_db_to_other_identifiers(rxn_mapping_file)
    met_db_to_id1_to_id2 = utils.read_db_to_other_identifiers(met_mapping_file)

    # 0b. Get mapping of what kind of database reaction identifiers map to metabolite identifiers.
    db_type_rxn_to_met = utils.read_default_db_type_rxn_to_met()
    
    # 1. Load reaction definitions.
    # TODO: Need to parse out reaction definitions.

    # 2. Find reaction equivalencies.
    # TODO.