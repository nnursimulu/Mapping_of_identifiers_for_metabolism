# Author: Nirvana Nursimulu
# Code inspired by previous code for Architect (https://github.com/ParkinsonLab/Architect/)

from configparser import ConfigParser
import json
from argparse import ArgumentParser

def add_to_dict(key_value, key, value):

    if key not in key_value:
        key_value[key] = set()
    key_value[key].add(value)


def get_metanet_to_values(file_name):

    metanet_to_values = {}
    value_to_metanet = {}
    with open(file_name) as open_file:
        for line in open_file:
            line = line.strip()
            if (line == "") or (line[0] == "#"):
                continue
            split = line.split("\t")
            elem = split[0]
            metanet = split[1]
            if metanet == "EMPTY":
                continue
            if "secondary/obsolete/fantasy identifier" in line:
                continue
            add_to_dict(metanet_to_values, metanet, elem)
            add_to_dict(value_to_metanet, elem, metanet)
    open_file.close()
    return metanet_to_values, value_to_metanet


def write_out_rxn_info(output, value_to_metanet, metanet_to_values, prefix_to_name_identifiers_dot_org):

    with open(output, "w") as writer:
        for value, metanet_id in value_to_metanet.items():
            curr_prefix = value.split(":")[0]
            if curr_prefix not in prefix_to_name_identifiers_dot_org:
                continue
            curr_prefix_identifiers_dot_org = prefix_to_name_identifiers_dot_org[curr_prefix]
            metanet_id = list(metanet_id)[0] # Each value cannot have more than one ID associated with it.
            other_values = metanet_to_values[metanet_id]
            for other_value in other_values:
                if (other_value == value) or (other_value == (curr_prefix_identifiers_dot_org + ":" + value.split(":")[1])):
                    continue
                if "R:" in other_value: #Redundant information.
                    continue
                if ("bigg" in other_value) and (":R_" in other_value):
                    continue
                if other_value == metanet_id:
                    continue
                if other_value.startswith("mnx:"):
                    continue
                writer.write("\t".join([value, other_value]) + "\n")
            writer.write("\t".join([value, "metanetx.reaction:" + metanet_id]) + "\n")


def write_out_met_info(output, value_to_metanet, metanet_to_values, prefix_to_name_identifiers_dot_org):

    with open(output, "w") as writer:
        for value, metanet_id in value_to_metanet.items():
            values_encountered = set()
            curr_prefix = value.split(":")[0]
            if curr_prefix not in prefix_to_name_identifiers_dot_org:
                continue
            curr_prefix_identifiers_dot_org = prefix_to_name_identifiers_dot_org[curr_prefix]
            metanet_id = list(metanet_id)[0] # Each value cannot have more than one ID associated with it.
            other_values = metanet_to_values[metanet_id]
            for other_value in other_values:
                if (other_value == value) or (other_value == (curr_prefix_identifiers_dot_org + ":" + value.split(":")[1])):
                    continue
                if "M:" in other_value: #Redundant information.
                    continue
                if ("bigg" in other_value) and (":M_" in other_value):
                    continue
                if other_value == metanet_id:
                    continue
                if other_value.startswith("mnx:"):
                    continue
                if "chebi" in other_value: # Duplicate with CHEBI
                    other_value = "CHEBI:" + other_value.split(":")[1]
                    if other_value in values_encountered:
                        continue
                if other_value.split(":")[0] in ["keggC", "keggD", "keggG", "rheaG"]:
                    continue
                if other_value.split(":")[0] == "slm":
                    other_value = "SLM:" + other_value.split(":")[1]
                    if other_value in values_encountered:
                        continue
                writer.write("\t".join([value, other_value]) + "\n")
                values_encountered.add(other_value)
            writer.write("\t".join([value, "metanetx.chemical:" + metanet_id]) + "\n")


def write_out_metanet(metanet_id_to_values, output_file):

    with open(output_file, "w") as writer:
        for metanet_id, values in metanet_id_to_values.items():
            for value in values:
                writer.write(metanet_id + "\t" + value + "\n")


if __name__ == "__main__":

    parser = ArgumentParser(description="Parses out and writes out reaction and metabolite identifiers maps from MetaNetX.")
    parser.add_argument("--metanetx-folder", type=str, help="Folder that contains the downloaded MetaNetX info.")
    parser.add_argument("--parsed-info", type=str, help="Folder that will contain the parsed info from MetaNetX.")

    args = parser.parse_args()
    metanetx_folder = args.metanetx_folder
    parsed_info_folder = args.parsed_info

    # The output from 0_fetch_metanetx_data.py
    metanetx_rxn_output = metanetx_folder + "/reac_xref.tsv"
    metanetx_met_output = metanetx_folder + "/chem_xref.tsv"

    rxn_metanet_to_others_output = parsed_info_folder + "/INTERMEDIATE_metanet_rxn_mapping.out"
    met_metanet_to_others_output = parsed_info_folder + "/INTERMEDIATE_metanet_met_mapping.out"

    rxn_mapping_output = parsed_info_folder + "/PARSED_reaction_mapping.out"
    met_mapping_output = parsed_info_folder + "/PARSED_metabolite_mapping.out"

    # Some mappings required to smoothly get all the information out.
    rxn_prefix_to_name_identifiers_dot_org = \
        {"keggR": "kegg.reaction", \
            "biggR": "bigg.reaction", \
                "seedR": "seed.reaction"} 
    met_prefix_to_name_identifiers_dot_org = \
        {"keggC": "kegg.compound", \
            "keggG": "kegg.glycan", \
                "biggM": "bigg.metabolite", \
                    "seedM": "seed.compound"}

    # Get the metanet ID to other mappings.  Intermediate files generated for debugging.
    rxn_metanet_to_values, rxn_value_to_metanet = get_metanet_to_values(metanetx_rxn_output)
    met_metanet_to_values, met_value_to_metanet = get_metanet_to_values(metanetx_met_output)
    write_out_metanet(rxn_metanet_to_values, rxn_metanet_to_others_output)
    write_out_metanet(met_metanet_to_values, met_metanet_to_others_output)

    # Get the identifiers linked to others via metanet ID.
    write_out_rxn_info(rxn_mapping_output, rxn_value_to_metanet, rxn_metanet_to_values, \
        rxn_prefix_to_name_identifiers_dot_org)
    write_out_met_info(met_mapping_output, met_value_to_metanet, met_metanet_to_values, \
        met_prefix_to_name_identifiers_dot_org)