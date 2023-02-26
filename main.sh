DATABASE_FOLDER=Database
OUTSIDE_INFO=${DATABASE_FOLDER}/Outside_info

mkdir -p ${OUTSIDE_INFO}
python3 scripts/0_fetch_metanetx_data.py --output-folder $OUTSIDE_INFO