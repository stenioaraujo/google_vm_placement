from vm_placement.Worst_fit import WorstFit

wf = WorstFit(number_bins=5, max_cpu_bins=0.1, max_mem_bins=0.1,
              csv_file="task_events_200.csv")
wf.start_allocation()
print(wf)

print("ALLOCATED")
for i, bin_ in enumerate(wf.occupied_bins):
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
for vm in wf.reject_vms:
    print(vm)
