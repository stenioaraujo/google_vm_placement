#!/bin/bash

echo "algorithm,max_cpu,max_mem,max_cpu_per_bin,max_mem_per_bin,number_bins,\
number_occupied_bins,number_of_allocated_vms,number_of_rejected_vms,\
number_of_deleted_vms,fragmentation" > experiment_results.csv

cat experiment_inputs.txt | parallel -j+0 "python3 run_experiment.py {} >> \
                                            experiment_results.csv"