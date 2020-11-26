from datetime import datetime
from typing import List

from attendanceparser.attendance import Attendance
from ruleresult import RuleResult
from transcriptparser.transcript import Transcript

COURSE_SKS_ALL = {"MKWU2": 2,
                  "UMG-55201-103": 2,
                  "MKWU1": 3,
                  "INF-55201-101": 3,
                  "INF-55201-102": 3,
                  "INF-55201-103": 4,
                  "INF-55201-104": 2,
                  "INF-55201-201": 2,
                  "INF-55201-202": 2,
                  "INF-55201-203": 3,
                  "INF-55201-204": 3,
                  "INF-55201-205": 4,
                  "INF-55201-206": 4,
                  "INF-55201-207": 3,
                  "INF-55201-301": 2,
                  "INF-55201-302": 4,
                  "INF-55201-303": 3,
                  "INF-55201-304": 3,
                  "INF-55201-305": 3,
                  "INF-55201-306": 2,
                  "INF-55201-307": 2,
                  "INF-55201-308": 2,
                  "INF-55201-401": 3,
                  "INF-55201-402": 2,
                  "INF-55201-501": 3,
                  "INF-55201-502": 3,
                  "INF-55021-500": 3,
                  "INF-55021-501": 3,
                  "INF-55021-502": 3,
                  "INF-55021-503": 3,
                  "INF-55021-504": 3,
                  "INF-55021-505": 3,
                  "INF-55021-506": 3,
                  "INF-55021-507": 3,
                  "INF-55021-508": 3,
                  "INF-55021-509": 3,
                  "INF-55201-510": 3,
                  "INF-55201-511": 3,
                  "INF-55201-512": 3,
                  "INF-55201-513": 3,
                  "INF-55201-514": 3,
                  "INF-55201-515": 3,
                  "INF-55201-516": 3,
                  "INF-55201-517": 3,
                  "INF-55201-518": 3,
                  "INF-55201-519": 3,
                  "INF-55201-520": 3,
                  "INF-55201-521": 3,
                  "INF-55201-522": 3,
                  "INF-55201-523": 3,
                  "INF-55201-524": 3,
                  "INF-55201-525": 3,
                  "INF-55201-526": 3,
                  "INF-55201-527": 3,
                  "INF-55201-528": 3,
                  "INF-55201-529": 3,
                  "INF-55201-530": 3,
                  "INF-55201-531": 3,
                  "INF-55201-532": 3,
                  "INF-55201-533": 3,
                  "INF-55201-534": 3,
                  "INF-55201-535": 3,
                  "INF-55201-536": 3,
                  "INF-55201-537": 3,
                  "INF-55201-538": 3,
                  "INF-55201-539": 3,
                  "INF-55201-540": 3,
                  "INF-55201-541": 3,
                  "INF-55201-542": 3,
                  "INF-55201-543": 3,
                  "INF-55201-544": 3,
                  "INF-55201-545": 3,
                  "INF-55201-546": 3,
                  "INF-55201-547": 3,
                  "INF-55201-548": 3,
                  "INF-55201-549": 3,
                  "INF-55201-550": 3,
                  "INF-55201-551": 3,
                  "INF-55201-552": 3,
                  "INF-55201-553": 3,
                  "INF-55201-554": 3,
                  "INF-55201-555": 3,
                  "INF-55201-556": 3,
                  "INF-55201-557": 3,
                  "INF-55201-558": 3,
                  "INF-55201-559": 3,
                  "INF-55201-560": 3,
                  "INF-55201-561": 3,
                  "INF-55201-562": 3,
                  "INF-55201-563": 3,
                  "INF-55201-564": 3,
                  "INF-55201-565": 3,
                  "INF-55201-566": 3,
                  "INF-55201-567": 3,
                  "INF-55201-568": 3,
                  "INF-55201-569": 3,
                  "INF-55201-570": 3,
                  "INF-55201-571": 3,
                  "INF-55201-572": 3,
                  "INF-55201-573": 3,
                  "INF-55201-574": 3,
                  "INF-55201-575": 3,
                  "INF-55201-576": 3,
                  "INF-55201-577": 3,
                  "INF-55201-578": 3,
                  "INF-55201-579": 3,
                  "INF-55201-580": 3,
                  "INF-55201-581": 3,
                  "INF-55201-582": 3,
                  "INF-55201-583": 3,
                  "INF-55201-584": 3,
                  "INF-55201-585": 3,
                  "INF-55201-586": 3,
                  "INF-55201-587": 3,
                  "INF-55201-588": 3,
                  "INF-55201-589": 3,
                  "INF-55201-590": 3,
                  "INF-55201-591": 3,
                  "INF-55201-592": 3,
                  "INF-55201-593": 3,
                  "INF-55201-594": 3,
                  "INF-55201-595": 3,
                  "INF-55201-596": 3,
                  "INF-55201-597": 3,
                  "INF-55201-598": 3,
                  "INF-55201-599": 3,
                  "INF-55201-403": 2,
                  "MKWu3": 2,
                  "MKWu4": 2,
                  "INF-55201-105": 3,
                  "INF-55201-106": 3,
                  "INF-55201-107": 3,
                  "INF-55201-108": 3,
                  "INF-55201-109": 4,
                  "INF-55201-208": 4,
                  "INF-55201-209": 2,
                  "INF-55201-210": 3,
                  "INF-55201-211": 4,
                  "INF-55201-212": 3,
                  "INF-55201-213": 2,
                  "INF-55201-214": 3,
                  "INF-55201-309": 2,
                  "INF-55201-310": 3,
                  "INF-55201-311": 2,
                  "INF-55201-312": 3,
                  "INF-55201-313": 3,
                  "INF-55201-314": 3,
                  "INF-55201-315": 4,
                  "INF-55201-316": 2,
                  "INF-55201-404": 4}


class QuickStatus:
    def __init__(self, transcript: Transcript):
        self.sks_taken = transcript.sks_taken
        self.low_courses = [(x.sks_count, x.course_code,) for x in
                            transcript.course_taken if
                            (x.grade[0] == 'D')]
        self.sum_D = sum([x[0] for x in self.low_courses])
        self.low_courses_names = [x[1] for x in self.low_courses]
        self.current_ipk = transcript.current_ipk


class RuleChecker:
    TRANSCRIPT: Transcript = None
    ATTENDANCES: List[Attendance] = []
    CHECK_RESULT: List[RuleResult] = []
    QUICK_STATUS: QuickStatus = None

    def __init__(self, transcript: Transcript,
                 attendances: List[Attendance]):
        self.TRANSCRIPT = transcript
        self.ATTENDANCES = attendances
        self.QUICK_STATUS = QuickStatus(transcript)

    def rule_pertemuan_tiap_semester(self) -> List[RuleResult]:
        res = []
        for a in self.ATTENDANCES:
            course_sks = COURSE_SKS_ALL.get(a.kodemk, 3)
            if (course_sks == 4 and a.total_pertemuan < 30) or (
                    course_sks != 4 and a.total_pertemuan < 16):
                res.append(
                    RuleResult('Jumlah perkuliahan tiap semester',
                               '{} / {} SKS'.format(a.kodemk,
                                                    course_sks),
                               (
                                   'Tidak memenuhi total pertemuan '
                                   'tiap semester. Sekarang: {}. '
                                   'Kuliah harus '
                                   'dilakukan sebanyak 16 kali '
                                   'apabila < 4 SKS, dan 30 kali '
                                   'apabila 4 '
                                   'SKS.').format(a.total_pertemuan)))
        return res

    def rule_hadir_kuliah(self) -> List[RuleResult]:
        res = []
        for a in self.ATTENDANCES:
            course_sks = COURSE_SKS_ALL.get(a.kodemk, 3)
            if (course_sks == 4 and a.jumlah_kehadiran < 24) or (
                    course_sks != 4 and a.jumlah_kehadiran < 13):
                res.append(
                    RuleResult('Presensi mata kuliah tiap semester',
                               '{} / {} SKS'.format(
                                   a.kodemk, course_sks),
                               (
                                   'Tidak memenuhi total presensi '
                                   'mahasiswa tiap semester. '
                                   'Sekarang: {}. '
                                   'Harus hadir kuliah setidaknya '
                                   'sebanyak 13 kali apabila < 4 '
                                   'SKS, '
                                   'dan 24 kali apabila 4 SKS.').format(
                                   a.jumlah_kehadiran)))

        return res

    def rule_penyelesaian_studi(self) -> RuleResult:
        failed_courses = [c.course_code for c in
                          self.TRANSCRIPT.course_taken if
                          c.grade == 'E']
        if len(failed_courses) != 0:
            return RuleResult('Penyelesaian studi',
                              'Terdapat mata kuliah yang tidak lulus',
                              (
                                  '{}. Luluskan matakuliah dan '
                                  'konsultasi ke dosen PA '
                                  'untuk mencapai resolusi terkait '
                                  'hal ini.').format(
                                  ", ".join(failed_courses)))

    def rule_special_course(self) -> List[RuleResult]:
        err = []

        if self.QUICK_STATUS.sks_taken < 110:
            err.append(
                "Jumlah SKS yang telah selesai harus lebih dari "
                "sama dengan 110 SKS. SKS sekarang: {}".format(
                    self.QUICK_STATUS.sks_taken))
        if self.QUICK_STATUS.sum_D > 11:
            err.append(
                "Jumlah SKS untuk mata kuliah yang D atau D+ harus "
                "kurang dari 11 SKS. "
                "\nPerhatikan untuk mata kuliah:\n" +
                ", ".join(self.QUICK_STATUS.low_courses_names))
        if self.QUICK_STATUS.current_ipk < 2.00:
            err.append(
                "IPK sekarang harus lebih dari sama dengan 2.00. "
                "IPK sekarang: {}".format(
                    self.QUICK_STATUS.current_ipk))

        return [RuleResult('Pengerjaan KP dan PMKM',
                           'Tidak dapat dilaksanakan semester ini',
                           e) for e in err]

    def rule_skripsi(self) -> List[RuleResult]:
        err = []

        if self.QUICK_STATUS.sks_taken < 120:
            err.append(
                "Jumlah SKS yang telah selesai harus lebih dari "
                "sama dengan 120 SKS. SKS sekarang: {}".format(
                    self.QUICK_STATUS.sks_taken))
        if self.QUICK_STATUS.sum_D > 12:
            err.append(
                "Jumlah SKS untuk mata kuliah yang D atau D+ harus "
                "kurang dari sama dengan 12 SKS. "
                "\nPerhatikan untuk mata kuliah:\n" +
                ", ".join(self.QUICK_STATUS.low_courses_names))
        if self.QUICK_STATUS.current_ipk < 2.00:
            err.append(
                "IPK sekarang harus lebih dari sama dengan 2.00. "
                "IPK sekarang: {}".format(
                    self.QUICK_STATUS.current_ipk))

        return [RuleResult('Pengerjaan skripsi',
                           'Tidak dapat dilaksanakan semester ini',
                           e) for e in err]

    def rule_ujian_skripsi(self) -> List[RuleResult]:
        err = []

        if self.QUICK_STATUS.sks_taken < 140:
            err.append(
                "Jumlah SKS yang telah selesai harus lebih dari "
                "sama dengan 140 SKS. SKS sekarang: {}".format(
                    self.QUICK_STATUS.sks_taken))
        if self.QUICK_STATUS.sum_D > 14:
            err.append(
                "Jumlah SKS untuk mata kuliah yang D atau D+ harus "
                "kurang dari 14 SKS. "
                "\nPerhatikan untuk mata kuliah:\n" +
                ", ".join(self.QUICK_STATUS.low_courses_names))

        return [RuleResult('Ujian skripsi',
                           'Tidak dapat dilaksanakan semester ini',
                           e) for e in err]

    def rule_potensi_predikat_kelulusan(self) -> RuleResult:
        current_sem = datetime.now().year - self.TRANSCRIPT.year_registered + (
                datetime.now().month >= 8)
        ipk = self.TRANSCRIPT.current_ipk
        c_exists = False
        d_exists = False

        for course in self.TRANSCRIPT.course_taken:
            if course.grade[0] == 'C':
                c_exists = True
            elif course.grade[0] == 'D':
                d_exists = True

        verdict = 'Lulus'

        if ipk > 3.50 and not c_exists and not d_exists and current_sem <= 10:
            verdict = 'Dengan Pujian'
        elif ipk > 3.00 and not d_exists and current_sem <= 10:
            verdict = 'Sangat memuaskan'
        elif ipk > 2.76:
            verdict = 'Memuaskan'

        c_ext = '. Terdapat mata kuliah lebih rendah dari B' if c_exists else ''
        d_ext = '. Terdapat mata kuliah lebih rendah dari D' if d_exists else ''
        return RuleResult('Potensi predikat kelulusan', verdict,
                          'IPK: {}{}{}'.format(ipk, c_ext, d_ext))

    def get_current_semester(self) -> int:
        return datetime.now().year - self.TRANSCRIPT.year_registered + (
                datetime.now().month >= 8)

    def rule_evaluasi(self) -> List[RuleResult]:
        current_sem = self.get_current_semester()

        err = []

        if current_sem == 5:
            if self.QUICK_STATUS.sks_taken < 45:
                err.append(
                    "Jumlah SKS yang telah selesai harus lebih dari "
                    "sama dengan 45 SKS. SKS sekarang: {}".format(
                        self.QUICK_STATUS.sks_taken))
            if self.QUICK_STATUS.sum_D > 4:
                err.append(
                    "Jumlah SKS untuk mata kuliah yang D atau D+ "
                    "harus kurang dari sama dengan 4 SKS. "
                    "\nPerhatikan untuk mata kuliah:\n" +
                    ", ".join(self.QUICK_STATUS.low_courses_names))
        elif current_sem == 7:
            if self.QUICK_STATUS.sks_taken < 90:
                err.append(
                    "Jumlah SKS yang telah selesai harus lebih dari "
                    "sama dengan 90 SKS. SKS sekarang: {}".format(
                        self.QUICK_STATUS.sks_taken))
            if self.QUICK_STATUS.sum_D > 9:
                err.append(
                    "Jumlah SKS untuk mata kuliah yang D atau D+ "
                    "harus kurang dari sama dengan 9 SKS. "
                    "\nPerhatikan untuk mata kuliah:\n" +
                    ", ".join(self.QUICK_STATUS.low_courses_names))
        elif current_sem == 15:
            pass

        return [
            RuleResult('Evaluasi', 'Terkendala evaluasi akhir tahun',
                       e) for e in err]

    def rule_batas_waktu_studi(self) -> RuleResult:
        current_sem = self.get_current_semester()
        return RuleResult('Batas waktu studi',
                          'Batas waktu studi: {} semester'.format(
                              14 - current_sem),
                          '')

    def check_all_rules(self) -> List[RuleResult]:
        self.CHECK_RESULT.clear()

        for ev in self.rule_pertemuan_tiap_semester():
            self.CHECK_RESULT.append(ev)

        for ev in self.rule_hadir_kuliah():
            self.CHECK_RESULT.append(ev)

        self.CHECK_RESULT.append(self.rule_penyelesaian_studi())

        for ev in self.rule_special_course():
            self.CHECK_RESULT.append(ev)

        for ev in self.rule_skripsi():
            self.CHECK_RESULT.append(ev)

        for ev in self.rule_ujian_skripsi():
            self.CHECK_RESULT.append(ev)

        self.CHECK_RESULT.append(
            self.rule_potensi_predikat_kelulusan())

        for ev in self.rule_evaluasi():
            self.CHECK_RESULT.append(ev)

        self.CHECK_RESULT.append(self.rule_batas_waktu_studi())

        return self.CHECK_RESULT
