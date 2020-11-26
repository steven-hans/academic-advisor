import re
from typing import List, Tuple, Union

from flask import flash, redirect, url_for
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
from werkzeug.wrappers.response import Response

from transcriptparser.course import Course
from transcriptparser.transcript import Transcript

COUNT_LIST = ['INF-55201-101',
              'INF-55201-102',
              'INF-55201-103',
              'INF-55201-104',
              'MKWU1', 'MKWU2',
              'UMG-55201-101',
              'UMG-55201-102',
              'UMG-55201-103',
              'INF-55201-105',
              'INF-55201-106',
              'INF-55201-107',
              'INF-55201-108',
              'INF-55201-109',
              'MKWU3',
              'MKWU4',
              'UMG-55201-104',
              'UMG-55201-105',
              'INF-55201-201',
              'INF-55201-202',
              'INF-55201-203',
              'INF-55201-204',
              'INF-55201-205',
              'INF-55201-206',
              'INF-55201-207',
              'INF-55201-208',
              'INF-55201-209',
              'INF-55201-210',
              'INF-55201-211',
              'INF-55201-212',
              'INF-55201-213',
              'INF-55201-214',
              'INF-55201-301',
              'INF-55201-302',
              'INF-55201-303',
              'INF-55201-304',
              'INF-55201-305',
              'INF-55201-306',
              'INF-55201-307',
              'INF-55201-308',
              'INF-55201-309',
              'INF-55201-310',
              'INF-55201-311',
              'INF-55201-312',
              'INF-55201-313',
              'INF-55201-314',
              'INF-55201-315',
              'INF-55201-316',
              'INF-55201-401',
              'INF-55201-402',
              'INF-55201-403',
              'INF55201500',
              'INF-55201-500',
              'INF55201501',
              'INF-55201-501',
              'INF55201502',
              'INF-55201-502',
              'INF55201503',
              'INF-55201-503',
              'INF55201504',
              'INF-55201-504',
              'INF55201505',
              'INF-55201-505',
              'INF55201506',
              'INF-55201-506',
              'INF55201507',
              'INF-55201-507',
              'INF55201508',
              'INF-55201-508',
              'INF55201509',
              'INF-55201-509',
              'INF55201510',
              'INF-55201-510',
              'INF55201511',
              'INF-55201-511',
              'INF55201512',
              'INF-55201-512',
              'INF55201513',
              'INF-55201-513',
              'INF55201514',
              'INF-55201-514',
              'INF55201515',
              'INF-55201-515',
              'INF55201516',
              'INF-55201-516',
              'INF55201517',
              'INF-55201-517',
              'INF55201518',
              'INF-55201-518',
              'INF55201519',
              'INF-55201-519',
              'INF55201520',
              'INF-55201-520',
              'INF55201521',
              'INF-55201-521',
              'INF55201522',
              'INF-55201-522',
              'INF55201523',
              'INF-55201-523',
              'INF55201524',
              'INF-55201-524',
              'INF55201525',
              'INF-55201-525',
              'INF55201526',
              'INF-55201-526',
              'INF55201527',
              'INF-55201-527',
              'INF55201528',
              'INF-55201-528',
              'INF55201529',
              'INF-55201-529',
              'INF55201530',
              'INF-55201-530',
              'INF55201531',
              'INF-55201-531',
              'INF55201532',
              'INF-55201-532',
              'INF55201533',
              'INF-55201-533',
              'INF55201534',
              'INF-55201-534',
              'INF55201535',
              'INF-55201-535',
              'INF55201536',
              'INF-55201-536',
              'INF55201537',
              'INF-55201-537',
              'INF55201538',
              'INF-55201-538',
              'INF55201539',
              'INF-55201-539',
              'INF55201540',
              'INF-55201-540',
              'INF55201541',
              'INF-55201-541',
              'INF55201542',
              'INF-55201-542',
              'INF55201543',
              'INF-55201-543',
              'INF55201544',
              'INF-55201-544',
              'INF55201545',
              'INF-55201-545',
              'INF55201546',
              'INF-55201-546',
              'INF55201547',
              'INF-55201-547',
              'INF55201548',
              'INF-55201-548',
              'INF55201549',
              'INF-55201-549',
              'INF55201550',
              'INF-55201-550',
              'INF-55201-404']

ipk_sks_pattern = re.compile(r": (\d.\d+) / (\d+) SKS")
year_pattern = re.compile(r": (\d{4})")
course_pattern = re.compile(
    r"(INF-55201-\d+)|(UMG-55201-\d+)|(MKWU\d)")
course_sks_pattern = re.compile(r"(\d+) SKS")
grade_pattern = re.compile(r"[A-E][-+]?")

student_id_pattern = re.compile(r"[A-Z]\d{10,}")


def compile_courses(course_codes: List[str], sks_counts: List[int],
                    grades: List[str]) -> List[Course]:
    # we assume that the course code, the sks count, and the grades
    # are laid in order we also assume that because of this,
    # the size of all lists must be the same, because each existing
    # course code has to have an sks count and grade.
    try:
        assert (len(course_codes) == len(sks_counts) == len(grades))
        return [Course(course_codes[i], sks_counts[i], grades[i]) for
                i in range(len(course_codes))]
    except AssertionError:
        print(
            'Length of lists are not the same (course, sks, grade):',
            len(course_codes), len(sks_counts), len(grades))
        return []


def get_pdf_text(filename: str) -> Union[str, Response]:
    try:
        text = extract_text(filename).replace('-\n', '-')
        return text
    except PDFSyntaxError:
        flash(
            'File tidak dapat dianalisis. '
            'Pastikan file adalah pdf transkrip SIAKAD.')
        return redirect(url_for('index'))


def get_ipk_sks(text: str) -> Tuple[float, int]:
    res = ipk_sks_pattern.findall(text)
    if len(res) == 0:
        return 0.00, 0
    else:
        return float(res[0][0]), int(res[0][1])


def get_year(text: str) -> int:
    res = year_pattern.findall(text)
    if len(res) == 0:
        return 2018
    else:
        return int(res[0])


def count_sort(course_set: set) -> List[str]:
    return [c for c in COUNT_LIST if c in course_set]


def get_course_codes(text: str) -> List[str]:
    res = course_pattern.findall(text)
    if len(res) == 0:
        return []
    else:
        course_set = set([x[0] if len(x[0]) > 0 else x[1] if len(
            x[1]) > 0 else x[2] for x in res])
        # ensure course is sorted according to predetermined
        # ordering using counting sort. complexity should be O(n)
        sorted_list = count_sort(course_set)
        return sorted_list


def get_course_sks(text: str) -> List[int]:
    res = course_sks_pattern.findall(text)
    return [int(sks) for sks in res][1:]
    # ignore the very first element. The first element
    # is the total of SKS.


def get_grades(text: str) -> List[str]:
    filtered_text = " ".join(
        [line for line in text.splitlines() if 0 < len(line) < 3])
    res = grade_pattern.findall(filtered_text)
    return res


def get_student_id(text: str) -> str:
    res = student_id_pattern.findall(text)
    if len(res) == 0:
        return 'A0000000000'
    else:
        return res[0]


def extract_transcript(filename: str) -> Union[Transcript, Response]:
    text = get_pdf_text(filename)

    if type(text) == Response:
        return text

    year_registered = get_year(text)
    student_id = get_student_id(text)
    ipk_sks = get_ipk_sks(text)
    ipk = ipk_sks[0]
    total_sks = ipk_sks[1]
    course_taken = compile_courses(get_course_codes(text),
                                   get_course_sks(text),
                                   get_grades(text))
    extracted_transcript = Transcript(year_registered, student_id,
                                      ipk, total_sks, course_taken)

    return extracted_transcript
