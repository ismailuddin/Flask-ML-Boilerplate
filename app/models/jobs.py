from datetime import datetime
from app import db
from sqlalchemy import exc


class Job(db.Model):
    """Database model for 'Job' table which holds a list of all
    submitted jobs.

    Column status (int):
        100: Pending
        200: In progress
        300: Succeeded
        400: Failed
    """
    id = db.Column(db.Integer, primary_key=True)
    scheduler_id = db.Column(db.String(128), index=True)
    name = db.Column(db.String(128))
    status = db.Column(db.Integer, default=100)
    result = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date_created = db.Column(db.DateTime, index=True,
                             default=datetime.utcnow())
    date_modified = db.Column(db.DateTime, index=True,
                              default=datetime.utcnow())

    def update_status(self, status: int) -> bool:
        self.status = status
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False
        return True

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
        scheduler_id: str = None, job_id: int = None, status: int = 100
    ) -> bool:
        if scheduler_id is not None:
            job = Job.query.filter_by(scheduler_id=scheduler_id).first()
        else:
            job = Job.query.get(job_id)
        if job is not None:
            job.status = status
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
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
