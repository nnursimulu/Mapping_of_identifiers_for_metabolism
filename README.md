# Mapping of identifiers for metabolism

Author: Nirvana Nursimulu

This set of scripts is meant to download and create mapping files for reaction and metabolite identifiers from one database to another.  Currently, the goal is to support KEGG, BiGG and ModelSEED identifiers.  The information is based in large part from the MetaNetX database.  This set of script was originally created for use by members of Dr Parkinson's lab. Suggestions for improvement are welcome.

## Dependencies:
The following are required to use these scripts:
* a stable internet connection
* python3 installation.
* configparser module within python3.
* wget in shell.

## Usage:
1. Clone this repository.
2. Run ``sh main.sh``.  This will create a Database folder and run python scripts in the Scripts folder.

## Expected output:
Once instructions in ``main.sh`` have been run, a Database folder will be created in this directory.  Expect the following sub-folders:
1. ``Outside_info``: contains various databases downloaded
2. ``Parsed_info``: parsed information from Outside_info for easy programmatic access
3. ``Parsed_split_met``: mapping files for metabolite identifiers from one database to another.
4. ``Parsed_split_rxn``: mapping files for reaction identifiers from one database to another, as well as equivalencies between reaction equation.

Here is a detailed breakdown of what each file in each subdirectory contains.

### Detailed breakdown

## Caution:
1. As scripts in this repository are being updated, certain scripts may not need to be re-run, for example, the one responsible for downloading MetaNetX.  I leave it up to the user's discretion to comment out relevant lines.
2. When comparing reaction formulae from one database to another, the actual stoichiometries of metabolite participants are not considered.  Similarly, compartment information is not taken into consideration--this is particularly relevant for modelSEED and BiGG reactions which contain compartment information. 
