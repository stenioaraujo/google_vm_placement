import re

from vm_placement.Structure import Bin
from vm_placement.Structure import VM

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def vm_from_csv_line(keys, csv_line, vm_id):
    csv_line = csv_line.replace("\n", "").replace('"', '').split(",")
    vm_dict = dict(zip(keys, csv_line))

    return VM(uuid=vm_id, cpu=float(vm_dict.get("cpu_req")),
              mem=float(vm_dict.get("memory_req")),
              start_time=int(float(vm_dict.get("time"))),
              end_time=int(float(vm_dict.get("end_time"))),
              type_vm=vm_dict.get("type"))


def keys_from_csv_head(csv_head):
    """Convert a csv_head to a list of strings with the keys in
    underscore_case.

    :param csv_head: a string divided by commas
    :return: a list with the keys in underscore_case
    """
    csv_head_keys = csv_head.replace("\n", "").replace('"', '')
    csv_head_keys = to_underscore_case(csv_head_keys).split(",")

    return csv_head_keys


def to_underscore_case(string):
    s1 = first_cap_re.sub(r'\1_\2', string)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def create_bins(number_bins, max_cpu_bins, max_mem_bins):
    bins = []

    for i in range(number_bins):
        bins.append(Bin(max_cpu_bins, max_mem_bins))

    return bins


def concatenate_lists_generator(*lists):
    for list_ in lists:
        for item in list_:
            yield item
