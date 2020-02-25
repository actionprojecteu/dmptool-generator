import logging
import time
import subprocess
from pymongo import MongoClient;
from bson import ObjectId

from generator import Generator;


class MyService():
    def __init__(self, *args, **kwargs):

        logging.basicConfig(handlers=[logging.StreamHandler(),logging.FileHandler("debug.log")], format='%(asctime)s %(levelname)-8s %(message)s',level=logging.DEBUG,datefmt='%Y-%m-%d %H:%M:%S')
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
                    try:
                        logging.info("Handling dmp "+str(dmp['_id']));
                        generator = Generator(dmp);
                        generator.generate();
                        logging.info("Updating database");
                        docbook_name= "docbook-"+str(dmp['_id'])+".xml";
                        docx_name = "docbook-"+str(dmp['_id'])+".docx";
                        logging.info("Generating DOCX file:"+docx_name);
                        cp = subprocess.run(["pandoc","--from","docbook","--to","docx","--output","/app/resources/"+docx_name,docbook_name]);
                        return_code_docx = cp.returncode;
                        if (return_code_docx==0):
                            logging.info("DOCX file generated");
                        else:
                            logging.info("Problem to generate DOCX file:"+str(return_code_docx));
                            logging.info("Message:" + str(cp.stderr));
                        pdf_name = "docbook-"+str(dmp['_id'])+".pdf";
                        logging.info("Generating PDF file:" + pdf_name);
                        cp = subprocess.run(["pandoc", "--from","docbook","--to","latex", "--output","/app/resources/"+pdf_name,docbook_name]);
                        return_code_pdf = cp.returncode;
                        if (return_code_pdf==0):
                            logging.info("PDF file generated");
                        else:
                            logging.info("Problem to generate PDF file:"+str(return_code_pdf));
                            logging.info("Message:" + str(cp.stderr));

                        if (return_code_docx!=0 or return_code_pdf!=0):
                            self.db.tasks.update({"_id": ObjectId(task['_id'])},{"$set":{"status": "error"}});
                        else:
                            self.db.tasks.update({"_id": ObjectId(task['_id'])},{"$set":{"status":"done","url_docx":docx_name,"url_pdf":pdf_name}});
                    except ValueError:
                        logging.error("Error to parse float ");
                        self.db.tasks.update({"_id": ObjectId(task['_id'])}, {"$set": {"status": "error"}});
                else:
                    logging.info("No DMP found with this id")


            time.sleep(5)

if __name__ == '__main__':

    service = MyService()
    service.run();