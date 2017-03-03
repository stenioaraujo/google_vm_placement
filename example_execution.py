from vm_placement.Worst_fit import WorstFit
from vm_placement.First_fit import FirstFit
from vm_placement.Best_fit import BestFit


def run_example_execution_for(algorithms):
    for alg in algorithms:
        print("==========================================")
        print("===============  %8s  ===============" % alg.__class__.__name__)
        print("==========================================")

        alg.start_allocation()
        print(alg)

        print("ALLOCATED")
        for i, bin_ in enumerate(alg.occupied_bins):
            print("Bin", i)
            print(bin_.capacity)
            print("VMs")
            cpu = 0  # To verify if it matches with the bin information
            mem = 0
            for vm in bin_.vms.values():
                print(vm)
                cpu += vm.cpu
                mem += vm.mem
            print("cpu: %s, mem: %s" % (cpu, mem))
            print("--------\n--------")

        print("REJECTED VMs")
        for vm in alg.rejected_vms:
            print(vm)


# 5 bins with 0.1 CPU and 0.1 MEM each
kwargs = {
    "number_bins": 5,
    "max_cpu": 0.5,
    "max_mem": 0.5,
    "csv_file": "task_events_200.csv"
}

worst_fit = WorstFit(**kwargs)
first_fit = FirstFit(**kwargs)
best_fit = BestFit(**kwargs)

run_example_execution_for([worst_fit, first_fit, best_fit])
