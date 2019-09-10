from datetime import datetime
from enum import Enum
from app import db
from sqlalchemy import exc
import logging

dbLogger = logging.getLogger("databaseLogger")


class JobStatus(Enum):
    PENDING = 100
    IN_PROGRESS = 200
    SUCCEEDED = 300
    FAILED = 400


class Job(db.Model):
    """Database model for 'Job' table which holds a list of all
    submitted jobs.
    """
    id = db.Column(db.Integer, primary_key=True)
    scheduler_id = db.Column(db.String(128), index=True)
    name = db.Column(db.String(128))
    status = db.Column(db.Enum(JobStatus), default=JobStatus.PENDING)
    result = db.Column(db.String(2048))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Float, default=0)
    date_created = db.Column(
        db.DateTime, index=True, default=datetime.utcnow()
    )
    date_modified = db.Column(
        db.DateTime, index=True, default=datetime.utcnow()
    )

    def update_scheduler_id(self, scheduler_id: str) -> bool:
        self.scheduler_id = scheduler_id
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False
        return True

    @staticmethod
    def get_job(job_id: str) -> 'Job':
        return Job.query.get(job_id)

    @staticmethod
    def get_job_status(job_id: str) -> int:
        return Job.query.get(job_id).status

    @staticmethod
    def update_job_status(
        status: JobStatus, scheduler_id: str = None, job_id: int = None
    ) -> bool:
        if scheduler_id is not None:
            job = Job.query.filter_by(scheduler_id=scheduler_id).first()
        else:
            job = Job.query.get(job_id)
        if job is not None:
            job.status = status
        else:
            dbLogger.warning(
                "Could not find requested job by ID {} / scheduler ID {}".format(
                    job_id, scheduler_id
                )
            )
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False
        return True

    @staticmethod
    def update_job_duration(job_id: int, duration: float) -> bool:
        job = Job.query.get(job_id)
        if job is not None:
            job.duration = duration
        else:
            dbLogger.warning(
                "Could not find requested job by ID: {}".format(
                    job_id
                )
            )
        try:
            db.session.commit()
        except exc.SQLAlchemyError as error:
            dbLogger.error(error)
            db.session.rollback()
            return False
        return True

    @staticmethod
    def set_job_failed(scheduler_id: str, result: str) -> bool:
        job = Job.query.filter_by(scheduler_id=scheduler_id).first()
        if job is not None:
            job.status = JobStatus.FAILED
            job.result = result
            job.end_time = datetime.utcnow()
            job.duration = (job.end_time - job.start_time).total_seconds()
        else:
            dbLogger.warning(
                "Could not find requested job by scheduler ID: {}".format(
                    scheduler_id
                )
            )
        try:
            db.session.commit()
        except exc.SQLAlchemyError as error:
            dbLogger.error(error)
            db.session.rollback()
            return False
        return True

    @staticmethod
    def update_job_timing(
        job_id: int, start_time: datetime = None, end_time: datetime = None
    ) -> bool:
        job = Job.query.get(job_id)
        if job is not None:
            if start_time is not None and end_time is not None:
                dbLogger.error(
                    "Start and end time trying to be set simulatenously"
                )
                return False
            if start_time is not None:
                job.start_time = start_time
            elif end_time is not None:
                job.end_time = end_time
        else:
            dbLogger.warning(
                "Could not find requested job by ID: {}".format(
                    job_id
                )
            )
        try:
            db.session.commit()
        except exc.SQLAlchemyError as error:
            dbLogger.error(error)
            db.session.rollback()
            return False
        return True

    @classmethod
    def create_job(job_id: str, **kwargs) -> 'Job':
        job = Job(
            name=kwargs["name"],
            user_id=kwargs["user_id"],
            status=kwargs["status"]
        )
        try:
            db.session.add(job)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return None
        return job
