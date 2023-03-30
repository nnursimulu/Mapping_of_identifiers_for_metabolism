DATABASE_FOLDER=Database
OUTSIDE_INFO=${DATABASE_FOLDER}/Outside_info
PARSED_INFO=${DATABASE_FOLDER}/Parsed_info
PARSED_RXN_SPLIT_INFO=${DATABASE_FOLDER}/Parsed_split_rxn
PARSED_MET_SPLIT_INFO=${DATABASE_FOLDER}/Parsed_split_met

mkdir -p ${OUTSIDE_INFO}
mkdir -p ${PARSED_INFO}
mkdir -p ${PARSED_RXN_SPLIT_INFO}
mkdir -p ${PARSED_MET_SPLIT_INFO}
#python3 scripts/0_fetch_metanetx_data.py --output-folder $OUTSIDE_INFO
#python3 scripts/1_parse_out_identifier_map.py --metanetx-folder $OUTSIDE_INFO --parsed-info $PARSED_INFO
#python3 scripts/2_create_individual_db_map.py --parsed-info $PARSED_INFO --parsed-split-rxn-info $PARSED_RXN_SPLIT_INFO --parsed-split-met-info $PARSED_MET_SPLIT_INFO
python3 scripts/3_parse_out_rxn_definitions.py
#python3 scripts/4_determine_rxn_reversibility_equiv.py --parsed-info $PARSED_INFO