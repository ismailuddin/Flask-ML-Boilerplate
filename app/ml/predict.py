import time
from datetime import datetime
from typing import Callable
import random
from app import celery
from celery.contrib import rdb
from app.models.jobs import Job, JobStatus


class MLJob(celery.Task):
    abstract = True

    def on_success(self, retval, task_id, args, kwargs):
        Job.update_job_status(scheduler_id=task_id, status=JobStatus.SUCCEEDED)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        Job.set_job_failed(scheduler_id=task_id, result=einfo.exception)


def despatch_job(
    func: Callable, user: int, fargs: tuple = (), fkwargs: dict = {}
) -> Job:
    job = Job.create_job(
        user_id=user.id,
        name="adaf",
        status=JobStatus.PENDING
    )
    if job is not None:
        fkwargs["job_id"] = job.id
        job_handler = func.apply_async(args=fargs, kwargs=fkwargs)
        if job.update_scheduler_id(job_handler.id):
            return job
        else:
            return None
    else:
        return None


@celery.task(bind=True, base=MLJob)
def run_prediction(self, arg1: str, arg2: str, job_id: str = None):
    runs = random.randrange(1, 5)
    start = time.time()
    Job.update_job_timing(start_time=datetime.utcnow(), job_id=job_id)
    for i in range(runs):
        Job.update_job_status(job_id=job_id, status=JobStatus.IN_PROGRESS)
        if i == 2:
            raise ValueError("Some weird error")
        self.update_state(
            state="IN_PROGRESS",
            meta={
                "current": i,
                "total": runs,
                "message": "Still running... {}, {}".format(arg1, arg2)
            }
        )
        time.sleep(1)
    end = time.time()
    Job.update_job_timing(end_time=datetime.utcnow(), job_id=job_id)
    Job.update_job_duration(job_id=job_id, duration=(end - start))
    return {
        "current": i,
        "total": runs,
        "message": "Job completed!",
        "result": 4636
    }
