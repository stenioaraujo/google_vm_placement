"""This is the implementation of the First Fit Algorithm for Virtual Machine
Placement. The algorithm is adapted to support the attributes CPU and Memory
as weights for the instances.
"""
from vm_placement import utils
from vm_placement.Fit import Fit


class FirstFit(Fit):
    _occupied_bins = set()

    def _try_to_allocate_vm(self, vm):
        for bin_ in utils.concatenate_lists_generator(self.occupied_bins,
                                                      self.bins):
            # noinspection PyBroadException
            try:
                bin_.add(vm)
                if bin_ not in self._occupied_bins:
                    self._occupied_bins.add(bin_)
                    self.occupied_bins.append(bin_)
                    self.bins.remove(bin_)

                self.vm_bins[vm.uuid] = bin_
                return True
            except:
                continue
        else:
            self._reject(vm)
            return False

    def _remove_vms(self, vms_to_remove):
        for vm in vms_to_remove:
            bin_ = self.vm_bins.get(vm.uuid)
            if bin_:
                del self.vm_bins[vm.uuid]
                bin_.remove(vm.uuid)
                if bin_.is_empty():
                    self.occupied_bins.remove(bin_)
                    self._occupied_bins.remove(bin_)
                    self.bins.append(bin_)
