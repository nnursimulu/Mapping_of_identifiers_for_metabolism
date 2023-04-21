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

To get a detailed breakdown of what each script does, consult the README in the Scripts directory.

## Expected output:
Once commands in ``main.sh`` have been run, a Database folder will be created in this directory.  Expect the following sub-folders:
1. ``Outside_info``
2. ``Parsed_info``
3. ``Parsed_split_met``
4. ``Parsed_split_rxn``

Below is a detailed breakdown of what each file in each subdirectory contains.

### Detailed breakdown of output

``Outside_info`` contains various databases downloaded.  Within this folder:
* ``chem_xref.tsv`` and ``reac_xref.tsv`` are downloaded from MetaNetX and contain information pertinent to compounds and reactions respectively.
* ``seed_model_reactions.tsv`` is downloaded from the ModelSEED GitHub.
* ``bigg_models_reactions.txt`` is downloaded from the BiGG database available online.

``Parsed_info`` contains parsed information from Outside_info for easy programmatic access by scripts in this repository.
* Reaction equations are parsed out (or downloaded in the case of KEGG) are written out to files of the format ``PARSED_*_rxn_formula.out``.
* The ``INTERMEDIATE_*`` files are purely used by scripts in this repository, and get associations from MetaNetX IDs (used as reference) to other database identifiers.
* ``PARSED_metabolite_mapping.out`` and ``PARSED_reaction_mapping.out``contain mappings from one identifier to another, made via MetaNetX identifiers.  **These are not meant to be the final output of the scripts but can be used at the discretion of users.**

``Parsed_split_met`` contains mapping files for metabolite identifiers from one database to another.
* ``MAP_biggM.out``, ``MAP_keggC.out``, ``MAP_keggG.out`` and ``MAP_seedM.out`` have mappings from BiGG, the KEGG compound, the KEGG Glycan and the modelSEED databases respectively.  **These are meant to be output for users.**

``Parsed_split_rxn`` contains for reaction identifiers from one database to another, as well as equivalencies between reaction equation.
* ``MAP_biggR.out``, ``MAP_keggR.out`` and ``MAP_seedR.out`` have mappings from BiGG, KEGG and the modelSEED databases respectively. **These are meant to be output for users.**
* As well, you have equivalencies between reaction equation from one database to another in ``COMPUTED_bigg_seed_equiv.out``, ``COMPUTED_kegg_bigg_equiv.out`` and ``COMPUTED_kegg_seed_equiv.out``.  These files tell you whether the equation in one database, when written using another database's metabolite identifiers, proceeds in the same direction in this other database.  **These are meant to be output for users.**

### Interpretation of computed reaction direction equivalences
Assume metabolites A, B, C and D are called ``A_1``, ``B_1``, ``C_1`` and ``D_1`` in one database (database 1), and ``A_2``, ``B_2``, ``C_2`` and ``D_2`` in another (database 2).  Suppose database 1 has a reaction of the form ``A_1 + B_1 -> C_1 + D_1``.  This reaction is deemed by MetaNetX to have an equivalent reaction in database 2.  However, how can we tell that the reactions in the databases proceed in the same direction?  Here are possibly scenarios considered by the scripts in this directory, in particular, the forms that the equivalent reaction in database 2 may adopt.  **Note that neither stoichiometric nor compartment information are considered.**

1. ``A_2 + B_2 -> C_2 + D_2``: Reaction is considered to be equivalent and to operate in the same direction.
2. ``C_2 + D_2 -> A_2 + B_2``: Reaction is considered to be equivalent and to operate in the reverse direction.
3. ``A_2 -> C_2 + D_2``: Reaction is considered to be likely equivalent and to operate in the same direction.  Same can be said for ``A_2 + B_2 -> C_2``.
4. ``C_2 + D_2 -> A_2``: Reaction are considered to be likely equivalent and to operate in the reverse direction. Same can be said for ``C_2 -> A_2 + B_2``.
5. ``A_2 + B_2 + E_2 -> C_2``: Some kind of conflicting information is found (as the reaction in database 1 is not strictly a subset of this reaction, or vice-versa). This needs to be resolved by the user.

In some cases, a reaction equation may be absent, perhaps due to discrepancies in external database update.  These will be reported to be as such to be further resolved by users.

## Caution
1. As scripts in this repository are being updated, certain scripts may not need to be re-run, for example, the one responsible for downloading MetaNetX.  I leave it up to the user's discretion to comment out relevant lines.
2. When comparing reaction formulae from one database to another, the actual stoichiometries of metabolite participants are not considered.  Similarly, compartment information is not taken into consideration--this is particularly relevant for modelSEED and BiGG reactions which contain compartment information. 