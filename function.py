from flask import Flask, request, jsonify, Response
from pymongo import MongoClient
from bson.objectid import ObjectId

class MyAPI:
    def __init__(self, data):

        # the Mongo Client
        self.client = MongoClient("mongodb://to be updated")

        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        # read the database
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data):
        # TO Do: add the write function
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def post(self):
        job = mongo.db.jobs
        job_name = request.json['job_name']
        job_description = request.json['job_description']
        job_creater = request.json['job_creater']
        job_address = request.json['job_address']
        job_id = job.insert({'job_name': job_name,
                             'job_description': job_description,
                             'job_creater': job_creater,
                             'job_address': job_address})

        new_job = job.find_one({'_id': job_id})
        output = {'job_name': new_job['job_name'],
                  'job_description': new_job['job_description'],
                  'job_creater': new_job['job_creater'],
                  'job_address': new_job['job_address']
                  }
        return jsonify({'result': output})

    def delete(self, job_id):
        mongo.db.jobs.remove({'id': ObjectId(job_id)})
        return jsonify({'result': 'job has been deleted'})

    def search_by_jobid(self, job_id):
        output = mongo.db.jobs.find({"job_id": job_id})
        return jsonify({'result': output})

    def search_by_jobname(self, job_name):
        output = mongo.db.jobs.find({"job_name": job_name})
        return jsonify({'result': output})

    def query_my_created_job(self, user_id):
        output = mongo.db.jobs.find({"job_creater": user_id})
        return jsonify({'result': output})

    def apply(self, job_id):
        job = mongo.db.jobs
        user_name = request.json["uesr_name"]
        job.update({}, {$set:{'job_receiver': user_name}})
        return jsonify({'result': 'apply successfully!'})