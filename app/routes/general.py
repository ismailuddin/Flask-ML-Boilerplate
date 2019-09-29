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
    
    prev_url = url_for("user_jobs", page=jobs.prev_num, entries=entries
    ) if jobs.has_prev else None
    next_url = url_for(
        "user_jobs", page=jobs.next_num, entries=entries
    ) if jobs.has_next else None
    last_url = url_for("user_jobs", page=jobs.pages, entries=entries)

    page_1 = url_for("user_jobs", page=1, entries=entries)
    page_2 = url_for("user_jobs", page=2, entries=entries)
    # if next_url is not None:
    #     next_url += "&entries={}".format(entries)
    # if prev_url is not None:
    #     prev_url += "&entries={}".format(entries)

    return render_template(
        "user/jobs.html",
        jobs=jobs.items,
        page=page,
        next_url=next_url,
        prev_url=prev_url,
        page_1=page_1,
        page_2=page_2,
        last_url=last_url,
        entries=entries
    )
