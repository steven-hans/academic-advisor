import unittest
from typing import List
from unittest import mock

import attendanceparser.parser
from attendanceparser import parser as AP
from attendanceparser.attendance import Attendance
from rulechecker import RuleChecker
from ruleresult import RuleResult
from transcriptparser import parser as TP
from transcriptparser.transcript import Transcript

mock_attendance = [
    {'kodemk': 'INF-55201-301',
     'namamk': 'Interaksi Manusia dan Komputer ',
     'total_pertemuan': 13, 'jumlah_kehadiran': 12,
     'matakuliah_id': 15929,
     'skor': 92},
    {'kodemk': 'INF-55201-302', 'namamk': 'Pemrograman Web*',
     'total_pertemuan': 40, 'jumlah_kehadiran': 19,
     'matakuliah_id': 15526, 'skor': 48},
    {'kodemk': 'INF-55201-303', 'namamk': 'Pemrograman Jaringan*',
     'total_pertemuan': 4, 'jumlah_kehadiran': 5,
     'matakuliah_id': 18564,
     'skor': 125},
    {'kodemk': 'INF-55201-304', 'namamk': 'Sistem Tertanam',
     'total_pertemuan': 9, 'jumlah_kehadiran': 9,
     'matakuliah_id': 15810, 'skor': 100},
    {'kodemk': 'INF-55201-305', 'namamk': 'Kecerdasan Buatan',
     'total_pertemuan': 14, 'jumlah_kehadiran': 9,
     'matakuliah_id': 16623,
     'skor': 64},
    {'kodemk': 'INF-55201-306',
     'namamk': 'Manajemen Proyek Perangkat Lunak',
     'total_pertemuan': 13, 'jumlah_kehadiran': 11,
     'matakuliah_id': 14798,
     'skor': 85},
    {'kodemk': 'INF-55201-308', 'namamk': 'Riset Operasi',
     'total_pertemuan': 21, 'jumlah_kehadiran': 15,
     'matakuliah_id': 12150, 'skor': 71},
    {'kodemk': 'INF-55201-310',
     'namamk': 'Penulisan Proposal Tugas Akhir ',
     'total_pertemuan': 11, 'jumlah_kehadiran': 11,
     'matakuliah_id': 12154,
     'skor': 100}
]


class RuleBase():
    T: Transcript = None
    A: List[Attendance] = []
    C: RuleChecker = None

    def refresh_checker(self):
        self.C: RuleChecker = RuleChecker(self.T, self.A)

    def initial_setUp(self):
        self.T = TP.extract_transcript('transcriptparser/test.pdf')
        with mock.patch.object(attendanceparser.parser,
                               'get_attendance',
                               return_value=mock_attendance
                               ):
            self.A: List[Attendance] = AP.parse_attendance(
                self.T.student_id)
        self.C: RuleChecker = RuleChecker(self.T, self.A)


class RulePertemuanTiapSemester(unittest.TestCase, RuleBase):
    def setUp(self) -> None:
        self.initial_setUp()

    def tearDown(self) -> None:
        self.T = None
        self.A = []
        self.C = None

    def test_not_enough_meeting(self):
        meeting_count: int = self.A[0].total_pertemuan
        self.assertEqual(meeting_count, 13)

        result: List[
            RuleResult] = self.C.rule_pertemuan_tiap_semester()

        self.assertTrue(len(result) != 0)
        self.assertEqual(result[0].error[:13], 'INF-55201-301')

    def test_enough_meeting(self):
        self.A[0].total_pertemuan = 16
        self.refresh_checker()
        result: List[
            RuleResult] = self.C.rule_pertemuan_tiap_semester()

        self.assertNotEqual(result[0].error[:13], 'INF-55201-301')

    def test_overflowing_meeting(self):
        self.A[0].total_pertemuan = 24  # 3 SKS should be 16 only
        self.refresh_checker()
        result: List[
            RuleResult] = self.C.rule_pertemuan_tiap_semester()

        self.assertNotEqual(result[0].error[:13], 'INF-55201-301')


class RuleHadirKuliah(unittest.TestCase, RuleBase):
    def setUp(self) -> None:
        self.initial_setUp()

    def tearDown(self) -> None:
        self.T = None
        self.A = []
        self.C = None

    def test_no_attendance_at_all(self):
        self.A[0].jumlah_kehadiran = 0
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_hadir_kuliah()

        self.assertEqual(result[0].error[:13], 'INF-55201-301')

    def test_not_enough_attendance(self):
        self.A[0].jumlah_kehadiran = 1
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_hadir_kuliah()

        self.assertEqual(result[0].error[:13], 'INF-55201-301')

    def test_just_enough_attendance(self):
        self.A[0].jumlah_kehadiran = 15
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_hadir_kuliah()

        self.assertNotEqual(result[0].error[:13], 'INF-55201-301')

    def test_overflowing_attendance_because_bad_database(self):
        self.A[0].jumlah_kehadiran = 100
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_hadir_kuliah()

        self.assertNotEqual(result[0].error[:13], 'INF-55201-301')


class RulePenyelesaianStudi(unittest.TestCase, RuleBase):
    def setUp(self) -> None:
        self.initial_setUp()

    def tearDown(self) -> None:
        self.T = None
        self.A = []
        self.C = None

    def test_no_failed_courses(self):
        result: RuleResult = self.C.rule_penyelesaian_studi()
        self.assertIsNone(result)

    def test_failed_one_course(self):
        self.T.course_taken[3].grade = 'E'
        self.refresh_checker()

        result: RuleResult = self.C.rule_penyelesaian_studi()
        self.assertIsNotNone(result)


class RuleSpecialCourse(unittest.TestCase, RuleBase):
    def setUp(self) -> None:
        self.initial_setUp()

    def tearDown(self) -> None:
        self.T = None
        self.A = []
        self.C = None

    def test_passed_all(self):
        self.T.sks_taken = 111
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_special_course()
        self.assertTrue(len(result) == 0)

    def test_sks_too_low(self):
        self.T.sks_taken = 1
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_special_course()
        self.assertTrue(len(result) == 1)

    def test_sum_too_high(self):
        self.T.sks_taken = 111
        self.T.course_taken[0].grade = 'D+'
        self.T.course_taken[1].grade = 'D+'
        self.T.course_taken[2].grade = 'D+'
        self.T.course_taken[3].grade = 'D+'
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_special_course()
        self.assertTrue(len(result) == 1)

    def test_ipk_too_low(self):
        self.T.sks_taken = 111
        self.T.current_ipk = 1.85
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_special_course()
        self.assertTrue(len(result) == 1)

    def test_threshold_value(self):
        self.T.sks_taken = 120
        self.T.current_ipk = 2.00
        self.T.course_taken[0].grade = 'D+'
        self.T.course_taken[1].grade = 'D+'
        self.T.course_taken[2].grade = 'D+'
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_special_course()
        self.assertTrue(len(result) == 0)


class RuleSkripsi(unittest.TestCase, RuleBase):
    def setUp(self) -> None:
        self.initial_setUp()

    def tearDown(self) -> None:
        self.T = None
        self.A = []
        self.C = None

    def test_passed_all(self):
        self.T.sks_taken = 140
        self.T.current_ipk = 3.98
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_skripsi()
        self.assertTrue(len(result) == 0)

    def test_sks_too_low(self):
        self.T.sks_taken = 50
        self.T.current_ipk = 3.98
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_skripsi()
        self.assertTrue(len(result) == 1)

    def test_sum_too_high(self):
        self.T.sks_taken = 140
        self.T.current_ipk = 3.00
        self.T.course_taken[0].grade = 'D+'
        self.T.course_taken[1].grade = 'D+'
        self.T.course_taken[2].grade = 'D+'
        self.T.course_taken[3].grade = 'D+'
        self.T.course_taken[4].grade = 'D+'
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_skripsi()
        self.assertTrue(len(result) == 1)

    def test_ipk_too_low(self):
        self.T.sks_taken = 140
        self.T.current_ipk = 1.50
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_skripsi()
        self.assertTrue(len(result) == 1)

    def test_threshold_value(self):
        self.T.sks_taken = 120
        self.T.course_taken[0].grade = 'D+'
        self.T.course_taken[1].grade = 'D+'
        self.T.course_taken[2].grade = 'D+'
        self.T.course_taken[3].grade = 'D+'
        self.T.current_ipk = 2.00
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_skripsi()
        self.assertTrue(len(result) == 0)


class UjianSkripsi(unittest.TestCase, RuleBase):
    def setUp(self) -> None:
        self.initial_setUp()

    def tearDown(self) -> None:
        self.T = None
        self.A = []
        self.C = None

    def test_passed_all(self):
        self.T.sks_taken = 140
        self.T.current_ipk = 3.98
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_ujian_skripsi()
        self.assertTrue(len(result) == 0)

    def test_sks_too_low(self):
        self.T.sks_taken = 120
        self.T.current_ipk = 3.98
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_ujian_skripsi()
        self.assertTrue(len(result) == 1)

    def test_sum_too_high(self):
        self.T.sks_taken = 140
        self.T.course_taken[0].grade = 'D+'
        self.T.course_taken[1].grade = 'D+'
        self.T.course_taken[2].grade = 'D+'
        self.T.course_taken[3].grade = 'D+'
        self.T.current_ipk = 2.00
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_ujian_skripsi()
        self.assertTrue(len(result) == 0)

    def test_threshold_value(self):
        self.T.sks_taken = 140
        self.T.course_taken[0].grade = 'D+'
        self.T.course_taken[1].grade = 'D+'
        self.T.course_taken[2].grade = 'D+'
        self.T.current_ipk = 2.00
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_ujian_skripsi()
        self.assertTrue(len(result) == 0)


class Predikat(unittest.TestCase, RuleBase):
    def setUp(self) -> None:
        self.initial_setUp()

    def tearDown(self) -> None:
        self.T = None
        self.A = []
        self.C = None

    def test_default_verdict(self):
        self.T.course_taken[0].grade = 'D+'
        self.T.course_taken[1].grade = 'D+'
        self.T.course_taken[2].grade = 'D+'
        self.T.course_taken[3].grade = 'D+'
        self.T.current_ipk = 2.00
        self.refresh_checker()

        result: RuleResult = self.C.rule_potensi_predikat_kelulusan()
        self.assertEqual(result.error, 'Lulus')

    def test_good_verdict(self):
        self.T.course_taken[0].grade = 'D+'
        self.T.course_taken[1].grade = 'D+'
        self.T.course_taken[2].grade = 'D+'
        self.T.current_ipk = 2.77
        self.refresh_checker()

        result: RuleResult = self.C.rule_potensi_predikat_kelulusan()
        self.assertEqual(result.error, 'Memuaskan')

    def test_better_verdict(self):
        self.T.course_taken[0].grade = 'C+'
        self.T.course_taken[1].grade = 'C+'
        self.T.course_taken[2].grade = 'C'
        self.T.current_ipk = 3.01
        self.refresh_checker()

        result: RuleResult = self.C.rule_potensi_predikat_kelulusan()
        self.assertEqual(result.error, 'Sangat memuaskan')

    def test_best_verdict(self):
        self.T.course_taken[0].grade = 'B'
        self.T.course_taken[1].grade = 'B'
        self.T.current_ipk = 3.51
        self.refresh_checker()

        result: RuleResult = self.C.rule_potensi_predikat_kelulusan()
        self.assertEqual(result.error, 'Dengan Pujian')


class Evaluation(unittest.TestCase, RuleBase):
    def setUp(self) -> None:
        self.initial_setUp()

    def tearDown(self) -> None:
        self.T = None
        self.A = []
        self.C = None

    @mock.patch('rulechecker.RuleChecker.get_current_semester')
    def test_even_semester(self, gcs):
        # note: List[RuleResult] should be empty
        gcs.return_value = 2
        self.T.sks_taken = 43
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_evaluasi()
        self.assertEqual(result, [])

    @mock.patch('rulechecker.RuleChecker.get_current_semester')
    def test_two_year_eval_passed(self, gcs):
        gcs.return_value = 5

        result: List[RuleResult] = self.C.rule_evaluasi()
        self.assertEqual(result, [])

    @mock.patch('rulechecker.RuleChecker.get_current_semester')
    def test_two_year_eval_failed(self, gcs):
        gcs.return_value = 5
        self.T.sks_taken = 43
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_evaluasi()
        self.assertTrue(len(result) == 1)

    @mock.patch('rulechecker.RuleChecker.get_current_semester')
    def test_three_year_eval_passed(self, gcs):
        gcs.return_value = 7
        self.T.sks_taken = 95
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_evaluasi()
        self.assertEqual(result, [])

    @mock.patch('rulechecker.RuleChecker.get_current_semester')
    def test_three_year_eval_failed(self, gcs):
        gcs.return_value = 7
        self.T.sks_taken = 95
        self.T.course_taken[0].grade = 'D'
        self.T.course_taken[1].grade = 'D'
        self.T.course_taken[2].grade = 'D'
        self.T.course_taken[3].grade = 'D'
        self.T.course_taken[4].grade = 'D'
        self.refresh_checker()

        result: List[RuleResult] = self.C.rule_evaluasi()
        self.assertTrue(len(result) == 1)

    @mock.patch('rulechecker.RuleChecker.get_current_semester')
    def test_final_term_passed(self, gcs):
        self.skipTest('Current implementation is not feasible.')

    @mock.patch('rulechecker.RuleChecker.get_current_semester')
    def test_final_term_failed(self, gcs):
        self.skipTest('Current implementation is not feasible.')


class BatasWaktuStudi(unittest.TestCase, RuleBase):
    def setUp(self) -> None:
        self.initial_setUp()

    def tearDown(self) -> None:
        self.T = None
        self.A = []
        self.C = None

    @mock.patch('rulechecker.RuleChecker.get_current_semester')
    def test_odd_semester(self, gcs):
        gcs.return_value = 1
        result: RuleResult = self.C.rule_batas_waktu_studi()
        self.assertEqual(result.error,
                         'Batas waktu studi: 13 semester')

    @mock.patch('rulechecker.RuleChecker.get_current_semester')
    def test_even_semester(self, gcs):
        gcs.return_value = 6
        result: RuleResult = self.C.rule_batas_waktu_studi()
        self.assertEqual(result.error,
                         'Batas waktu studi: 8 semester')


if __name__ == '__main__':
    unittest.main()
