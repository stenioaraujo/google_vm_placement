class Bin:
    def __init__(self, cpu_capa, mem_capa):
        self.vms = {}
        self.capacity = {"cpu": 0, "mem": 0}
        self.max_capa = {"cpu": cpu_capa, "mem": mem_capa}

    def add(self, vm):
        if not self.fit(vm):
            raise Exception("The Bin cannot fit the VM")

        self.vms[vm.uuid] = vm
        self._add_to_capacity(vm)

    def _add_to_capacity(self, vm, multiply_by=1):
        self.capacity["cpu"] += multiply_by * vm.cpu
        self.capacity["mem"] += multiply_by * vm.mem

    def fit(self, vm):
        fits_cpu = self.capacity["cpu"] + vm.cpu <= self.max_capa["cpu"]
        fits_mem = self.capacity["mem"] + vm.mem <= self.max_capa["mem"]

        return fits_cpu and fits_mem

    def remove(self, vm_uuid):
        vm = self.vms.pop(vm_uuid)
        self._add_to_capacity(vm, multiply_by=-1)

    def is_empty(self):
        return sum(self.capacity.values()) < 1.0e-8

    def __lt__(self, other):
        return self.capacity.get("cpu") < other.capacity.get("cpu")

    def __str__(self):
        return 'Bin (current_capacity=%s, items=%s, max_capacity=%s)' % (
            self.capacity, str(self.vms), self.max_capa)


class VM:
    def __init__(self, uuid, cpu, mem, start_time, end_time, type_vm):
        self.uuid = uuid
        self.cpu = cpu
        self.mem = mem
        self.start_time = start_time
        self.end_time = end_time
        self.type = type_vm

    def __str__(self):
        return "VM (id=%s, cpu=%s, mem=%s, end=%s, type=%s" % (self.uuid,
                                                               self.cpu,
                                                               self.mem,
                                                               self.end_time,
                                                               self.type)

    def __hash__(self):
        return self.uuid
