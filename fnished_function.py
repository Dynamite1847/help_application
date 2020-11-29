from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb://COEN6313:admin@35.183.26.186:27017/admin')
db = client.users
db_jobs = client.jobs


def delete(self, job_id):
    db_jobs.jobs.delete_one({'_id': ObjectId(job_id)})


def update(seld,job_id):
    db_jobs.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": {'email': 'dynamite1864@163.com'}})
