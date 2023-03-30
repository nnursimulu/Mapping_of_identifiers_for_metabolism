# Mapping of identifiers for metabolism

This set of scripts is meant to download and create mapping files for reaction and metabolite identifiers from one database to another.  Currently, the goal is to support KEGG, BiGG and ModelSEED identifiers.  The information is based in large part from the MetaNetX database.  This set of script was originally created for use by members of Dr Parkinson's lab. Suggestions for improvement are welcome.

## Dependencies:
The following are required to use these scripts:
* python3 installation.
* configparser module within python3.
* wget in shell.

## Usage:
1. Clone this repository.
2. Run main.sh.  This will create a Database folder.

### Note:
As scripts in this repository are being updated, certain scripts may not need to be re-run, for example, the one responsible for downloading MetaNetX.  I leave it up to the user's discretion to comment out relevant lines.