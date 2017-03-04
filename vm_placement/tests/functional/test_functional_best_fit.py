import heapq_max
import os
import unittest

from vm_placement.Best_fit import BestFit
from vm_placement import utils

TST_DIR = os.path.dirname(os.path.abspath(__file__))


class FunctionalTestBestFitAlgorithm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data1 = os.path.join(TST_DIR, "data/test_task_events_deletion.csv")
        cls.data2 = os.path.join(TST_DIR, "data/test_task_events_fullness.csv")

        cls.best_fit1 = BestFit(number_bins=5, max_cpu=50, max_mem=50,
                                csv_file=cls.data1)
        cls.best_fit2 = BestFit(number_bins=5, max_cpu=1.5, max_mem=2,
                                csv_file=cls.data2)

        cls.best_fit1.start_allocation()
        cls.best_fit2.start_allocation()

        cls.algorithm_executions = [cls.best_fit1, cls.best_fit2]

    def test_order_of_occupied_bins_correct_for_worst_fit(self):
        for alg in self.algorithm_executions:
            last_cpu_capacity = 999999
            temp_heap = []
            while alg.occupied_bins:
                bin_ = heapq_max.heappop_max(alg.occupied_bins)
                cpu = bin_.capacity.get("cpu")
                self.assertLessEqual(cpu, last_cpu_capacity)
                last_cpu_capacity = cpu
                heapq_max.heappush_max(temp_heap, bin_)
            alg.occupied_bins = temp_heap

    def test_bins_with_vms_after_deletion(self):
        number_vms = 0
        for bin_ in utils.concatenate_lists_generator(
                self.best_fit1.occupied_bins, self.best_fit1.bins):
            number_vms += len(bin_.vms)

        self.assertEqual(number_vms, 5)

    def test_allocated_vms(self):
        self.assertEqual(self.best_fit1.number_successful_allocated_vms, 10)
        self.assertEqual(self.best_fit2.number_successful_allocated_vms, 9)

    def test_rejected_vms(self):
        self.assertEqual(len(self.best_fit1.rejected_vms), 0)
        self.assertEqual(len(self.best_fit2.rejected_vms), 1)