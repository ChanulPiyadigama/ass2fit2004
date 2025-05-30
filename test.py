import unittest
from crowdedCampuss import crowdedCampus

class TestA2(unittest.TestCase):
    def validate_allocation(
        self, n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation
    ):
        # Check correct type and length
        self.assertIsInstance(allocation, list)
        self.assertEqual(len(allocation), n)

        # Class counts and satisfaction count
        counts = [0] * m
        satisfied = 0

        for i in range(n):
            class_id = allocation[i]
            self.assertTrue(0 <= class_id < m)
            counts[class_id] += 1
            time_slot = proposed_classes[class_id][0]
            if time_slot in time_preferences[i][:5]:
                satisfied += 1

        # Check class capacity constraints
        for j in range(m):
            min_cap, max_cap = proposed_classes[j][1], proposed_classes[j][2]
            self.assertGreaterEqual(counts[j], min_cap)
            self.assertLessEqual(counts[j], max_cap)

        # Check minimum satisfaction
        self.assertGreaterEqual(satisfied, minimum_satisfaction)

    def test_a_1(self):
        n, m = 1, 1
        time_preferences = [[0] + list(range(1, 20))]
        proposed_classes = [[0, 1, 1]]
        min_satisfaction = 1
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_a_2(self):
        n, m = 4, 2
        time_preferences = [[0] + list(range(1, 20))] * 4
        proposed_classes = [[0, 2, 2], [0, 2, 2]]
        min_satisfaction = 4
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_a_3(self):
        n, m = 3, 2
        time_preferences = [list(range(20)) for _ in range(n)]
        proposed_classes = [[0, 2, 3], [1, 2, 3]]
        min_satisfaction = 0
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.assertIsNone(allocation)

    def test_a_4(self):
        n, m = 5, 2
        time_preferences = [
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [1] + list(range(2, 20)) + [0],
            [1] + list(range(2, 20)) + [0],
        ]
        proposed_classes = [[0, 1, 3], [1, 1, 3]]
        min_satisfaction = 3
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_a_5(self):
        import random

        random.seed(42)
        n, m = 10, 3
        time_preferences = [random.sample(range(20), 20) for _ in range(n)]
        proposed_classes = [[0, 2, 4], [5, 2, 4], [10, 2, 4]]
        min_satisfaction = 5
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        if allocation:
            self.validate_allocation(
                n, m, time_preferences, proposed_classes, min_satisfaction, allocation
            )

    def test_a_6(self):
        n = 5
        m = 1
        time_preferences = [list(range(20)) for _ in range(n)]
        proposed_classes = [[0, 5, 5]]
        min_satisfaction = 5
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_a_7(self):
        n = 6
        m = 3
        time_preferences = [[j] + list(range(20)) for j in [0, 0, 1, 1, 2, 2]]
        proposed_classes = [[0, 2, 2], [1, 2, 2], [2, 2, 2]]
        min_satisfaction = 6
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_a_8(self):
        n = 4
        m = 2
        time_preferences = [[19, 18, 17, 16, 15] + list(range(15)) for _ in range(n)]
        proposed_classes = [[0, 2, 3], [1, 1, 2]]
        min_satisfaction = 4
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.assertIsNone(allocation)

    def test_a_9(self):
        n = 6
        m = 2
        time_preferences = [[5] + list(range(20)) for _ in range(n)]
        proposed_classes = [[5, 3, 3], [5, 3, 3]]
        min_satisfaction = 6
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_a_10(self):
        n = 4
        m = 2
        time_preferences = [
            [0] + list(range(1, 20)),
            [1, 2] + list(range(3, 20)) + [0],
            [1, 2] + list(range(3, 20)) + [0],
            [2, 1] + list(range(3, 20)) + [0],
        ]
        proposed_classes = [[0, 1, 2], [1, 1, 2]]
        min_satisfaction = 2
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_g_1(self):
        n = 1
        m = 1
        prefs = [list(range(20))]
        classes = [[0, 1, 1]]
        min_sat = 1
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_g_2(self):
        n = 2
        m = 1
        prefs = [list(range(20))] * 2
        classes = [[0, 2, 2]]
        min_sat = 2
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_g_3(self):
        n = 2
        m = 2
        prefs = [[1, 0] + list(range(2, 20)), list(range(20))]
        classes = [[1, 1, 1], [0, 1, 1]]
        min_sat = 2
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_g_4(self):
        n = 3
        m = 2
        prefs = [
            [0, 1] + list(range(2, 20)),
            [1, 0] + list(range(2, 20)),
            [0, 1] + list(range(2, 20)),
        ]
        classes = [[0, 2, 2], [1, 1, 2]]
        min_sat = 2
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_g_5(self):
        n = 4
        m = 2
        prefs = [[0, 1] + list(range(2, 20)) for _ in range(2)] + [
            [1, 0] + list(range(2, 20)) for _ in range(2)
        ]
        classes = [[0, 2, 2], [1, 2, 2]]
        min_sat = 4
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_g_6(self):
        n = 3
        m = 2
        prefs = [list(range(20)) for _ in range(3)]
        classes = [[0, 1, 2], [0, 1, 2]]
        min_sat = 3
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_g_7(self):
        n = 4
        m = 2
        prefs = [list(range(20)) for _ in range(4)]
        classes = [[0, 2, 2], [0, 2, 2]]
        min_sat = 4
        allocation = crowdedCampus(n, m, prefs, classes, min_sat)
        self.validate_allocation(n, m, prefs, classes, min_sat, allocation)

    def test_j_1(self):
        n = 3
        m = 2
        time_preferences = [
            [0, 1, 2, 3, 4] + [t for t in range(20) if t not in [0, 1, 2, 3, 4]],
            [0, 1, 2, 3, 4] + [t for t in range(20) if t not in [0, 1, 2, 3, 4]],
            [1, 0, 2, 3, 4] + [t for t in range(20) if t not in [1, 0, 2, 3, 4]],
        ]
        proposed_classes = [[0, 2, 2], [1, 1, 2]]
        min_satisfaction = 2

        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, min_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, min_satisfaction, allocation
        )

    def test_n_q1_1(self):
        n = 10
        m = 2
        time_preferences = [[5] + [t for t in range(20) if t != 5] for _ in range(n)]
        proposed_classes = [[5, 1, 6], [5, 1, 6]]
        minimum_satisfaction = 10
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, minimum_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation
        )

    def test_n_q1_2(self):
        import random

        random.seed(1337)
        n = 50
        m = 5
        time_preferences = [random.sample(list(range(20)), 20) for _ in range(n)]
        proposed_classes = []
        for j in range(m):
            slot = j * 4
            min_cap = 5
            max_cap = 15
            proposed_classes.append([slot, min_cap, max_cap])
        minimum_satisfaction = 20
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, minimum_satisfaction
        )
        if allocation is not None:
            self.validate_allocation(
                n,
                m,
                time_preferences,
                proposed_classes,
                minimum_satisfaction,
                allocation,
            )

    def test_n_q1_3(self):
        n = 5
        m = 2
        time_preferences = [
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
            [0] + list(range(1, 20)),
        ]
        proposed_classes = [[19, 2, 3], [19, 2, 3]]
        minimum_satisfaction = 1
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, minimum_satisfaction
        )
        self.assertIsNone(allocation)

    def test_n_q1_4(self):
        n = 10
        m = 2
        time_preferences = [list(range(20)) for _ in range(n)]
        proposed_classes = [[0, 1, 4], [1, 1, 4]]
        minimum_satisfaction = 0
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, minimum_satisfaction
        )
        self.assertIsNone(allocation)

    def test_n_q1_5(self):
        n = 10
        m = 2
        time_preferences = [list(range(20)) for _ in range(n)]
        proposed_classes = [[0, 5, 5], [1, 5, 5]]
        minimum_satisfaction = 0
        allocation = crowdedCampus(
            n, m, time_preferences, proposed_classes, minimum_satisfaction
        )
        self.validate_allocation(
            n, m, time_preferences, proposed_classes, minimum_satisfaction, allocation
        )