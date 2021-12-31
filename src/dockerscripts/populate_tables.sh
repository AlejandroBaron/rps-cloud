for depth in {1..5}
    do
        echo "Populating table $depth ..."
        python3 src/utils/sql/init_transition_matrix.py -d $depth
done