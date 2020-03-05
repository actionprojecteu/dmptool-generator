from pymongo import MongoClient;
import xml.etree.ElementTree as ET
import logging

import json;
import pprint;

class Generator:
    def __init__(self, dmp):
        self.dmp = dmp;
        #self.client = MongoClient('mongodb://localhost:27017/');
        #self.db = self.client.dmptool;
        #self.xmlFile = ET.parse('template.xml').getroot()

    def generate(self):
        #json_query = {"name":self.id};
        #dmp = self.db.dmptool.find_one(json_query);
        #print(dmp);

        article = ET.Element("article",xmlns="http://docbook.org/ns/docbook");

        info = ET.SubElement(article, "info");
        if (self.dmp['project']!=None):
            title = ET.SubElement(info,"title").text = "Data Management Plan: Project "+self.dmp['project'];
        else:
            title = ET.SubElement(info, "title").text = "Data Management Plan";
        author = ET.SubElement(info, "author");
        personname = ET.SubElement(author,"personname");
        firstname = ET.SubElement(personname,"user");

        publisher = ET.SubElement(info,"publisher");
        publishername = ET.SubElement(publisher,"publishername").text = "ACTION Project";
        pubdate = ET.SubElement(publisher,"pubdate").text = "2020";

        section_executive = ET.SubElement(article,"section",id="executive");
        title_executive = ET.SubElement(section_executive,"title").text = "Executive Summary"
        ET.SubElement(section_executive,"para").text="This document serves as the data management plan for the ACTION project pilots. It consists of a "\
        "number of individual data management plans, covering the pilot projects that form part of the "\
        "ACTION consortium, as well as additional data management plans for the datasets to be gathered "\
        "and maintained as part of the work package activities in WP3 (Open Call), WP5 (Socio-Technical "\
        "Toolkit) and WP6 (Impact Assessment). At the time of production of this DMP, no further datasets "\
        "are foreseen. Should additional datasets be required or produced as part of ACTION, updated "\
        "versions of this DMP will be produced and submitted as necessary."

        section_body = ET.SubElement(article,"section", id="body");
        ET.SubElement(section_body,"title").text="Data Management Plan";

        section_data_summary = ET.SubElement(section_body,"sect1");
        ET.SubElement(section_data_summary,"title").text="Data Summary";

        ET.SubElement(section_data_summary,"strong").text="What is the purpose of the data collection/generation and its relation to the objectives of the project?"
        if (self.dmp['purpose']!=None):
            ET.SubElement(section_data_summary,"para").text=self.dmp['purpose']
        else:
            ET.SubElement(section_data_summary, "para").text = "No purpose defined"

        ET.SubElement(section_data_summary,
                      "strong").text = "What types and formats of data will the project generate/collect?"
        if(self.dmp['description']):
            ET.SubElement(section_data_summary, "para").text = self.dmp['description']
        else:
            ET.SubElement(section_data_summary, "para").text = "No description defined"

        ET.SubElement(section_data_summary,
                      "strong").text = "Will you re-use any existing data and how?"

        if (self.dmp['reuse'] == 'Yes'):
            ET.SubElement(section_data_summary, "para").text = "In this project, we re-use data that can be downloaded from the following url "+self.dmp['reuse_url'];
        elif (self.dmp['reuse'] == 'No'):
            ET.SubElement(section_data_summary, "para").text = "We do not re-use data in this project"
        else:
            ET.SubElement(section_data_summary, "para").text = "At this moment, we are unaware of the using of any kind of data from external projects"

        text_string = "At this moment, we are not generating data in our project"

        if(self.dmp['use_data'] == 'Yes'):
            text_string = "At this moment, we are generating data in our project"
            if (self.dmp['use_data_url'] != None):
                text_string = text_string + " and it can be found here "+self.dmp['use_data_url'];
            else:
                text_string = text_string + " but it is not public in any url";

        ET.SubElement(section_data_summary, "strong").text = "What is the origin of the data?"
        ET.SubElement(section_data_summary,"para").text = text_string


        ET.SubElement(section_data_summary, "strong").text = "What is the expected size of the data?"

        if (self.dmp['size_datasets']!=None):
            ET.SubElement(section_data_summary,"para").text = "The estimated size for the dataset is "+self.dmp['size_datasets']
        else:
            ET.SubElement(section_data_summary, "para").text = "We haven´t a clear estimation of the amount of data generated in the project."

        ET.SubElement(section_data_summary,"strong").text = "To whom might it be useful ('data utility')?"

        if (self.dmp['interest'] == 'Yes'):
            ET.SubElement(section_data_summary,"para").text = "We have identified the following community that could be interested in using our data: "+self.dmp['interest'];
        else:
            ET.SubElement(section_data_summary,"para").text = "As far as I know, We have not identified any community interested in our data";



        section_fair_data = ET.SubElement(section_body, "sect1");
        ET.SubElement(section_fair_data,"title").text="FAIR data";

        section_data_findable = ET.SubElement(section_fair_data,"sect2");
        ET.SubElement(section_data_findable,"title").text="Making data findable, including provisions for metadata";
        ET.SubElement(section_data_findable,"para").text="A Digital Object Identifier (DOI) will be generated using Zenodo to make it findable. This dataset will be findable from our Zenodo Community (http://zenodo.org/communities/actionprojecteu) and from our Data Portal";

        ET.SubElement(section_data_findable,"strong").text="Will search keywords be provided that optimize possibilities for re-use?";
        if ('keywords' in self.dmp):
            ET.SubElement(section_data_findable,"para").text="We have identified the following keywords:"+self.dmp['keywords'];
        else:
            ET.SubElement(section_data_findable,"para").text="We have not identified keywords to optimize our dataset for re-using it"

        ET.SubElement(section_data_findable,"strong").text="Do you provide clear version numbers?";
        ET.SubElement(section_data_findable,"para").text="For this pilot, we will produce a unique data set that will be periodically updated. So we will use versioning for the dataset. Platforms like Zenodo could provide us the data versioning, so that we do not have to track versions ourselves."

        ET.SubElement(section_data_findable, "strong").text = "What metadata will be created? In case metadata standards do not exist in your discipline, please outline what type of metadata will be created and how. We will also include metadata defined";
        ET.SubElement(section_data_findable, "para").text = "We will also include metadata defined by CKAN. This includes (title, description,tags,license, source, version, author email and some another custom fields)";

        section_data_accesible = ET.SubElement(section_fair_data,"sect2");
        ET.SubElement(section_data_accesible,"title").text="Making data openly accessible";

        ET.SubElement(section_data_accesible,"strong").text="Which data produced and/or used in the project will be made openly available as the default? If certain datasets cannot be shared (or need to be shared under restrictions), explain why, clearly separating legal and contractual reasons from voluntary restrictions.";
        if (self.dmp["sharing"] == 'Yes'):
            ET.SubElement(section_data_accesible,"para").text="All the datasets will be available by default.";
        elif (self.dmp["sharing"] == 'No'):
            if (self.dmp["embargo"] == 'Yes'):
                ET.SubElement(section_data_accesible, "para").text = "Datasets in our project will not be openly published and sharing. Nevertheless, after the date "+self.dmp["embargo_date"]+" will be openly available.";
            else:
                ET.SubElement(section_data_accesible, "para").text = "Datasets in our project will not be openly published and sharing. This is it because "+self.dmp['reason'];
        else:
            ET.SubElement(section_data_accesible, "para").text = "We are not sure if our dataset will be available to citizens.";

        ET.SubElement(section_data_accesible, "strong").text = "Note that in multi-beneficiary projects it is also possible for specific beneficiaries to keep their data closed if relevantprovisions are made in the consortium agreement and are in line with the reasons for opting out.";
        ET.SubElement(section_data_accesible,"para").text="There is no provision to keep the data closed and no specific beneficiaries are foreseen.";

        ET.SubElement(section_data_accesible,"strong").text="How will the data be made accessible (e.g. by deposition in a repository)?"
        ET.SubElement(section_data_accesible,"para").text="We will set up a web infrastructure and upload periodically our data to a public repository (i.e. Zenodo). Our data Portal (based on CKAN) will be used for searching but not physically store the data, rather it will keep a link to the public repository."

        ET.SubElement(section_data_accesible,"strong").text="What methods or software tools are needed to access the data?";
        ET.SubElement(section_data_accesible,"para").text="An ordinary web browser will be enough to download data from our data portal or public repository. Datasets will be in CSV. Optionally, the user could use our search facility of our data portal.";

        ET.SubElement(section_data_accesible,"strong").text="Is documentation about the software needed to access the data included?";
        ET.SubElement(section_data_accesible,"para").text="The API of Zenodo or our data portal can be used to consult the different datasets deposit in these repositories. Plus, there are open software tools available to process datasets";

        ET.SubElement(section_data_accesible,"strong").text="Is it possible to include the relevant software (e.g. in open source code)?";
        ET.SubElement(section_data_accesible,"para").text="Examples querying and using data will be uploaded to a public repository (i.e GitHub).";

        ET.SubElement(section_data_accesible,"strong").text="Where will the data and associated metadata, documentation and code be deposited? Preference should be given to certified repositories which support open access where possible.";
        ET.SubElement(section_data_accesible,"para").text="Data will be stored in a public repository, our data portal providing search facilities. Documentation will be available on our website (http://actionproject.eu). The code will be uploaded to our public repository in Github. (https://github.com/actionprojecteu)";

        ET.SubElement(section_data_accesible,"strong").text="Have you explored appropriate arrangements with the identified repository?";
        ET.SubElement(section_data_accesible,"para").text="No.";

        ET.SubElement(section_data_accesible,"strong").text="If there are restrictions on use, how will access be provided?";

        sharing_text = "";
        if (self.dmp["sharing"]=='Yes'):
            sharing_text="There will be no access restrictions.";
        elif (self.dmp["sharing"]=='No'):
            if (self.dmp["embargo"]=='Yes'):
                sharing_text="Data have an embargo period. After "+self.dmp["embargo_date"]+", the restriction will be wiped out from the data.";
            else:
                sharing_text="Data can not be accessed. Please contact with the owner for requesting permission. Data are licensed with "+self.dmp["license"];
                if ('conditions' in self.dmp):
                    sharing_text = sharing_text + ". See the terms and conditions: "+self.dmp["conditions"];

        ET.SubElement(section_data_accesible,"para").text=sharing_text;

        sharing_text = "";
        ET.SubElement(section_data_accesible,"strong").text="Is there a need for a data access committee?";
        if (self.dmp["sharing"] == 'Yes'):
            sharing_text = "No";
        elif (self.dmp["sharing"]=='No'):
            if (self.dmp["embargo"]=='Yes'):
                sharing_text="Data will be available after date  "+self.dmp["embargo_date"]+".";
            else:
                sharing_text="Data can not be accessed. Please contact with the owner for requesting permission. Data are licensed with "+self.dmp["license"];
                if ('conditions' in self.dmp):
                    sharing_text = sharing_text+". See the terms and conditions: "+self.dmp["conditions"];
        ET.SubElement(section_data_accesible,"para").text=sharing_text;

        ET.SubElement(section_data_accesible,"strong").text="Are there well described conditions for access (i.e. a machine readable license)?";
        license_text = "The license of the data is "+self.dmp["license"];
        if (self.dmp["license"]=='Others'):
            license_text = license_text + "The terms and conditions of the license are "+self.dmp["conditions"];
        ET.SubElement(section_data_accesible,"para").text=license_text;

        ET.SubElement(section_data_accesible,"strong").text="How will the identity of the person accessing the data be ascertained?";
        if (self.dmp["sharing"]=='Yes'):
            ET.SubElement(section_data_accesible,"para").text="There is no need to identify the person to access and to download the data selected";
        else:
            ET.SubElement(section_data_accesible,"para").text="It is not contemplated to implement an authenticate process to access to the data.";

        section_data_interoperable = ET.SubElement(section_fair_data,"sect2");
        ET.SubElement(section_data_interoperable,"title").text="Making data interoperable";

        ET.SubElement(section_data_interoperable,"strong").text="Are the data produced in the project interoperable, that is allowing data exchange and re-use between researchers, institutions, organisations, countries, etc. (i.e. adhering to standards for formats, as much as possible compliant with available (open) software applications, and in particular facilitating re-combinations with different datasets from different origins)?";
        if (self.dmp["vocabulary"]=='Yes'):
            ET.SubElement(section_data_interoperable,"para").text="This data used an specific vocabulary to make the data interoprable.";
        elif (self.dmp["vocabulary"]=='No'):
            ET.SubElement(section_data_interoperable,"para").text="No";

        ET.SubElement(section_data_interoperable,"strong").text="What data and metadata vocabularies, standards or methodologies will you follow to make your data interoperable?";
        if (self.dmp["vocabulary"]=='Yes'):
            ET.SubElement(section_data_interoperable,"para").text=self.dmp["vocabulary_text"];
        elif (self.dmp["vocabulary"]=='No'):
            ET.SubElement(section_data_interoperable, "para").text = "None.";

        ET.SubElement(section_data_interoperable,"strong").text = "Will you be using standard vocabularies for all data types present in your data set, to allow inter-disciplinary interoperability?";
        if (self.dmp["vocabulary"] == 'Yes'):
            ET.SubElement(section_data_interoperable, "para").text = self.dmp["vocabulary_text"];
        elif (self.dmp["vocabulary"] == 'No'):
            ET.SubElement(section_data_interoperable, "para").text = "No.";

        ET.SubElement(section_data_interoperable,"strong").text = "In case it is unavoidable that you use uncommon or generate project specific ontologies or vocabularies, will you provide mappings to more commonly used ontologies?";
        if (self.dmp["vocabulary"] == 'Yes'):
            ET.SubElement(section_data_interoperable,"para").text = self.dmp["vocabulary_text"];
        elif (self.dmp["vocabulary"] == 'No'):
            ET.SubElement(section_data_interoperable, "para").text = "We are not planning to use ontologies or vocabularies to describe the data generated.";

        section_data_reuse = ET.SubElement(section_fair_data,"sect2");
        ET.SubElement(section_data_reuse,"title").text="Increase data re-use (through clarifying licences)";

        ET.SubElement(section_data_reuse,"strong").text="How will the data be licensed to permit the widest re-use possible?";
        if (self.dmp["license"]!='Others'):
            ET.SubElement(section_data_reuse,"para").text="The data have been published with the following license";
        else:
            ET.SubElement(section_data_reuse,"para").text="The data have been published with an specific license. Terms and conditions are: "+self.dmp["conditions"];

        sharing_text=""
        ET.SubElement(section_data_reuse,"strong").text="When will the data be made available for reuse? If an embargo is sought to give time to publish or seek patents, specify why and how long this will apply, bearing in mind that research data should be made available as soon as possible.";
        if (self.dmp["sharing"] == 'Yes'):
            sharing_text = "Data will be available as soon as the dataset is generated with the periodicity configured by the coordinator";
        elif (self.dmp["sharing"] == 'No'):
            if (self.dmp["embargo"] == 'Yes'):
                sharing_text = "Data will be available after date  " + self.dmp["embargo_date"] + ".";
            else:
                sharing_text = "Data can not be accessed. Please contact with the owner for requesting permission. Data are licensed with " +self.dmp["license"];
                if ('conditions' in self.dmp):
                    sharing_text = sharing_text+ ". See the terms and conditions: " + self.dmp["conditions"];
        ET.SubElement(section_data_reuse,"para").text=sharing_text;

        ET.SubElement(section_data_reuse,"strong").text="Are the data produced and/or used in the project useable by third parties, in particular after the end of the project? If the re-use of some data is restricted, explain why.";
        interest_text = "";
        if (self.dmp["interest"]=='Yes'):
            interest_text= "We have identified this community interesting in using our datasets."+self.dmp["community"];
        else:
            interest_text= "At this moment, we have not identified any community interesting in using our dataset";


        if (self.dmp["sharing"] == 'Yes'):
                    interest_text = interest_text + "Data will be available as soon as the dataset is generated with the periodicity configured by the coordinator";
        elif (self.dmp["sharing"] == 'No'):
            if (self.dmp["embargo"] == 'Yes'):
                interest_text = interest_text + "Data will be available after date  " + self.dmp["embargo_date"] + ".";
            else:
                interest_text = interest_text + "Data can not be accessed. Please contact with the owner for requesting permission. Data are licensed with " +self.dmp["license"];
                if ('conditions' in self.dmp):
                    interest_text=interest_text+". See the terms and conditions: " + self.dmp["conditions"];

        ET.SubElement(section_data_reuse,"para").text=interest_text;

        ET.SubElement(section_data_reuse,"strong").text="How long is it intended that the data remains re-usable?";
        ET.SubElement(section_data_reuse,"para").text="Reusability of data is tied to the actual data sources to be catalogued. Update campaigns should be carried out to keep our data up to date.";

        ET.SubElement(section_data_reuse,"strong").text="Are data quality assurance processes described?";
        if (self.dmp["quality"]=="Yes"):
            ET.SubElement(section_data_reuse,"para").text=self.dmp["quality_text"];
        else:
            ET.SubElement(section_data_reuse,"para").text="Not yet defined at this stage.";

        section_allocation_resources = ET.SubElement(section_body,"sect1");
        ET.SubElement(section_allocation_resources,"title").text="Allocation of resources";

        ET.SubElement(section_allocation_resources,"strong").text="What are the costs for making data FAIR in your project?";
        ET.SubElement(section_allocation_resources,"para").text="The cost of making our data FAIR in public repositories like Zenodo is free. However, there is a cost on the data infrastructure to be held in the UPM";

        ET.SubElement(section_allocation_resources,"strong").text="How will these be covered? Note that costs related to open access to research data are eligible as part of the Horizon 2020 grant (if compliant with the Grant Agreement conditions).";
        ET.SubElement(section_allocation_resources,"para").text="Data infrastructure cost during the project will be covered by the grant.";

        ET.SubElement(section_allocation_resources,"strong").text="Who will be responsible for data management in your project?";
        ET.SubElement(section_allocation_resources,"para").text="The data management process is managed by UPM (Universidad Politécnica de Madrid), as leader of WP4 (Digital infrastructure for citizen science)";

        ET.SubElement(section_allocation_resources,"strong").text="Are the resources for long term preservation discussed (costs and potential value, who decides and how what data will be kept and for how long)?";
        ET.SubElement(section_allocation_resources,"para").text="Regarding costs, we are seriously considering Zenodo as the platform of choice for preserving our data, since this is an open platform. Our data should be readily available once the quality check by our backend application (or by user validation) is made.";

        section_data_security = ET.SubElement(section_body,"sect1");
        ET.SubElement(section_data_security,"title").text="Data security";

        ET.SubElement(section_data_security,"strong").text="What provisions are in place for data security (including data recovery as well as secure storage and transfer of sensitive data)?"
        ET.SubElement(section_data_security,"para").text="With the exception of data uploaded to public repositories, are hosted in UPM's servers. Only personal authorized can access these servers and periodical backups are being done.";

        ET.SubElement(section_data_security,"strong").text="Is the data safely stored in certified repositories for long term preservation and curation?";
        ET.SubElement(section_data_security,"para").text="With the exception of data uploaded to public repositories, are hosted in UPM's servers. Only personal authorized can access these servers and periodical backups are being done.";

        section_ethical_aspects = ET.SubElement(section_body,"sect1");
        ET.SubElement(section_ethical_aspects,"title").text="Ethical aspects";

        ET.SubElement(section_ethical_aspects,"strong").text="Are there any ethical or legal issues that can have an impact on data sharing? These can also be discussed in the context of the ethics review. If relevant, include references to ethics deliverables and ethics chapter in the Description of the Action (DoA).";
        ethical_text ="";
        if (self.dmp["personal"]=='Yes'):
            ethical_text = "In our case, personal data is used in ut public dataset. To publish it, we will follow this anonymization process."+self.dmp["personal_text"];
        else:
            ethical_text = "Personal information about users will not be published in our public repositories.";
        if (self.dmp["protected_geolocation"]=='Yes'):
            ethical_text = ethical_text +"Plus, a obfuscation process is applied to avoid the location of sensitive species."+self.dmp["protected_geolocation_text"];

        section_others = ET.SubElement(section_body,"sect1");
        ET.SubElement(section_others,"title").text="Other issues";
        ET.SubElement(section_others,"strong").text="Do you make use of other national/funder/sectorial/departmental procedures for data management? If yes, which ones?";
        ET.SubElement(section_others,"para").text="None identified so far";

        tree = ET.ElementTree(article);

        fileName = "docbook-"+str(self.dmp['_id'])+".xml"
        logging.info("Generating file "+fileName);

        tree.write(fileName);


            #dmp = self.db.dmptool.find_one({"name":"test1"});



if __name__ == "__main__":
    dmp = Generator("test1");
    dmp.generate();
