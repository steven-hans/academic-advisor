import unittest
from unittest import mock

import attendanceparser.parser

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


class AttendanceTest(unittest.TestCase):
    def test_attendance_structure(self):
        with mock.patch.object(attendanceparser.parser,
                               'get_attendance',
                               return_value=mock_attendance
                               ):
            res = attendanceparser.parser.parse_attendance(
                'D1041181001')
            self.assertTrue(len(res) > 2)
            self.assertEqual(res[0].kodemk, 'INF-55201-301',
                             'Inconsistent kodemk')
            self.assertEqual(res[0].namamk.strip(),
                             'Interaksi Manusia dan Komputer',
                             'Inconsistent namamk')
            self.assertEqual(type(res[0].total_pertemuan), int,
                             'total_pertemuan should be int')
            self.assertEqual(res[0].jumlah_kehadiran, 12)


if __name__ == '__main__':
    unittest.main()
