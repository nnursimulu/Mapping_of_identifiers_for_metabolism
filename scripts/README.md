###Detailed breakdown of scripts

``0_fetch_metanetx_data.py``: downloads raw information from MetaNetX, BiGG and SEED and saves to ``repo/Database/Outside_info``.

``1_parse_out_identifier_map.py``: parses out information downloaded from MetaNetX so that it can be more easily read.  The information is written out to ``repo/Database/Parsed_info`` as ``PARSED_metabolite_mapping.out`` and ``PARSED_reaction_mapping.out``.  These link identifiers from one database to another using metanetx.  Intermediate files only containing metanetx identifiers to other database identifiers are written out in ``INTERMEDIATE_metanet_rxn_mapping.out`` and ``INTERMEDIATE_metanet_met_mapping.out``; these files are meant to be used for debugging.

``2_create_individual_db_map.py``: parses information from ``PARSED_metabolite_mapping.out`` and ``PARSED_reaction_mapping.out`` to get the mapping, per database, for identifier to other identifiers whether in this database or elsewhere.  Writes out to ``Parsed_split_met`` and ``Parsed_split_rxn``.

``3_parse_out_rxn_definitions.py``: downloads or parses out reaction equations.  Written to ``Parsed_info``.

``4_determine_rxn_reversibility_equiv.py``: compares and writes whether reaction equations in one database proceed in the same direction in another database, if the metabolite identifiers are translated from one database to another. **Caution: does not consider stoichiometry or compartment information.**