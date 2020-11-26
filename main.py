from typing import List, Dict, Union, Tuple

from flask import Flask, render_template, request
from werkzeug.wrappers.response import Response

import rulechecker
from attendanceparser import parser as aparser
from attendanceparser.attendance import Attendance
from ruleresult import RuleResult
from transcriptparser import parser as tparser
from transcriptparser.transcript import Transcript
from intent import predict

app = Flask(__name__)
app.secret_key = b'_897ug5984j79584759g7349579037039g5790g54j780j795jj07j9u425ujJ(*(*))(#%)(_(*_)J*_)(#J*(J()*(WGU3498 '
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024

PackedRule = Dict[str, List[Tuple[str, str, int]]]


def pack_rule_result(
        result: Union[List[RuleResult], RuleResult]) -> PackedRule:
    if type(result) == RuleResult:
        # note that type is RuleResult
        result: List[RuleResult] = [result]

    res = {}
    for k, r in enumerate(result):
        if r is not None:
            if r.name not in res:
                res[r.name] = []

            res[r.name].append((r.error, r.resolution, k))

    return res


@app.route('/')
def index():
    return render_template('mainpage.html')


@app.route('/analysis', methods=['POST'])
def analysis():
    f = request.files['transcript_file']
    f.save('test.pdf')

    transcript: Transcript = tparser.extract_transcript('test.pdf')

    if type(transcript) == Response:
        return transcript

    attendances: List[Attendance] = aparser.parse_attendance(
        transcript.student_id)

    checker: rulechecker.RuleChecker = rulechecker.RuleChecker(
        transcript, attendances)

    res: PackedRule = []
    temp_rule_result: List[RuleResult] = []

    prompts = request.form['questions'].lower().strip().split('\n')[:5]

    if prompts[0] == '':
        temp_rule_result: Union[
            List[RuleResult], RuleResult] = checker.check_all_rules()
    else:
        for line in prompts:
            # using eval could be a potential security risk.
            # but i won't bother since it's more concise compared with
            # rewriting and matching each function rule one by one
            result: Union[
                List[RuleResult], RuleResult] = eval('checker.'+
                                                     predict(line)+
                                                     '()')
            if type(result) == RuleResult:
                temp_rule_result.append(result)
            else:
                temp_rule_result += result

    res = pack_rule_result(temp_rule_result)
    return render_template('analysisresult.html', R=res)
