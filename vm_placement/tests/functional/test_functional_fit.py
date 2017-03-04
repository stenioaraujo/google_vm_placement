import os
import unittest

from vm_placement.Worst_fit import WorstFit

TST_DIR = os.path.dirname(os.path.abspath(__file__))


class FunctionalTestFitReadingFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.number_bins = 2
        cls.max_cpu = 10.2
        cls.max_mem = 10.4
        cls.csv_file = os.path.join(TST_DIR, "data/test_task_events.csv")
        cls.number_of_vm_requests = cls._count_lines(cls.csv_file) - 1

        cls.worst_fit = WorstFit(number_bins=cls.number_bins,
                                 max_cpu=cls.max_cpu, max_mem=cls.max_mem,
                                 csv_file=cls.csv_file)

        cls.worst_fit.start_allocation()

    @staticmethod
    def _count_lines(csv_file):
        with open(csv_file, "r") as csvfile:
            return len(csvfile.readlines())

    def test_number_of_vm_requests(self):
        wf = self.worst_fit
        self.assertEqual(len(wf.rejected_vms) + len(wf.vm_bins),
                         self.number_of_vm_requests)

    def test_number_of_bins(self):
        wf = self.worst_fit
        self.assertEqual(len(wf.occupied_bins) + len(wf.bins),
                         self.number_bins)

    def test_bin_sizes(self):
        for bin_ in self.worst_fit.occupied_bins + self.worst_fit.bins:
            cpu = bin_.max_capa.get("cpu")
            mem = bin_.max_capa.get("mem")

            self.assertAlmostEqual(cpu, self.max_cpu/self.number_bins,
                                   delta=1e-8)
            self.assertAlmostEqual(mem, self.max_mem/self.number_bins,
                                   delta=1e-8)

    def test_bins_without_vms_are_empty(self):
        for bin_ in self.worst_fit.bins:
            self.assertTrue(bin_.is_empty())

    def test_bins_with_vms_are_not_empty(self):
        for bin_ in self.worst_fit.occupied_bins:
            self.assertFalse(bin_.is_empty())
