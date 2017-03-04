import unittest

from vm_placement.Structure import Bin
from vm_placement.Structure import VM


class UnitTestStructureBin(unittest.TestCase):
    def setUp(self):
        self.bin1 = Bin(cpu_capa=0.3, mem_capa=0.4)
        self.bin2 = Bin(cpu_capa=0.001, mem_capa=0.001)
        self.vm1 = VM("1", cpu=0.25, mem=0.2, start_time=0, end_time=2,
                      type_vm="medium")
        self.vm2 = VM("2", cpu=0.05, mem=0.2, start_time=2, end_time=4,
                      type_vm="small")

    def test_add_vms(self):
        self.assertEqual(len(self.bin1.vms), 0)

        self.bin1.add(self.vm1)
        self.assertEqual(len(self.bin1.vms), 1)
        print(self.bin1.vms)
        self.assertEqual(self.vm1, self.bin1.vms.get(self.vm1.uuid))

    def test_remove_vm(self):
        self.bin1.add(self.vm1)

        self.bin1.remove(self.vm1.uuid)
        self.assertEqual(len(self.bin1.vms), 0)

    def test_change_capacity(self):
        self.assertAlmostEqual(self.bin1.capacity.get("cpu"), 0, delta=1e-8)
        self.assertAlmostEqual(self.bin1.capacity.get("mem"), 0, delta=1e-8)

        self.bin1.add(self.vm1)

        self.assertAlmostEqual(self.bin1.capacity.get("cpu"), 0.25, delta=1e-8)
        self.assertAlmostEqual(self.bin1.capacity.get("mem"), 0.2, delta=1e-8)

    def test_capacity_same_vms_in_bin(self):
        self.bin1.add(self.vm1)
        self.bin1.add(self.vm2)

        vms = [self.vm1, self.vm2]
        cpu_vms_total = sum(vm.cpu for vm in vms)
        mem_vms_total = sum(vm.mem for vm in vms)

        self.assertAlmostEqual(self.bin1.capacity.get("cpu"), cpu_vms_total,
                               delta=1e-8)
        self.assertAlmostEqual(self.bin1.capacity.get("mem"), mem_vms_total,
                               delta=1e-8)

    def test_if_vm_fit(self):
        self.assertTrue(self.bin1.fit(self.vm1))
        self.assertFalse(self.bin2.fit(self.vm1))

    def test_add_vm_when_bin_is_full(self):
        self.assertRaises(Exception, self.bin2.add, self.vm1)

    def test_bin_emptiness(self):
        self.assertTrue(self.bin1.is_empty())

        self.bin1.add(self.vm1)
        self.assertFalse(self.bin1.is_empty())

        self.bin1.remove(self.vm1.uuid)
        self.assertTrue(self.bin1.is_empty())

    def test_complete_bin(self):
        self.bin1.add(self.vm1)
        self.bin1.add(self.vm2)
        self.assertEqual(len(self.bin1.vms), 2)

    def test_free_space(self):
        self.assertEqual(self.bin1.free_space(),
                         {"cpu": self.bin1.max_capa["cpu"],
                          "mem": self.bin1.max_capa["mem"]})
        self.bin1.add(self.vm1)
        self.assertEqual(self.bin1.free_space(),
                         {"cpu": self.bin1.max_capa["cpu"] - self.vm1.cpu,
                          "mem": self.bin1.max_capa["mem"] - self.vm1.mem})
        self.bin1.add(self.vm2)
        self.assertEqual(self.bin1.free_space(), {"cpu": 0, "mem": 0})
        self.bin1.remove(self.vm1.uuid)
        self.assertEqual(self.bin1.free_space(),
                         {"cpu": self.bin1.max_capa["cpu"] - self.vm2.cpu,
                          "mem": self.bin1.max_capa["mem"] - self.vm2.mem})
        self.bin1.remove(self.vm2.uuid)
        self.assertEqual(self.bin1.free_space(),
                         {"cpu": self.bin1.max_capa["cpu"],
                          "mem": self.bin1.max_capa["mem"]})
