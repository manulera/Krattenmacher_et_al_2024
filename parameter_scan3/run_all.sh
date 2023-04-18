for dir in "$@"
do
    bash run_scan.sh $dir
    bash run_analysis.sh $dir
done
