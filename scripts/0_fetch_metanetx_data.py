from argparse import ArgumentParser

if __name__ == '__main__':

    parser = ArgumentParser(description="Fetches up-to-date MetaNetX data.")
    parser.add_argument("--output-folder", type=str, help="Folder to contain the downloaded MetaNetX info.")

    args = parser.parse_args()
    output_folder = args.output_folder

    #TODO.