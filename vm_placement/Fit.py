"""This is the bone base for the fitting classes Worst Fit, Best Fit and
First fit Algorithms for Virtual Machine Placement. The algorithm is adapted
to support the attributes CPU and Memory as weights for the instances.
"""
from abc import ABCMeta, abstractmethod

from vm_placement import utils


class Fit:
    __metaclass__ = ABCMeta

    def __init__(self, number_bins, max_cpu, max_mem, csv_file):
        """Apply the WorstFit Algorithm in the CSV file

        :param number_bins: number of bins that will be used
        :param max_cpu: max cpu capacity of all the bins together.
        :param max_mem: max memory capacity of all the bins together.
        :param csv_file: the path for the csv file
        """
        self.max_cpu = max_cpu
        self.max_mem = max_mem
        self.number_bins = number_bins
        self.max_cpu_per_bin = max_cpu/number_bins
        self.max_mem_per_bin = max_mem/number_bins
        self.bins = utils.create_bins(number_bins=number_bins,
                                      max_cpu_bins=self.max_cpu_per_bin,
                                      max_mem_bins=self.max_mem_per_bin)
        self.occupied_bins = []
        self.vm_bins = {}
        self.rejected_vms = []
        self.csv_file = csv_file
        self.vms_end_times = {}

    def start_allocation(self):
        with open(self.csv_file, "r") as csv:
            head_keys = utils.keys_from_csv_head(csv.readline())

            for vm_uuid, line in enumerate(csv):
                vm = utils.vm_from_csv_line(head_keys, line, vm_uuid)
                actual_time = vm.start_time
                self.vms_end_times.get(vm.end_time, []).append(vm)

                if vm.cpu > self.max_cpu_per_bin \
                        or vm.mem > self.max_mem_per_bin:
                    self._reject(vm)
                else:
                    self._try_to_allocate_vm(vm)

                vms_to_remove = self.vms_end_times.get(actual_time, [])
                if vms_to_remove:
                    self._remove_vms(vms_to_remove)
                    del self.vms_end_times[actual_time]

    def _reject(self, vm):
        self.rejected_vms.append(vm)

    @abstractmethod
    def _try_to_allocate_vm(self, vm):
        pass

    @abstractmethod
    def _remove_vms(self, vms_to_remove):
        pass

    def __str__(self):
        output = {
            "max_cpu": self.max_cpu,
            "max_mem": self.max_mem,
            "max_cpu_per_bin": self.max_cpu_per_bin,
            "max_mem_per_bin": self.max_mem_per_bin,
            "number_bins": self.number_bins,
            "number_occupied_bins": len(self.occupied_bins),
            "number_of_allocated_vms": len(self.vm_bins),
            "number_of_rejected_vms": len(self.rejected_vms)
        }
        return str(output)
