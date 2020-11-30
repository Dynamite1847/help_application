from uuid import UUID

from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb://COEN6313:admin@35.183.26.186:27017/admin')
db = client.users
db_jobs = client.jobs


def delete(self, job_id):
    db_jobs.jobs.delete_one({'_id': ObjectId(job_id)})


def apply_for_job(user_uid, job_id):
    db_jobs.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": {'employeeUid': user_uid}})


