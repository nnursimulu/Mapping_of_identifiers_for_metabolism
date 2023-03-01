# Author: Nirvana Nursimulu

from argparse import ArgumentParser
import subprocess

if __name__ == '__main__':

    parser = ArgumentParser(description="Fetches up-to-date MetaNetX data.")
    parser.add_argument("--output-folder", type=str, help="Folder to contain the downloaded MetaNetX info.")

    args = parser.parse_args()
    output_folder = args.output_folder

    # Download the metanetX information as is.
    url_latest_rxn = "https://beta.metanetx.org/ftp/latest/reac_xref.tsv"
    url_latest_met = "https://beta.metanetx.org/ftp/latest/chem_xref.tsv"
    metanetx_rxn_output = output_folder + "/reac_xref.tsv"
    metanetx_met_output = output_folder + "/chem_xref.tsv"

    try:
        subprocess.call(["wget", url_latest_rxn, "-O", metanetx_rxn_output, "--no-check-certificate"])
    except Exception:
        print ("Error: could not download from https://beta.metanetx.org/ftp/latest/reac_xref.tsv for some reason.")

    try:
        subprocess.call(["wget", url_latest_met, "-O", metanetx_met_output, "--no-check-certificate"])
    except Exception:
        print ("Error: could not download from https://beta.metanetx.org/ftp/latest/chem_xref.tsv for some reason.")