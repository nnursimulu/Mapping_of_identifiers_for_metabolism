# Author: Nirvana Nursimulu

from argparse import ArgumentParser
import utils, subprocess

def parse_out_bigg_rxn(bigg_initial_download, bigg_output_parsed):

    with open(bigg_initial_download) as reader:
        with open(bigg_output_parsed, "w") as writer:
            for line in reader:
                if line.strip() == "":
                    continue
                split = line.split("\t")
                bigg_id = split[0]
                rxn_formula = split[2]
                writer.write(bigg_id + "\t" + rxn_formula + "\n")


if __name__ == '__main__':

    parser = ArgumentParser(description="Parse out reaction definitions for KEGG and BiGG.")
    parser.add_argument("--output-folder", type=str, help="Folder to contain downloaded info from BiGG.")
    parser.add_argument("--parsed-info", type=str, help="Folder that contains the parsed info from KEGG and BiGG.")

    args = parser.parse_args()
    output_folder = args.output_folder
    parsed_info = args.parsed_info

    kegg_output_file = parsed_info + "/KEGG_rxn_equations.out"
    #TODO: download parsed out KEGG reaction equations from the website.

    # For BiGG, first download the file with the information.
    bigg_initial_download = output_folder + "/bigg_models_reactions.txt"
    bigg_output_parsed = parsed_info + "/PARSED_BiGG_rxn_formula.out"
    url_bigg = "http://bigg.ucsd.edu/static/namespace/bigg_models_reactions.txt"
    try:
        subprocess.call(["wget", url_bigg, "-O", bigg_initial_download])
    except Exception:
        print ("Error: could not download from http://bigg.ucsd.edu/static/namespace/bigg_models_reactions.txt for some reason.")
    
    # For BiGG, parse out the reaction definition for each reaction.
    parse_out_bigg_rxn(bigg_initial_download, bigg_output_parsed)