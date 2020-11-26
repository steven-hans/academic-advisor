import json
from typing import List, Dict

import requests
from requests import Response

from attendanceparser.attendance import Attendance


def get_request(student_id=str) -> Response:
    try:
        response = requests.get(
            'http://informatika.untan.ac.id/biodata/score/api.php?'
            'type=GETSELECTED&nim=' + student_id)
        return response
    except requests.exceptions.RequestException:
        return None


def get_attendance(student_id=str) -> List[Dict[str, str]]:
    response = get_request(student_id)

    if response is not None:
        return json.loads(response.content.decode('UTF-8'))
    else:
        return [{'kodemk': 'server nya', 'namamk': 'down lagi',
                 'jumlah_kehadiran': '0', 'total_pertemuan': '1'}]


def parse_attendance(student_id=str) -> List[Attendance]:
    return [
        Attendance(a['kodemk'], a['namamk'], a['jumlah_kehadiran'],
                   a['total_pertemuan'])
        for a in get_attendance(student_id)]
