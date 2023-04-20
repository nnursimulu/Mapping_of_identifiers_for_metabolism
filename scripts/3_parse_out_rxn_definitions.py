# Author: Nirvana Nursimulu
# Some of this code is inspired by what I have previously written for Architect at:
# https://github.com/ParkinsonLab/Architect/blob/master/scripts/model_reconstruction/x_set_up_kegg_db.py

from argparse import ArgumentParser
import utils, subprocess, urllib.request

def parse_out_bigg_rxn(bigg_initial_download, bigg_output_parsed):

    with open(bigg_initial_download) as reader:
        with open(bigg_output_parsed, "w") as writer:
            for line in reader:
                if line.strip() == "":
                    continue
                split = line.split("\t")
                bigg_id = split[0]
                if bigg_id == "bigg_id":
                    continue
                rxn_formula = split[2]
                writer.write(bigg_id + "\t" + rxn_formula + "\n")


def read_parsed_kegg_rxns(file_name):

    list_of_kegg_rxns = set()
    with open(file_name) as reader:
        for line in reader:
            line = line.strip()
            if line == "":
                continue
            rxn_id = line.split()[0]
            rxn_id = rxn_id.split("#")[0]
            list_of_kegg_rxns.add(rxn_id)
    return list_of_kegg_rxns


def get_actual_url(prefix, elems):

    return prefix + "+".join(elems)


def get_info_about_elem(actual_url, header, elem_to_info):

    open_file = urllib.request.urlopen(actual_url)
    for line in open_file:
        # line = line.decode('utf-8')
        line = line.decode()
        if line.strip() == "":
            continue
        if line.strip() == "///":
            curr_title = ""
            continue
        if line[0] != " ":
            curr_title = line.split()[0]
            if curr_title == "ENTRY":
                curr_entry = line.split()[1]
                elem_to_info[curr_entry] = get_dict_from_header(header)
        if curr_title != "ENTRY":
            if curr_title not in header:
                continue
            curr_string = line[12:].strip()
            elem_to_info[curr_entry][curr_title].append(curr_string)
    open_file.close()


def get_dict_from_header(liste):

    d = {}
    for elem in liste:
        d[elem] = []
    return d


def parse_out_kegg_info_from_website(elems_of_int, headers_of_int):

    elems_of_int = sorted(list(elems_of_int))
    unable_to_parse = set()
    all_missing_elem = set()
    elem_to_info = {}
    prefix = "http://rest.kegg.jp/get/"
    i = 0
    while i < len(elems_of_int):
        
        actual_url = get_actual_url(prefix, elems_of_int[i:i + 10])
        try:
            get_info_about_elem(actual_url, headers_of_int, elem_to_info)
        except Exception as e:

            for elem in elems_of_int[i:i+10]:
                unable_to_parse.add(elem)
        i += 10
        #print (i)
    for elem in elems_of_int:
        if elem not in elem_to_info:
            all_missing_elem.add(elem)
    return elem_to_info, all_missing_elem, unable_to_parse


def format_to_get_only_kegg_rxn_eqn(kegg_reactions_to_info):

    kegg_reactions_to_equation = {}
    for rxn, info in kegg_reactions_to_info.items():
        # Possibility to retain more information from KEGG in the future if required.
        # info_formatted = {}
        # info_formatted["NAME"] = "#".join(info["NAME"])
        # info_formatted["PATHWAY"] = "#".join(info["PATHWAY"])
        # info_formatted["ENZYME"] = get_ecs_from_kegg_download(info["ENZYME"])
        # info_formatted["EQUATION"] = info["EQUATION"][0]

        kegg_reactions_to_equation[rxn] = info["EQUATION"][0]
    return kegg_reactions_to_equation


def write_out_kegg_information(kegg_output_file, kegg_rxn_to_eqn, missing_kegg_reactions, unable_to_parse_kegg_reactions):

    with open(kegg_output_file, "w") as writer:
        # First write the information we could not get.
        writer.write("# Commented lines concern any KEGG reactions that we could not parse.\n")
        for rxn in missing_kegg_reactions:
            if rxn in unable_to_parse_kegg_reactions:
                writer.write("\t".join(["# ", rxn, "URL_not_resolved"]) + "\n")
            else:
                writer.write("\t".join(["# ", rxn, "Did_not_find"]) + "\n")
        for rxn, eqn in kegg_rxn_to_eqn.items():
            writer.write(rxn + "\t" + eqn + "\n")


def parse_out_seed_rxn(seed_initial_download, seed_output_parsed):

    with open(seed_initial_download) as reader:
        with open(seed_output_parsed, "w") as writer:
            writer.write("# The third column gives the reaction directionality according to SEED" + \
            "--computed via Gibbs free energy.\n")
            writer.write("# >: forward, <: reverse, =: reversible, ?: undefined\n\n")

            for i, line in enumerate(reader):
                line = line.strip()
                if (i == 0) or (line == ""):
                    continue
                split = line.split("\t")
                rxn_id, equation, reversibility = split[0], split[6], split[8]
                equation = equation.replace("(", " ")
                equation = equation.replace(")", " ")
                info = [rxn_id, equation, reversibility]
                writer.write("\t".join(info) + "\n")


if __name__ == '__main__':

    parser = ArgumentParser(description="Parse out reaction definitions for KEGG and BiGG.")
    parser.add_argument("--output-folder", type=str, help="Folder to contain downloaded info from BiGG.")
    parser.add_argument("--parsed-info", type=str, help="Folder that contains the parsed info from KEGG and BiGG.")
    parser.add_argument("--parsed-split-rxn-info", type=str, help="Folder that contains parsed reaction info" + \
        " that is also split per database.")

    args = parser.parse_args()
    output_folder = args.output_folder
    parsed_info = args.parsed_info
    parsed_split_rxn_info = args.parsed_split_rxn_info

    # Download parsed out KEGG reaction equations from KEGG.
    kegg_output_file = parsed_info + "/PARSED_KEGG_rxn_formula.out"
    list_of_kegg_rxns = read_parsed_kegg_rxns(parsed_split_rxn_info + "/MAP_keggR.out")
    kegg_rxn_headers_of_int = ["EQUATION"] # Can be altered in the future if need more information from KEGG.
    kegg_reactions_to_downloaded_info, missing_kegg_reactions, unable_to_parse_kegg_reactions  = \
        parse_out_kegg_info_from_website(list_of_kegg_rxns, kegg_rxn_headers_of_int)
    kegg_rxn_to_eqn = format_to_get_only_kegg_rxn_eqn(kegg_reactions_to_downloaded_info)
    write_out_kegg_information(kegg_output_file, kegg_rxn_to_eqn, missing_kegg_reactions, unable_to_parse_kegg_reactions)


    # For BiGG, first download the file with the information.
    bigg_initial_download = output_folder + "/bigg_models_reactions.txt"
    bigg_output_parsed = parsed_info + "/PARSED_BiGG_rxn_formula.out"
    url_bigg = "http://bigg.ucsd.edu/static/namespace/bigg_models_reactions.txt"
    try:
        subprocess.call(["wget", url_bigg, "-O", bigg_initial_download])
    except Exception:
        print ("Error: could not download from " + url_bigg + " for some reason.")
    # Then, parse out the reaction definition for each reaction.
    parse_out_bigg_rxn(bigg_initial_download, bigg_output_parsed)


    # For SEED, first download the file with the information.
    seed_initial_download = output_folder + "/seed_models_reactions.tsv"
    seed_output_parsed = parsed_info + "/PARSED_SEED_rxn_formula.out"
    url_seed = "https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/master/Biochemistry/reactions.tsv"
    try:
        subprocess.call(["wget", url_seed, "-O", seed_initial_download])
    except Exception:
        print ("Error: could not download from " + url_seed + " for some reason.")
    parse_out_seed_rxn(seed_initial_download, seed_output_parsed)