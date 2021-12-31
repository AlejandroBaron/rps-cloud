source src/dockerscripts/populate_tables.sh
python3 ./src/utils/sql/init_stats_table.py
python3 app/main.py