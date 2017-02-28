from collections import OrderedDict

from app.queries import get_users, get_username_by_user_id
from flask import Blueprint
from flask import render_template, request, url_for, redirect
from flask.ext.login import login_required, current_user

from app.performance_summary import s
from app.views import admin_required
from flask_table import Table, Col, LinkCol

from producers.StarLims import StarLimsApi
from producers.eqaAPI import EqaAPI


summary = Blueprint('summary', __name__, template_folder='templates')


@summary.route('/search', methods=['GET', 'POST'])
@login_required
@admin_required
def search():
    if request.method == 'POST':
        staff = request.form["staff"]
        if staff == "":
            return render_template('search.html', list=list, modifier="OOOoooops!",
                                   message="You Must Enter a Search Term!")
        s = StarLimsApi()
        all_staff = []
        samples_by_user = s.get_samples_by_user(staff)
        reports_by_user = s.get_report_samples_by_user(staff)
        if "FAIL" not in samples_by_user[0]:
            for i in samples_by_user:
                all_staff.append(i["FULLNAME"])
        if "FAIL" not in reports_by_user[0]:
            for i in reports_by_user:
                all_staff.append(i["FULLNAME"])

        unique_staff = set(all_staff)
        if len(unique_staff) > 0:
            return search_list(unique_staff)
        else:
            return render_template('search.html', list=list, modifier="Hey!", message="\"" + staff + "\" Not Found in Starlims! Try Another Search...")


@summary.route('/summary', methods=['GET', 'POST'])
@login_required
@admin_required
def staff_summary():
    staff_name = request.args["staff"]
    s = StarLimsApi()
    e = EqaAPI()
    all_samples = []
    starlims_samples = s.get_samples_by_user(staff_name)
    starlims_reports = s.get_report_samples_by_user(staff_name)
    for i in starlims_samples:
        all_samples.append(i["FOLDERNO"])
    for i in starlims_reports:
        all_samples.append(i["FOLDERNO"])
    unique_samples = set(all_samples)
    results=[]
    for sample in unique_samples:
        print sample
        eqa_result = e.get_scheme_by_snumber(sample)[0]
        if "FAIL" not in eqa_result:
            events = []
            for i in starlims_samples:
                if i["FOLDERNO"] == eqa_result["SampleStarlimsRef"]:
                    event = {}
                    event["STEP"] = i["STEPCODE"]
                    event["TYPE"] = i["EVENTTYPE"]
                    events.append(event)
            for i in starlims_reports:
                if i["FOLDERNO"] == eqa_result["SampleStarlimsRef"]:
                    event = {}
                    event["TYPE"] = i["EVENTCOMMENT"]
                    event["STEP"] = i["EVENTSTATUS"]
                    events.append(event)
            eqa_result["EVENTS"]=events
            results.append(eqa_result)

    result_count=len(results)
    sample_count=len(unique_samples)


    return render_template('staff_record.html',name=staff_name,sample_count=sample_count,result_count = result_count,results = results)

@summary.route('/search/list', methods=['GET', 'POST'])
@login_required
@admin_required
def search_list(list=None):
    if list is not None:
        return render_template('staff_list.html',list=list)








