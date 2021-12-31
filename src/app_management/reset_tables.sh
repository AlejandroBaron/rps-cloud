for depth in {1..5}
    do
        echo "Dropping table for depth $depth"
        python3 src/utils/sql/drop_transition_matrix.py -d $depth
        echo "Initializing table for depth $depth"
        python3 src/utils/sql/init_transition_matrix.py -d $depth
done