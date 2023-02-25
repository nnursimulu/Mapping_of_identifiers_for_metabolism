DATABASE_FOLDER=Database
OUTSIDE_INFO=Outside_info

mkdir -p ${DATABASE_FOLDER}/${OUTSIDE_INFO}
python3 scripts/0_fetch_metanetx_data.py --output-folder $OUTSIDE_INFO