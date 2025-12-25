import unittest
from school_service import SchoolEnrollmentService

class TestSchoolEnrollmentService(unittest.TestCase):

    def setUp(self):
        self.service = SchoolEnrollmentService(max_students_per_class=1)

    def test_add_student_empty_name_raises(self):
        with self.assertRaises(ValueError) as cm:
            self.service.add_student("", 1)
        self.assertEqual(str(cm.exception), "Ім'я дитини не може бути порожнім.")

    @unittest.expectedFailure
    def test_add_student_class_full_raises(self):
        self.service.add_student("Учень 1", 1)
        self.service.add_student("Учень 2", 1)

        with self.assertRaises(Exception) as cm:
            self.service.add_student("Учень 3", 1)
        self.assertTrue(str(cm.exception).startswith("Немає місць у 1 класі."))
        self.assertEqual(self.service.get_total_students(), 2)

    def test_remove_nonexistent_student(self):

        self.service.add_student("Учень А", 2)
        result = self.service.remove_student("Учень Б") 
        self.assertFalse(result)

        self.assertEqual(self.service.get_total_students(), 1)

    def test_get_class_roster_and_keyerror(self):
    
        student_a = "Учень 1А"
        student_b = "Учень 2А"
        self.service.add_student(student_a, 1)
        self.service.add_student(student_b, 2)
        roster_1a = self.service.get_class_roster('1-A')
        self.assertIn(student_a, roster_1a)
        self.assertEqual(len(roster_1a), 1)
     
        with self.assertRaises(KeyError):
            self.service.get_class_roster('5-A')

if __name__ == '__main__':
    import xmlrunner
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)
    unittest.main(verbosity=2)
