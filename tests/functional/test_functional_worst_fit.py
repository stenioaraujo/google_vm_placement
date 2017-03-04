import heapq
import unittest

from vm_placement.Worst_fit import WorstFit
from vm_placement import utils


class FunctionalTestWorstFitAlgorithm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data1 = "data/test_task_events_deletion.csv"
        cls.data2 = "data/test_task_events_fullness.csv"

        cls.worst_fit1 = WorstFit(number_bins=5, max_cpu=50, max_mem=50,
                                  csv_file=cls.data1)
        cls.worst_fit2 = WorstFit(number_bins=5, max_cpu=1.5, max_mem=2,
                                  csv_file=cls.data2)

        cls.worst_fit1.start_allocation()
        cls.worst_fit2.start_allocation()

        cls.algorithm_executions = [cls.worst_fit1, cls.worst_fit2]

    def test_order_of_occupied_bins_correct_for_worst_fit(self):
        for alg in self.algorithm_executions:
            last_cpu_capacity = 0
            temp_heap = []
            while alg.occupied_bins:
                bin_ = heapq.heappop(alg.occupied_bins)
                cpu = bin_.capacity.get("cpu")
                self.assertGreaterEqual(cpu, last_cpu_capacity)
                last_cpu_capacity = cpu
                heapq.heappush(temp_heap, bin_)
            alg.occupied_bins = temp_heap

    def test_bins_with_vms_after_deletion(self):
        number_vms = 0
        for bin_ in utils.concatenate_lists_generator(
                self.worst_fit1.occupied_bins, self.worst_fit1.bins):
            number_vms += len(bin_.vms)

        self.assertEqual(number_vms, 5)

    def test_allocated_vms(self):
        self.assertEqual(self.worst_fit1.number_successful_allocated_vms, 10)
        self.assertEqual(self.worst_fit2.number_successful_allocated_vms, 9)

    def test_rejected_vms(self):
        self.assertEqual(len(self.worst_fit1.rejected_vms), 0)
        self.assertEqual(len(self.worst_fit2.rejected_vms), 1)
