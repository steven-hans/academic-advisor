import unittest

from transcriptparser import parser


class TestRegexFind(unittest.TestCase):
    def setUp(self) -> None:
        self.text = parser.get_pdf_text('test.pdf')

    def test_ipk_sks(self):
        ipk_sks = parser.get_ipk_sks(self.text)
        self.assertEqual(ipk_sks, (3.97, 89))

    def test_year(self):
        year = parser.get_year(self.text)
        self.assertEqual(year, 2018)

    def test_course_codes_list(self):
        courses = parser.get_course_codes(self.text)
        target = ['INF-55201-101', 'INF-55201-102', 'INF-55201-103',
                  'INF-55201-104', 'MKWU1', 'MKWU2', 'UMG-55201-103',
                  'INF-55201-105', 'INF-55201-106', 'INF-55201-107',
                  'INF-55201-108', 'INF-55201-109', 'MKWU3', 'MKWU4',
                  'INF-55201-201', 'INF-55201-202', 'INF-55201-203',
                  'INF-55201-204', 'INF-55201-205', 'INF-55201-206',
                  'INF-55201-207', 'INF-55201-208', 'INF-55201-209',
                  'INF-55201-210', 'INF-55201-211', 'INF-55201-212',
                  'INF-55201-213', 'INF-55201-214', 'INF-55201-304',
                  'INF-55201-307', 'INF-55201-309']
        self.assertEqual(courses, target)

    # note: this test is potentially not strict enough to check
    # that the ordering is correct
    def test_course_sks_list(self):
        sks_list = parser.get_course_sks(self.text)
        target = [3, 3, 4, 2, 3, 2, 2, 3, 3, 3, 3, 4, 2, 2, 2, 2, 3,
                  3, 4, 4, 3, 4, 2, 3, 4, 3, 2, 3, 3, 2, 3]
        self.assertEqual(sks_list, target)

    # note: this test is potentially not strict enough to check
    # that the ordering is correct.
    def test_grade_list(self):
        grade_list = parser.get_grades(self.text)
        target = ['A', 'A', 'B+', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                  'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                  'A', 'A', 'A', 'A',
                  'A', 'A', 'B+', 'A', 'A', 'A', 'A']
        self.assertEqual(grade_list, target)

    def test_consistent_course_components(self):
        course_size = len(parser.get_course_codes(self.text))
        sks_size = len(parser.get_course_sks(self.text))
        grade_size = len(parser.get_grades(self.text))
        self.assertTrue(course_size == sks_size == grade_size)


if __name__ == '__main__':
    unittest.main()
