"""This is the implementation of the Best Fit Algorithm for Virtual Machine
Placement. The algorithm is adapted to support the attributes CPU and Memory
as weights for the instances.
"""
import heapq_max

from vm_placement.Fit import Fit


class BestFit(Fit):
    def _try_to_allocate_vm(self, vm):
        temp_heap = []
        while self.occupied_bins:
            # noinspection PyBroadException
            try:
                bin_ = heapq_max.heappop_max(self.occupied_bins)
                heapq_max.heappush_max(temp_heap, bin_)

                bin_.add(vm)
                heapq_max.heappush_max(self.occupied_bins, bin_)
                temp_heap.remove(bin_)

                while temp_heap:
                    temp_bin = heapq_max.heappop_max(temp_heap)
                    heapq_max.heappush_max(self.occupied_bins, temp_bin)

                self.vm_bins[vm.uuid] = bin_
                return True
            except:
                continue
        else:
            self.occupied_bins = temp_heap
            if not self.bins:
                self._reject(vm)
                return False
            else:
                bin_ = self.bins.pop()
                bin_.add(vm)
                heapq_max.heappush_max(self.occupied_bins, bin_)
                self.vm_bins[vm.uuid] = bin_
                return True

    def _remove_vms(self, vms_to_remove):
        for vm in vms_to_remove:
            bin_ = self.vm_bins.get(vm.uuid)
            if bin_:
                del self.vm_bins[vm.uuid]
                bin_.remove(vm.uuid)
                if bin_.is_empty():
                    self.occupied_bins.remove(bin_)
                    self.bins.append(bin_)
        heapq_max.heapify_max(self.occupied_bins)
