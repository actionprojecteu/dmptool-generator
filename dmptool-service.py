import logging
import time
from pymongo import MongoClient;

from generator import Generator;


class MyService():
    def __init__(self, *args, **kwargs):

        logging.basicConfig(handlers=[logging.StreamHandler(),logging.FileHandler("debug.log")], level=logging.DEBUG)
        self.client = MongoClient('mongodb://localhost:27017/');
        self.db = self.client.dmptool;
        logging.info("Initiating mongo database");

    def run(self):
        while True:
            logging.info("I'm working...");
            tasks = self.db.tasks.find({"status":"pending"});
            for task in tasks:
                logging.info("Processing task ")
                json_query = {"name": task['dmp']};
                dmp = self.db.dmptool.find_one(json_query);
                if (dmp!=None):
                    logging.info("Handling dmp "+str(dmp['_id']));
                    generator = Generator(dmp);
                    generator.generate();
                    logging.info("Updating database");
                    self.db.tasks.update({"dmp":str(dmp['_id'])},{"status":"done"});


            time.sleep(5)

if __name__ == '__main__':

    service = MyService()
    service.run();