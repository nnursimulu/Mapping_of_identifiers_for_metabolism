DATABASE_FOLDER=Database
OUTSIDE_INFO=${DATABASE_FOLDER}/Outside_info
PARSED_INFO=${DATABASE_FOLDER}/Parsed_info

mkdir -p ${OUTSIDE_INFO}
mkdir -p ${PARSED_INFO}
#python3 scripts/0_fetch_metanetx_data.py --output-folder $OUTSIDE_INFO
python3 scripts/1_parse_out_identifier_map.py --metanetx-folder $OUTSIDE_INFO --parsed-info $PARSED_INFO