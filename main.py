#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import jinja2
import webapp2
from google.appengine.api import rdbms
from datetime import datetime
from pytz import timezone
import pytz

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

_INSTANCE_NAME="prinya-th-2013:prinya-db"

class MainHandler(webapp2.RequestHandler):
	def get(self):

		conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    		cursor = conn.cursor()
		cursor.execute('SELECT course_id,course_code,course_name,credit_lecture,credit_lab,credit_learning,status,regiscourse_id FROM course natural join regiscourse')

		conn2=rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    		cursor2 = conn2.cursor()
		cursor2.execute('SELECT sum(capacity),sum(enroll),regiscourse_id FROM section group by regiscourse_id')

		# conn3=rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
  #   		cursor3 = conn3.cursor()
		# cursor3.execute('SELECT course_id,status FROM regiscourse')

		templates = {

			'course' : cursor.fetchall(),
			'enroll' : cursor2.fetchall(),
			# 'status' : cursor3.fetchall(),

			}

		template = JINJA_ENVIRONMENT.get_template('course.html')
		self.response.write(template.render(templates))

	
	

class Toggle(webapp2.RequestHandler):
	def get(self):

		value=self.request.get('course_id');
		value=int(value)
		
				

		conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    		cursor = conn.cursor()
    		sql1="SELECT status FROM regiscourse WHERE course_id= '%d'"%value
    		cursor.execute(sql1);
    		result=cursor.fetchall()

    		for row in result:
			if row[0]==1:
				sql2="UPDATE regiscourse set status=0 where course_id='%d'"%value

				cursor.execute(sql2);
				

			else:
				sql3="UPDATE regiscourse set status=1 where course_id='%d'"%value
				cursor.execute(sql3);

				
		conn.commit()
		conn.close()
		self.redirect("/")


class search(webapp2.RequestHandler):
  	def get(self):

  		course_code=self.request.get('keyword');
  		year=self.request.get('year');
  		
  		semester=self.request.get('semester');
  		check_code=0
  		check_fac=0
  		check_dep=0
  		check_year=0
  		check_sem=0
  		allcheck=0
  		key_year=""
  		key_sem=""
  		code=""

  		if year=="":
  			check_year=0
  		else:
  			check_year=1
  			key_year="year="+year

  		if semester=="":
  			check_sem=0
  		else:
  			check_sem=1
  			key_sem="semester="+semester

  		if course_code == "":
  			check_code=0

  		else:
  			check_code=1
  			code="course_code like '%"+course_code+"%' "




  		data_faculity_id=self.request.get('faculity');
  		data_faculity_id=str(data_faculity_id)
  		data_faculity=""
		if data_faculity_id=="1":
			data_faculity = "faculity='Engineering'";
		elif data_faculity_id=="2":
			data_faculity = "faculity='Information Technology'";
		elif data_faculity_id=="3":
			data_faculity = "faculity='Business Administration'";
		elif data_faculity_id=="4":
			data_faculity = "faculity='Language'";

		if data_faculity_id =="":
			check_fac=0
		else:
			check_fac=1
  		
  		
	
		data_department=self.request.get('department');
		data_department=str(data_department)
		data_department_full=""

		if data_department=="1":
			data_department_full="department='Information Technology'"
		elif data_department=="2":
			data_department_full="department='Multimedia Technology'"
		elif data_department=="3":
			data_department_full="department='Business Information Technology'"
		elif data_department=="4":
			data_department_full="department='Accountancy'"
		elif data_department=="5":
			data_department_full="department='Industrial Management'"
		elif data_department=="6":
			data_department_full="department='International Business Management'"
		elif data_department=="7":
			data_department_full="department='Japanese Businees Administration'"
		elif data_department=="8":
			data_department_full="department='Computer Engineering'"
		elif data_department=="9":
			data_department_full="department='Production Engineering'"
		elif data_department=="10":
			data_department_full="department='Automotive Engineering'"
		elif data_department=="11":
			data_department_full="department='Electrical Engineering'"
		elif data_department=="12":
			data_department_full="department='Industrial Engineering'"
		elif data_department=="13":
			data_department_full="department='Language'"

		if data_department=="":
			check_dep=0
		else:
			check_dep=1

		

		where_code=" "
		a=" and "

		

		if check_code == 1:
			if check_code == 1:
				where_code+=code
			if check_year == 1:
				where_code+=a
				where_code+=key_year
			if check_sem == 1:
				where_code+=a
				where_code+=key_sem
			if check_fac == 1:
				where_code+=a
				where_code+=data_faculity
			if check_dep==1:
				where_code+=a
				where_code+=data_department_full
		elif check_year == 1:
			if check_year == 1:
				where_code+=key_year
			if check_sem == 1:
				where_code+=a
				where_code+=key_sem
			if check_fac == 1:
				where_code+=a
				where_code+=data_faculity
			if check_dep==1:
				where_code+=a
				where_code+=data_department_full
		elif check_sem == 1:
			if check_sem == 1:
				where_code+=key_sem
			if check_fac == 1:
				where_code+=a
				where_code+=data_faculity
			if check_dep==1:
				where_code+=a
				where_code+=data_department_full
		elif check_fac == 1:
			if check_fac == 1:
				where_code+=data_faculity
			if check_dep==1:
				where_code+=a
				where_code+=data_department_full
		elif check_dep==1:
			if check_dep==1:
				where_code+=data_department_full
		else:
			where_code="course_id = 0"



		# self.response.write(where_code)


                
      	
	

		conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    		cursor = conn.cursor()
    		sql="SELECT course_id,course_code,course_name,credit_lecture,credit_lab,credit_learning,status,regiscourse_id FROM course natural join regiscourse where %s "%(where_code)
                # sql="SELECT course_id,course_code,course_name,credit_lecture,credit_lab,credit_learning,status,regiscourse_id FROM course natural join regiscourse where course_code like '%s'"%(percent)
		cursor.execute(sql)
		conn.commit()
		

		conn2=rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    		cursor2 = conn2.cursor()
		cursor2.execute('SELECT sum(capacity),sum(enroll),regiscourse_id FROM section group by regiscourse_id')
		conn2.commit()


		
	

		templates = {

			'course' : cursor.fetchall(),
			'enroll' : cursor2.fetchall(),
			

			}

		template = JINJA_ENVIRONMENT.get_template('course.html')
		self.response.write(template.render(templates))

		conn.close()
		conn2.close()

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class CreateHandler(webapp2.RequestHandler):
    def get(self):


        conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor = conn.cursor()
        cursor.execute("select * from course")
        
        templates = {
    		'course' : cursor.fetchall(),
    	}
    	get_template = JINJA_ENVIRONMENT.get_template('course_create.html')
    	self.response.write(get_template.render(templates));

    	

class InsertHandler(webapp2.RequestHandler):
    def post(self):

        utc = pytz.utc
        date_object = datetime.today()
        utc_dt = utc.localize(date_object);
        bkk_tz = timezone("Asia/Bangkok");
        bkk_dt = bkk_tz.normalize(utc_dt.astimezone(bkk_tz))
        time_insert = bkk_dt.strftime("%H:%M:%S")

        data_code = self.request.get('course_code')

        

        conn4 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor4 = conn4.cursor()
        cursor4.execute("select course_code from course")
       
        
        count=0
        for row in cursor4.fetchall():
            if row[0] in data_code:
                count=1
        

        if count==1:
            self.redirect("/Error")

        else:
            data_course_name = self.request.get('course_name')
            data_course_description = self.request.get('course_description')
            data_faculity_id = self.request.get('faculity')
            data_faculity = ""
            # data_total_capacity = self.request.get('total_capacity')
            data_department = self.request.get('department')
            data_credit_lecture = self.request.get('credit_lecture')
            data_credit_lab = self.request.get('credit_lab')
            data_credit_learning = self.request.get('credit_learning')
            data_credit_type = self.request.get('credit_type')
            data_credit_type2 = self.request.get('credit_type2')
            data_prerequisite = self.request.get('prerequisite')
            data_prerequisite=int(data_prerequisite)
            

            if data_faculity_id=="1":
                data_faculity = "Engineering";
            elif data_faculity_id=="2":
                data_faculity = "Information Technology";
            elif data_faculity_id=="3":
                data_faculity = "Business";
            elif data_faculity_id=="4":
                data_faculity = "Language";

            data_credit_type=int(data_credit_type)
            data_credit_type2=int(data_credit_type2)

            price = [0,1350,1350,1500,1500,1750,1350,1000,1500,1500,1350,1000,1000,1500]
            price1 = price[data_credit_type]
            price2 = price[data_credit_type2]

            # if data_credit_type in (1,2,6,10):
            #     price1=1350
            # elif data_credit_type in (3,4,8,9,13):
            #     price1=1500
            # elif data_credit_type==5:
            #     price1=1750
            # elif data_credit_type in (7,11,12):
            #     price1=3000

            # if data_credit_type2 in (1,2,6,10):
            #     price2=1350
            # elif data_credit_type2 in (3,4,8,9,13):
            #     price2=1500
            # elif data_credit_type2==5:
            #     price2=1750
            # elif data_credit_type2 in (7,11,12):
            #     price2=3000

            data_credit_lecture = int(data_credit_lecture)
            data_credit_lab = int(data_credit_lab)
            data_department = int(data_department)

            price1 =int(price1)
            price2 =int(price2)
            total=0
            total=(price1*data_credit_lecture)+(price2*data_credit_lab)

            data_department_full=""

            if data_department==1:
                data_department_full="Information Technology"
            elif data_department==2:
                data_department_full="Multimedia Technology"
            elif data_department==3:
                data_department_full="Business Information Technology"
            elif data_department==4:
                data_department_full="Accountancy"
            elif data_department==5:
                data_department_full="Industrial Management"
            elif data_department==6:
                data_department_full="International Business Management"
            elif data_department==7:
                data_department_full="Japanese Businees Administration"
            elif data_department==8:
                data_department_full="Computer Engineering"
            elif data_department==9:
                data_department_full="Production Engineering"
            elif data_department==10:
                data_department_full="Automotive Engineering"
            elif data_department==11:
                data_department_full="Electrical Engineering"
            elif data_department==12:
                data_department_full="Industrial Engineering"
            elif data_department==13:
                data_department_full="Language"

                    
            total=int(total)
            data_faculity_id=int(data_faculity_id)
            data_credit_lecture=int(data_credit_lecture)
            data_credit_lab=int(data_credit_lab)
            data_credit_learning=int(data_credit_learning)

            # data_credit_lecture = str(data_credit_lecture)
            # data_credit_lab = str(data_credit_lab)

            # price1 =str(price1)
            # price2 =str(price2)

            
            conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
            cursor = conn.cursor()
            cursor.execute("insert into course \
                (course_code,course_name,course_description,credit_lecture,credit_lab,credit_learning,type_credit_lecture,type_credit_lab,price,department,faculity,faculity_id) VALUES ('%s','%s','%s','%d','%d','%d','%d','%d','%d','%s','%s','%d')"%
                (data_code,data_course_name,data_course_description,data_credit_lecture,data_credit_lab,data_credit_learning,data_credit_type,data_credit_type2,total,data_department_full,data_faculity,data_faculity_id))
            conn.commit()

            conn2 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
            cursor2 = conn2.cursor()
            cursor2.execute("insert into regiscourse\
                (course_id,semester,year,status) values((select course_id from course where course_code = '%s'),1,2556,1)"%
                (data_code))        
            conn2.commit()

            conn3 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
            cursor3 = conn3.cursor()
            cursor3.execute("insert into log\
                (staff_id,course_id,day,time,type) values(2,(select course_id from course where course_code = '%s'),CURDATE(),'%s',1)"%
                (data_code,time_insert))        
            conn3.commit()

            if data_prerequisite!=0:                
                conn4 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
                cursor4 = conn4.cursor()
                cursor4.execute("insert into prerequsite_course\
                    (course_id,type,prerequsite_id) values((select course_id from course where course_code = '%s'),1,'%s')"%
                    (data_code,data_prerequisite))        
                conn4.commit()

            # self.response.write(total)
            # self.response.write(price1)
            # self.response.write(price2)
            conn.close()
            conn2.close()
            conn3.close()
            conn4.close()
            self.redirect("/")


class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        templates = {
            # 'course' : cursor.fetchall(),
        }
        get_template = JINJA_ENVIRONMENT.get_template('error.html')
        self.response.write(get_template.render(templates));
        # self.redirect('/')


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


class Notification(webapp2.RequestHandler):
	def get(self):

		conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
	    	cursor = conn.cursor()
	    	sql = ("""select log_id,course_name,day,time,l.type,l.staff_id,firstname,email 
					from log l join staff s 
					on l.staff_id=s.staff_id 
					join course c
					on c.course_id=l.course_id
					order by log_id desc""")
		cursor.execute(sql)

		templates = {

					'log' : cursor.fetchall(),
					}

		template = JINJA_ENVIRONMENT.get_template('notification.html')
		self.response.write(template.render(templates))
		
		conn.commit();	
		conn.close();

  	
    		
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
class DetailCourseHandler(webapp2.RequestHandler):
    def get(self):
    	course_id = self.request.get('course_code');
    	# course_id = "BIS-101"

    	conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    	cursor = conn.cursor()
        sql="SELECT * FROM course WHERE course_code = '%s'"%(course_id)
    	cursor.execute(sql);

        conn2 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor2 = conn2.cursor()
        sql2="SELECT co.course_code FROM course co,prerequsite_course pre\
            WHERE prerequsite_id=co.course_id AND pre.course_id=\
            (SELECT course_id FROM course WHERE course_code='%s')"%(course_id)
        cursor2.execute(sql2);
        pre_code=""
        for row in cursor2.fetchall():
            pre_code=row[0]

        templates = {
    		'course' : cursor.fetchall(),
            'prerequisite_code' : pre_code,
    	}
    	get_template = JINJA_ENVIRONMENT.get_template('course_detail.html')
    	self.response.write(get_template.render(templates));
        conn.close();
        conn2.close();

class ModifyCourseHandler(webapp2.RequestHandler):
    def get(self):
    	course_id = self.request.get('course_id');

    	conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    	cursor = conn.cursor()
        sql="SELECT * FROM course WHERE course_code = '%s'"%(course_id)
        cursor.execute(sql);

        conn2 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor2 = conn2.cursor()
        sql2="SELECT course_id,course_code from course where course_code not like '%s'"%(course_id)
        cursor2.execute(sql2);

        conn3 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor3 = conn3.cursor()
        sql3="SELECT section_id,section_number,UPPER(CONCAT(CONCAT(firstname,' '),lastname)),enroll,capacity\
            FROM section sec JOIN staff st ON teacher_id=staff_id\
            WHERE regiscourse_id=(SELECT regiscourse_id FROM regiscourse WHERE course_id=\
            (SELECT course_id from course where course_code='%s')) ORDER BY section_number"%(course_id)
        cursor3.execute(sql3);

        conn4 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor4 = conn4.cursor()
        sql4="SELECT co.course_id,co.course_code FROM course co,prerequsite_course pre\
            WHERE prerequsite_id=co.course_id AND pre.course_id=\
            (SELECT course_id FROM course WHERE course_code='%s')"%(course_id)
        # sql4="SELECT prerequisite , CASE prerequisite WHEN '0' THEN '- NONE - ' \
        #     ELSE (SELECT course_code FROM course WHERE course_id=\
        #     (SELECT prerequisite FROM course WHERE course_code='%s'))\
        #     END FROM course WHERE  course_code='%s'"%(course_id,course_id)
        cursor4.execute(sql4);
        pre_id=""
        pre_code=""
        for row in cursor4.fetchall():
            pre_id=row[0]
            pre_code=row[1]

        templates = {
    		'course' : cursor.fetchall(),
            'course2' : cursor2.fetchall(),
            'course3' : cursor3.fetchall(),
            'course_id' : course_id,
            'prerequisite_id' : pre_id,
            'prerequisite_code' : pre_code,
    	}
    	get_template = JINJA_ENVIRONMENT.get_template('course_modify.html')
    	self.response.write(get_template.render(templates));
        conn.close();
        conn2.close();
        conn3.close();
        conn4.close();


class UpdateCourseHandler(webapp2.RequestHandler):
    def post(self):
    	course_id = self.request.get('course_id');
        course_name = self.request.get('course_name');
        prerequisite = self.request.get('prerequisite');
        if prerequisite!="":
            prerequisite=int(prerequisite)
        course_description = self.request.get('course_description');
    	credit_lecture = self.request.get('credit_lecture');
        credit_lecture=int(credit_lecture)
        credit_lab = self.request.get('credit_lab');
        credit_lab=int(credit_lab)
        credit_learning = self.request.get('credit_learning');
        credit_learning=int(credit_learning)
    	faculity = self.request.get('faculity');
        department = self.request.get('department');

    	conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    	cursor = conn.cursor()
        sql="UPDATE course SET course_code = '%s' , \
        course_name = '%s' , course_description = '%s' , \
         credit_lecture = '%d' , credit_lab = '%d' , \
         credit_learning = '%d' , department = '%s' , \
         faculity = '%s' WHERE course_code = '%s'"%(course_id,course_name,course_description,credit_lecture,credit_lab,credit_learning,department,faculity,course_id)
    	cursor.execute(sql);
        conn.commit();
              
        conn3 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor3 = conn3.cursor()
        sql3="DELETE FROM prerequsite_course\
                    WHERE course_id=(SELECT course_id FROM course WHERE course_code = '%s')"%(course_id)
        cursor3.execute(sql3)        
        conn3.commit()
        
        if prerequisite!="":
            conn4 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
            cursor4 = conn4.cursor()
            sql4="INSERT INTO prerequsite_course\
                        (course_id,type,prerequsite_id) VALUES((SELECT course_id FROM course WHERE course_code = '%s'),1,'%s')"%(course_id,prerequisite)
            cursor4.execute(sql4)        
            conn4.commit()
            conn4.close();


        

        utc = pytz.utc
        date_object = datetime.today()
        utc_dt = utc.localize(date_object);
        bkk_tz = timezone("Asia/Bangkok");
        bkk_dt = bkk_tz.normalize(utc_dt.astimezone(bkk_tz))
        time_insert = bkk_dt.strftime("%H:%M:%S")

        conn2 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor2 = conn2.cursor()
        sql2="INSERT INTO log (staff_id,course_id,day,time,type)\
            VALUES(3,(SELECT course_id FROM course WHERE course_code = '%s'),CURDATE(),'%s',4)"%(course_id,time_insert)
        cursor2.execute(sql2)        
        conn2.commit()
        conn2.close();
        conn.close();
        conn3.close();
        
        self.redirect("/ModifyCourse?course_id="+course_id)

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class AddSectionHandler(webapp2.RequestHandler):
    def get(self):
        
        course_id=self.request.get('course_id');

        templates = {
            'course_id' : course_id,
        }
        get_template = JINJA_ENVIRONMENT.get_template('section.html')
        self.response.write(get_template.render(templates));

class InsSectionHandler(webapp2.RequestHandler):
    def post(self):

    	course_id=self.request.get('course_id');
        section_number=self.request.get('section_number');
        section_number=int(section_number)
        teacher=self.request.get('teacher');
        capacity=self.request.get('capacity');
        capacity=int(capacity)

        # conncheck = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        # cursorcheck = conncheck.cursor()
        # sqlcheck="INSERT INTO section (regiscourse_id,section_number,teacher_id,capacity,enroll) \
        #     VALUES ((SELECT course_id FROM course where course_code = '%s'),'%d',\
        #     (SELECT staff_id FROM staff WHERE firstname = '%s'),'%d','0')"%(course_id,section_number,teacher,capacity)
        # cursorcheck.execute(sqlcheck);
        # conncheck.commit();
        # conncheck.close();


        conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor = conn.cursor()
        sql="INSERT INTO section (regiscourse_id,section_number,teacher_id,capacity,enroll) \
            VALUES ((SELECT course_id FROM course where course_code = '%s'),'%d',\
            (SELECT staff_id FROM staff WHERE firstname = '%s'),'%d','0')"%(course_id,section_number,teacher,capacity)
        cursor.execute(sql);
        conn.commit();
        conn.close();

        utc = pytz.utc
        date_object = datetime.today()
        utc_dt = utc.localize(date_object);
        bkk_tz = timezone("Asia/Bangkok");
        bkk_dt = bkk_tz.normalize(utc_dt.astimezone(bkk_tz))
        time_insert = bkk_dt.strftime("%H:%M:%S")

        conn2 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor2 = conn2.cursor()
        sql2="INSERT INTO log (staff_id,course_id,day,time,type)\
            VALUES(3,(SELECT course_id FROM course WHERE course_code = '%s'),CURDATE(),'%s',2)"%(course_id,time_insert)
        cursor2.execute(sql2)        
        conn2.commit()
        conn2.close();

        self.redirect("/ModifyCourse?course_id="+course_id)

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class DetailSectionHandler(webapp2.RequestHandler):
    def get(self):
        
        course_id=self.request.get('course_id');
        section_id=self.request.get('section_id');
        section_id=int(section_id)
        section_number=self.request.get('section_number');
        section_number=int(section_number)

        conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor = conn.cursor()

        sql="SELECT section_number,firstname,capacity\
            FROM section sec JOIN staff st ON teacher_id=staff_id\
            WHERE section_id='%d' AND section_number='%d'"%(section_id,section_number)
        cursor.execute(sql);

        conn2 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor2 = conn2.cursor()
        sql2="SELECT sectime_id, CASE day WHEN '1' THEN 'Sunday'\
            WHEN '2' THEN 'Monday'\
            WHEN '3' THEN 'Tuesday'\
            WHEN '4' THEN 'Wednesday'\
            WHEN '5' THEN 'Thursday'\
            WHEN '6' THEN 'Friday'\
            WHEN '7' THEN 'Saturday'\
            ELSE 'ERROR' END,CONCAT(CONCAT(start_time,'-'),end_time),room FROM section_time WHERE section_id='%d'"%(section_id)
        cursor2.execute(sql2);



        templates = {
            'section' : cursor.fetchall(),
            'time' : cursor2.fetchall(),
            'course_id' : course_id,
            'section_id' : section_id,
            'section_number' : section_number,
        }
        get_template = JINJA_ENVIRONMENT.get_template('secdetail.html')
        self.response.write(get_template.render(templates));
        conn.close();
        conn2.close();

class ModifySectionHandler(webapp2.RequestHandler):
    def get(self):

        course_id=self.request.get('course_id');
        section_id=self.request.get('section_id');
        section_id=int(section_id)
        section_number=self.request.get('section_number');
        section_number=int(section_number)
        conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor = conn.cursor()

        sql="SELECT section_number,firstname,capacity\
            FROM section sec JOIN staff st ON teacher_id=staff_id\
            WHERE section_id='%d' AND section_number='%d'"%(section_id,section_number)
        cursor.execute(sql);

        conn2 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor2 = conn2.cursor()
        sql2="SELECT sectime_id, CASE day WHEN '1' THEN 'Sunday'\
            WHEN '2' THEN 'Monday'\
            WHEN '3' THEN 'Tuesday'\
            WHEN '4' THEN 'Wednesday'\
            WHEN '5' THEN 'Thursday'\
            WHEN '6' THEN 'Friday'\
            WHEN '7' THEN 'Saturday'\
            ELSE 'ERROR' END,CONCAT(CONCAT(start_time,'-'),end_time),room FROM section_time WHERE section_id='%d'"%(section_id)
        cursor2.execute(sql2);

        templates = {
            'section' : cursor.fetchall(),
            'time' : cursor2.fetchall(),
            'course_id' : course_id,
            'section_id' : section_id,
            'section_number' : section_number,
        }
        get_template = JINJA_ENVIRONMENT.get_template('section_modify.html')
        self.response.write(get_template.render(templates));
        conn.close();
        conn2.close();

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class AddSectimeHandler(webapp2.RequestHandler):
    def get(self):
        
        course_id=self.request.get('course_id');
        section_id=self.request.get('section_id');
        section_id=int(section_id)
        section_number=self.request.get('section_number');
        section_number=int(section_number)

        templates = {
            'course_id' : course_id,
            'section_id' : section_id,
            'section_number' : section_number,
        }
        get_template = JINJA_ENVIRONMENT.get_template('section_time.html')
        self.response.write(get_template.render(templates));

class InsSectimeHandler(webapp2.RequestHandler):
    def post(self):

        course_id=self.request.get('course_id');
        section_id=self.request.get('section_id');
        section_id=int(section_id)
        section_number=self.request.get('section_number');
        section_number=int(section_number)
        day=self.request.get('day');
        day=int(day)
        start_time=self.request.get('start_time');
        end_time=self.request.get('end_time');
        room=self.request.get('roomid');

        conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor = conn.cursor()
        sql="INSERT INTO section_time (day,start_time,end_time,room,section_id)\
            VALUES ('%d','%s','%s','%s','%d')"%(day,start_time,end_time,room,section_id)
        cursor.execute(sql);
        conn.commit();
        conn.close();

        utc = pytz.utc
        date_object = datetime.today()
        utc_dt = utc.localize(date_object);
        bkk_tz = timezone("Asia/Bangkok");
        bkk_dt = bkk_tz.normalize(utc_dt.astimezone(bkk_tz))
        time_insert = bkk_dt.strftime("%H:%M:%S")

        conn2 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor2 = conn2.cursor()
        sql2="INSERT INTO log (staff_id,course_id,day,time,type)\
            VALUES(3,(SELECT course_id FROM course WHERE course_code = '%s'),CURDATE(),'%s',3)"%(course_id,time_insert)
        cursor2.execute(sql2)        
        conn2.commit()
        conn2.close();

        self.redirect("/ModifySection?course_id="+str(course_id)+"&section_id="+str(section_id)+"&section_number="+str(section_number));

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class DeleteCourseHandler(webapp2.RequestHandler):
    def get(self):
        
        course_id=self.request.get('course_id')
        conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor = conn.cursor()
        sql="DELETE FROM regiscourse  WHERE course_id=(SELECT course_id FROM course WHERE course_code='%s')"%(course_id)
        cursor.execute(sql);
        conn.commit();
        conn.close();

        conn3 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor3 = conn3.cursor()
        sql3="DELETE FROM course WHERE course_code='%s'"%(course_id)
        cursor3.execute(sql3);
        conn3.commit();
        conn3.close();

        utc = pytz.utc
        date_object = datetime.today()
        utc_dt = utc.localize(date_object);
        bkk_tz = timezone("Asia/Bangkok");
        bkk_dt = bkk_tz.normalize(utc_dt.astimezone(bkk_tz))
        time_insert = bkk_dt.strftime("%H:%M:%S")

        conn2 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor2 = conn2.cursor()
        sql2="INSERT INTO log (staff_id,course_id,day,time,type)\
            VALUES(3,(SELECT course_id FROM course WHERE course_code = '%s'),CURDATE(),'%s',7)"%(course_id,time_insert)
        cursor2.execute(sql2)        
        conn2.commit()
        conn2.close();

        self.redirect("/");

class DeleteSectionHandler(webapp2.RequestHandler):
    def get(self):
    	
        course_id=self.request.get('course_id')
        section_id=self.request.get('section_id')
        section_id=int(section_id)
        conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor = conn.cursor()
        sql="DELETE FROM section WHERE section_id='%d'"%(section_id)
        cursor.execute(sql);
        conn.commit();
        conn.close();

        utc = pytz.utc
        date_object = datetime.today()
        utc_dt = utc.localize(date_object);
        bkk_tz = timezone("Asia/Bangkok");
        bkk_dt = bkk_tz.normalize(utc_dt.astimezone(bkk_tz))
        time_insert = bkk_dt.strftime("%H:%M:%S")

        conn2 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor2 = conn2.cursor()
        sql2="INSERT INTO log (staff_id,course_id,day,time,type)\
            VALUES(3,(SELECT course_id FROM course WHERE course_code = '%s'),CURDATE(),'%s',6)"%(course_id,time_insert)
        cursor2.execute(sql2)        
        conn2.commit()
        conn2.close();

        self.redirect("/ModifyCourse?course_id="+course_id)

class DeleteSectimeHandler(webapp2.RequestHandler):
    def get(self):
        
        course_id=self.request.get('course_id')
        sectime_id=self.request.get('sectime_id')
        sectime_id=int(sectime_id)
        section_id=self.request.get('section_id')
        section_id=int(section_id)
        section_number=self.request.get('section_number');
        section_number=int(section_number)
        conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor = conn.cursor()
        sql="DELETE FROM section_time WHERE sectime_id='%d'"%(sectime_id)
        cursor.execute(sql);
        conn.commit();
        conn.close();

        utc = pytz.utc
        date_object = datetime.today()
        utc_dt = utc.localize(date_object);
        bkk_tz = timezone("Asia/Bangkok");
        bkk_dt = bkk_tz.normalize(utc_dt.astimezone(bkk_tz))
        time_insert = bkk_dt.strftime("%H:%M:%S")

        conn2 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor2 = conn2.cursor()
        sql2="INSERT INTO log (staff_id,course_id,day,time,type)\
            VALUES(3,(SELECT course_id FROM course WHERE course_code = '%s'),CURDATE(),'%s',7)"%(course_id,time_insert)
        cursor2.execute(sql2)        
        conn2.commit()
        conn2.close();

        self.redirect("/ModifySection?course_id="+course_id+"&section_id="+str(section_id)+"&section_number="+str(section_number));




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/toggle',Toggle),
    ('/search',search),
    ('/Create', CreateHandler),
    ('/Insert', InsertHandler),
    ('/Error', ErrorHandler),
    ('/Notification',Notification),
    ('/DetailCourse',DetailCourseHandler),
    ('/ModifyCourse',ModifyCourseHandler),
    ('/UpdateCourse',UpdateCourseHandler),
    ('/AddSection',AddSectionHandler),
    ('/InsSection',InsSectionHandler),
    ('/AddSectime',AddSectimeHandler),
    ('/InsSectime',InsSectimeHandler),
    ('/DetailSection',DetailSectionHandler),
    ('/ModifySection',ModifySectionHandler),
    ('/DeleteCourse',DeleteCourseHandler),
    ('/DeleteSection',DeleteSectionHandler),
    ('/DeleteSectime',DeleteSectimeHandler)
], debug=True)
