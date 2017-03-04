import unittest

from vm_placement.First_fit import FirstFit
from vm_placement import utils


class FunctionalTestFirstFitAlgorithm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data1 = "data/test_task_events_deletion.csv"
        cls.data2 = "data/test_task_events_fullness.csv"

        cls.first_fit1 = FirstFit(number_bins=5, max_cpu=50, max_mem=50,
                                  csv_file=cls.data1)
        cls.first_fit2 = FirstFit(number_bins=5, max_cpu=1.5, max_mem=2,
                                  csv_file=cls.data2)

        cls.first_fit1.start_allocation()
        cls.first_fit2.start_allocation()

        cls.algorithm_executions = [cls.first_fit1, cls.first_fit2]

    def test_bins_with_vms_after_deletion(self):
        number_vms = 0
        for bin_ in utils.concatenate_lists_generator(
                self.first_fit1.occupied_bins, self.first_fit1.bins):
            number_vms += len(bin_.vms)

        self.assertEqual(number_vms, 5)

    def test_allocated_vms(self):
        self.assertEqual(self.first_fit1.number_successful_allocated_vms, 10)
        self.assertEqual(self.first_fit2.number_successful_allocated_vms, 9)

    def test_rejected_vms(self):
        self.assertEqual(len(self.first_fit1.rejected_vms), 0)
        self.assertEqual(len(self.first_fit2.rejected_vms), 1)
