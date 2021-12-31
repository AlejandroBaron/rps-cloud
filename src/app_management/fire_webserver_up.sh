echo "Populating transition matrices"
source src/dockerscripts/populate_tables.sh

echo "Initializing stats table"
python3 ./src/utils/sql/init_stats_table.py

echo "Initializing rounds table"
python3 ./src/utils/sql/init_rounds_table.py
python3 src/app/main.py