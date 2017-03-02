"""This is the implementation of the Worst Fit Algorithm for Virtual Machine
Placement. The algorithm is adapted to support the attributes CPU and Memory
as weights for the instances.
"""
import heapq

from vm_placement import utils


class WorstFit:
    def __init__(self, number_bins, max_cpu_bins, max_mem_bins, csv_file):
        """Apply the WorstFit Algorithm in the CSV file

        :param number_bins: number of bins that will be used
        :param max_cpu_bins: max cpu capacity of all the bins.
        :param max_mem_bins: max memory capacity of all the bins.
        :param csv_file: the path for the csv file
        """

        self.max_cpu = max_cpu_bins
        self.max_mem = max_mem_bins
        self.number_bins = number_bins
        self.bins = utils.create_bins(number_bins, max_cpu_bins, max_mem_bins)
        self.occupied_bins = []
        self.vm_bins = {}
        self.reject_vms = []
        self.csv_file = csv_file

    def start_allocation(self):
        with open(self.csv_file, "r") as csv:
            head_keys = utils.keys_from_csv_head(csv.readline())

            for vm_uuid, line in enumerate(csv):
                vm = utils.vm_from_csv_line(head_keys, line, vm_uuid)

                if vm.cpu > self.max_cpu or vm.mem > self.max_mem:
                    self._reject(vm)
                    continue

                temp_heap = []
                while self.occupied_bins:
                    # noinspection PyBroadException
                    try:
                        bin_ = heapq.heappop(self.occupied_bins)
                        heapq.heappush(temp_heap, bin_)

                        bin_.add(vm)
                        heapq.heappush(self.occupied_bins, bin_)

                        temp_heap.remove(bin_)
                        heapq.heapify(temp_heap)
                        self.occupied_bins = list(heapq.merge(
                            self.occupied_bins, temp_heap))

                        self.vm_bins[vm.uuid] = bin_
                        break
                    except:
                        continue
                else:
                    self.occupied_bins = temp_heap
                    if not self.bins:
                        self._reject(vm)
                    else:
                        bin_ = self.bins.pop()
                        bin_.add(vm)
                        heapq.heappush(self.occupied_bins, bin_)
                        self.vm_bins[vm.uuid] = bin_

    def __str__(self):
        output = {
            "max_cpu": self.max_cpu,
            "max_mem": self.max_mem,
            "number_bins": self.number_bins,
            "number_occupied_bins": len(self.occupied_bins),
            "number_of_allocated_vms": len(self.vm_bins),
            "number_of_rejected_vms": len(self.reject_vms)
        }
        return str(output)

    def _reject(self, vm):
        self.reject_vms.append(vm)
        pass
