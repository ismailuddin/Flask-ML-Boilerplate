import math
from app import app, db
from flask import render_template, make_response, jsonify, Response
from flask import request, url_for, redirect
from flask_login import login_required, current_user
from app.models.users import User
from app.ml.predict import despatch_job, run_prediction


@app.route("/")
def index():
    return render_template("homepage.html", page_title="Home")


@app.route("/jobs/create")
@login_required
def create_job():
    return render_template("job_create.html", page_title="Create new job")


@app.route("/jobs/run")
@login_required
def run_job():
    job = despatch_job(
        func=run_prediction, user=current_user, fargs=("cool", "task")
    )
    if job is not None:
        return make_response(jsonify({
            "task_id": job.scheduler_id
        }), 202)
    else:
        return Response(response="Failed to create job", status=500)


@app.route("/jobs/status/<job_id>")
def get_job_status(job_id: str):
    job = run_prediction.AsyncResult(job_id)
    if job.state == "PENDING":
        response = {
            "state": job.state,
            "current": 0,
            "total": 1,
            "status": "Pending..."
        }
    elif job.state != "FAILURE":
        # Job is running
        response = {
            "state": job.state,
            "current": job.info.get("current", 0),
            "total": job.info.get("total", 1),
            "status": job.info.get("status", "")
        }
        if "result" in job.info:
            response["result"] = job.info["result"]
    else:
        # Job has failed
        response = {
            "state": job.state,
            "current": 1,
            "total": 1,
            "status": str(job.info)
        }
    return jsonify(response)


def build_pagination(current_page: int, total_pages: int, n_of_buttons: int) -> list:
    inner_buttons = []
    n, N = 1, total_pages
    d = math.floor((n_of_buttons - 2) / 2)
    if current_page <= (n + (n_of_buttons - 2)):
        for i in range(1, n_of_buttons - 1):
            inner_buttons.append(n + i)
    elif current_page > (n + (n_of_buttons - 2)) and (current_page + d) < N:
        d = -1 * d
        _page = current_page + d
        for i in range(n_of_buttons - 2):
            inner_buttons.append(_page)
            _page += 1
    elif current_page >= N - (n_of_buttons - 2):
        for i in range(1, n_of_buttons - 1)[::-1]:
            inner_buttons.append(N - i)
    return inner_buttons


@app.route("/account/jobs")
@login_required
def user_jobs():
    page = request.args.get('page', default=1, type=int)
    entries = request.args.get('entries', default=10, type=int)
    jobs = current_user.get_jobs().paginate(
        page, entries, False
    )
    # Redirect if requested page is past number of page for specified
    # entries per page
    if page > jobs.pages:
        return redirect(url_for("user_jobs") + "?" + "entries={}".format(entries))

    pagination_buttons = build_pagination(page, jobs.pages, 5)

    button_list = []
    for page_number in pagination_buttons:
        button_list.append({
            "number": page_number,
            "url": url_for("user_jobs", page=page_number, entries=entries)
        })

    first_url = url_for("user_jobs", page=1, entries=entries)
    prev_url = url_for("user_jobs", page=jobs.prev_num, entries=entries
                       ) if jobs.has_prev else ""
    next_url = url_for(
        "user_jobs", page=jobs.next_num, entries=entries
    ) if jobs.has_next else ""
    last_url = url_for("user_jobs", page=jobs.pages, entries=entries)


    return render_template(
        "user/jobs.html",
        jobs=jobs.items,
        page=page,
        first_url=first_url,
        prev_url=prev_url,
        next_url=next_url,
        last_url=last_url,
        total_pages=jobs.pages,
        button_list=button_list,
        entries=entries
    )
