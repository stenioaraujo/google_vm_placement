import sys

from vm_placement.Worst_fit import WorstFit
from vm_placement.First_fit import FirstFit
from vm_placement.Best_fit import BestFit


args = sys.argv[1].split(",")

if len(args) != 4:
    raise Exception("Expecting the parameters: algorithm[ff,bf,wf], "
                    "machine_cpu_size, machine_mem_size, type[normal/grande] "
                    "respectively. ALL TOGETHER separated by a comma (e.g ff,"
                    "1,1,normal)")

algorithms = {
    "bf": BestFit,
    "ff": FirstFit,
    "wf": WorstFit
}
data_source = {
    "normal": "experiment_data/task_events_100K_normal.csv",
    "grande": "experiment_data/task_events_100K_grande.csv"
}
MAXIMUM_CPU_SIZE = 7150
MAXIMUM_MEM_SIZE = 7150
bin_cpu_size = float(args[1])
bin_mem_size = float(args[2])

Algorithm = algorithms.get(args[0])

number_bins = int(MAXIMUM_CPU_SIZE/max(bin_cpu_size, bin_mem_size))


def run_experiment_for(algorithm):
    algorithm.start_allocation()

    to_string = algorithm.to_string_object()
    to_string["algorithm"] = args[0]

    print("%(algorithm)s,%(max_cpu)s,%(max_mem)s,%(max_cpu_per_bin)s,"
          "%(max_mem_per_bin)s,%(number_bins)s,%(number_occupied_bins)s,"
          "%(number_of_allocated_vms)s,%(number_of_rejected_vms)s,"
          "%(number_of_deleted_vms)s,%(fragmentation_cpu)s,"
          "%(fragmentation_mem)s" % to_string)

kwargs = {
    "number_bins": number_bins,
    "max_cpu": number_bins*bin_cpu_size,
    "max_mem": number_bins*bin_mem_size,
    "csv_file": data_source.get(args[3])
}

run_experiment_for(Algorithm(**kwargs))
