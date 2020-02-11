import logging
import time
from pymongo import MongoClient;
from bson import ObjectId

from generator import Generator;


class MyService():
    def __init__(self, *args, **kwargs):

        logging.basicConfig(handlers=[logging.StreamHandler(),logging.FileHandler("debug.log")], level=logging.DEBUG)
        self.client = MongoClient('mongodb://mongodb:27017/');
        self.db = self.client.dmptool;
        logging.info("Initiating mongo database");

    def run(self):
        while True:
            logging.info("I'm working...");
            tasks = self.db.tasks.find({"status":"pending"});
            for task in tasks:
                logging.info("Processing task with dmp id:"+str(task['dmp']))
                json_query = {"_id": ObjectId(task['dmp'])};
                logging.info("Looking for DMP "+str(json_query));
                dmp = self.db.dmps.find_one(json_query);
                if (dmp!=None):
                    logging.info("Handling dmp "+str(dmp['_id']));
                    generator = Generator(dmp);
                    generator.generate();
                    logging.info("Updating database");
                    docx_name = "docbook-"+str(dmp['_id'])+".docx";
                    pdf_name = "docbook-"+str(dmp['_id'])+".pdf";
                    self.db.tasks.update({"dmp":str(dmp['_id'])},{"status":"done","url_docx":docx_name,"url_pdf":pdf_name});
                else:
                    logging.info("No DMP found with this id")


            time.sleep(5)

if __name__ == '__main__':

    service = MyService()
    service.run();