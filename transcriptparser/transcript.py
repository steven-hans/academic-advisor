from typing import List, Dict

from transcriptparser.course import Course


class Transcript:
    COURSE_SKS: Dict[str, int] = {}

    def __init__(self,
                 year_registered: int,
                 student_id: str,
                 current_ipk: float,
                 sks_taken: int,
                 course_taken: List[Course]):
        self.year_registered = year_registered
        self.student_id = student_id
        self.current_ipk = current_ipk
        self.sks_taken = sks_taken
        self.course_taken = course_taken
        self.build_course_sks_mapping()

    def build_course_sks_mapping(self):
        for c in self.course_taken:
            self.COURSE_SKS[c.course_code] = c.sks_count
