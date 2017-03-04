"""This is the bone base for the fitting classes Worst Fit, Best Fit and
First fit Algorithms for Virtual Machine Placement. The algorithm is adapted
to support the attributes CPU and Memory as weights for the instances.
"""
from abc import ABCMeta, abstractmethod
import heapq

from vm_placement import utils


class Fit:
    __metaclass__ = ABCMeta

    def __init__(self, number_bins, max_cpu, max_mem, csv_file):
        """Apply the Fit Algorithm in the CSV file

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
        self.number_successful_allocated_vms = 0
        self.rejected_vms = []
        self.csv_file = csv_file
        self.vms_end_times = {}
        self.end_times = []

    def start_allocation(self):
        with open(self.csv_file, "r") as csv:
            head_keys = utils.keys_from_csv_head(csv.readline())

            for vm_uuid, line in enumerate(csv):
                vm = utils.vm_from_csv_line(head_keys, line, vm_uuid)
                self.vms_end_times.setdefault(vm.end_time, []).append(vm)
                heapq.heappush(self.end_times, vm.end_time)

                self._handle_end_time(start_time=vm.start_time)

                if vm.cpu > self.max_cpu_per_bin \
                        or vm.mem > self.max_mem_per_bin:
                    self._reject(vm)
                else:
                    if self._try_to_allocate_vm(vm):
                        self.number_successful_allocated_vms += 1

    def fragmentation(self):
        """Calculate the fragmentation separately for CPU and MEM

        The formula used is:
        (free - freemax)
        ----------------    (or 0.0 for free=0)
            free

        Where:
        free     = total number free resources for CPU and MEM separately
        freemax  = Largest Free Resources for ONE Bin

        The greater the worst.

        :return: A dictionary with the total fragmentation x, with 0 <= x <= 1
        """
        free = {"cpu": 0, "mem": 0}
        freemax = None
        resources = ["cpu", "mem"]
        for bin_ in utils.concatenate_lists_generator(self.occupied_bins,
                                                      self.bins):
            free_space = bin_.free_space()
            for res in resources:
                free[res] += free_space[res]
                if freemax:
                    if freemax[res] < free_space[res]:
                        freemax[res] = free_space[res]
                else:
                    freemax = free_space

        frag = {"cpu": 0, "mem": 0}
        for res in resources:
            if free[res] < 1e-8:
                frag[res] = 0
            else:
                frag[res] = (free[res] - freemax[res]) / free[res]

        return frag

    def _reject(self, vm):
        self.rejected_vms.append(vm)

    @abstractmethod
    def _try_to_allocate_vm(self, vm):
        pass

    @abstractmethod
    def _remove_vms(self, vms_to_remove):
        pass

    def _handle_end_time(self, start_time):
        actual_time = start_time
        while self.end_times:
            if actual_time < heapq.nsmallest(1, self.end_times)[0]:
                break
            end_time_to_delete = heapq.heappop(self.end_times)
            if self.vms_end_times.get(end_time_to_delete):
                vms_to_remove = self.vms_end_times.get(end_time_to_delete, [])
                self._remove_vms(vms_to_remove)
                del self.vms_end_times[end_time_to_delete]

    def __str__(self):
        output = {
            "max_cpu": self.max_cpu,
            "max_mem": self.max_mem,
            "max_cpu_per_bin": self.max_cpu_per_bin,
            "max_mem_per_bin": self.max_mem_per_bin,
            "number_bins": self.number_bins,
            "number_occupied_bins": len(self.occupied_bins),
            "number_of_allocated_vms": len(self.vm_bins),
            "number_of_rejected_vms": len(self.rejected_vms),
            "fragmentation": self.fragmentation()
        }
        return str(output)
