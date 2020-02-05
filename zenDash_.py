#Zenpy Doodling
#Using Zenpy to connect Zendesk Data into grafana
# Zenpy accepts an API token
creds = {
    'email' : '',
    'token' : '',
    'subdomain': ''
}

# An OAuth token
#creds = {
#  "subdomain": "yoursubdomain",
#  "oauth_token": "youroathtoken"
#}

# Or a password
creds = {
    'email' : '',
    'password' : '',
    'subdomain': ''
}

# Import the Zenpy Class
from zenpy import Zenpy
import datetime
import time
import os
import mysql.connector
import re

os.environ['EST'] = 'United States/New York'

zenpy_client = Zenpy(**creds)
print('Connected \n')


start_time = time.time()

ticket_ID = [] #array of ticket ids
refresh_counter = 0

#mysql connection
mydb = mysql.connector.connect(
        host='',
        user='',
        password='',
        database='zendesk_dash',
        auth_plugin='mysql_native_password'
        )
#mydb = mysql.connector.connect(
#            host='',
#            user='',
#            password='',
#            database='',
#            auth_plugin='mysql_native_password'
#            )
mycursor = mydb.cursor()
cursor = mydb.cursor()       
#function for sql statements
def connection_week(id_ticket,user,requester,timespan, xtotal, created_at, updated_at, statuses):
    sql = 'INSERT INTO basic_ticket_data_week(ticket_id, user, requester, timespan, xtotal, created_at, updated_at, status) VALUES (%s, %s , %s, %s, %s, %s, %s, %s);'
    val = [id_ticket, user, requester, timespan, xtotal, created_at, updated_at, statuses]
    mycursor.execute(sql,val)
    mydb.commit()
        #print(mycursor.rowcount, "was inserted.")
        
def connection_month(id_ticket,user,requester,timespan, xtotal, created_at, updated_at, statuses):
    sql = 'INSERT INTO basic_ticket_data_month(ticket_id, user, requester, timespan, xtotal, created_at, updated_at, status, entry_date_added) VALUES (%s, %s , %s, %s, %s, %s, %s, %s);'
    val = [id_ticket, user, requester, timespan, xtotal, created_at, updated_at, statuses]
    mycursor.execute(sql,val)
    mydb.commit()
    
def connection_big_bucket(id_ticket,user,requester,timespan, xtotal, created_at, updated_at, statuses):
    sql = 'INSERT INTO big_bucket(ticket_id, user, requester, timespan, xtotal, created_at, updated_at, status) VALUES (%s, %s , %s, %s, %s, %s, %s, %s);'
    val = [id_ticket, user, requester, timespan, xtotal, created_at, updated_at, statuses]
    mycursor.execute(sql,val)
    mydb.commit()

def insertDUPE_table(id_ticket, user, requester,timespan, xtotal, created_at, updated_at, statuses, tag):
    sql = 'INSERT INTO cte(ticket_id, user, requester, timespan, xtotal, created_at, updated_at, status, tag) VALUES (%s, %s , %s, %s, %s, %s, %s, %s, %s);'
    val = [id_ticket, user, requester, timespan, xtotal, created_at, updated_at, statuses, tag]
    mycursor.execute(sql,val)
    mydb.commit()
    
def insert_Satisfaction(id_ticket, rating, total,tag, good_count, bad_count):
    sql = 'INSERT INTO satisfaction(ticket_id, rating, total,tag, good_count, bad_count) VALUES (%s, %s, %s , %s, %s, %s);'
    val = [id_ticket, rating, total,tag, good_count, bad_count]
    mycursor.execute(sql,val)
    mydb.commit()

def insert_reply_time(id_ticket, replyTime, tag, avg_time):
    sql = 'INSERT INTO metrics(ticket_id, replyTime,tag, avg_time) VALUES (%s, %s, %s, %s);'
    val = [id_ticket, replyTime,tag,avg_time]
    mycursor.execute(sql,val)
    mydb.commit()
    
def insert_system_builds(id_ticket,user,requester,timespan,created_at,status, subject):
    sql = 'INSERT INTO system_builds(ticket_id,user,requester,timespan,created_at,status, subject) VALUES (%s, %s, %s, %s, %s, %s, %s);'
    val = [id_ticket,user,requester,timespan,created_at,status,subject]
    mycursor.execute(sql,val)
    mydb.commit()

def insert_employee_check(id_ticket,start_date,employee_name,department,status):
    sql = 'INSERT INTO employee_check(ticket_id,start_date,employee_name,department,status) VALUES (%s, %s, %s, %s, %s);'
    val = [id_ticket,start_date,employee_name,department,status]
    mycursor.execute(sql,val)
    mydb.commit()

def searchData(ticketid,user,requester,timespan, xtotal, created_at, updated_at, status):
    ticket_string = str(ticketid)
    ticket_string = ticket_string.replace('Ticket(id=', '')
    ticket_string = ticket_string.replace(')', '')
    
    sql = 'SELECT * FROM basic_ticket_data '
    drop_that_shit = 'DELETE FROM basic_ticket_data WHERE ticket_id = %s '
    
    value = ticket_string

    mycursor.execute(sql)
    records = mycursor.fetchall()


    for row in records:
        if(ticket_string == str(row[0])):
            print("Record Found: ", ticket_string, "=", str(row[0]))
            print(drop_that_shit)
            mycursor.execute(drop_that_shit, (value,))
            print("Deleted old record")
            mydb.commit()
            connection(ticket_string,user,requester,timespan, xtotal, created_at, updated_at)
        else:
            print("Uploaded new record")
            connection(ticket_string,user,requester,timespan, xtotal, created_at, updated_at)
        
        print("Out of the search loop")


def duplicateTable_Drop():
    print("Dropping old data")    

    sql = """
    DELETE FROM cte;
    
    """
    mycursor.execute(sql)
    mydb.commit()
    
def duplicateTable_Drop_Satis():
    print("Dropping old data")    

    sql = """
    DELETE FROM satisfaction;
    
    """
    mycursor.execute(sql)
    mydb.commit()
    
def duplicateTable_Drop_metrics():
    print("Dropping old data")    

    sql = """
    DELETE FROM metrics;
    
    """
    mycursor.execute(sql)
    mydb.commit()
    
def duplicateTable_Drop_systemBuilds():
    print("Dropping old data")    

    sql = """
    DELETE FROM system_builds;
    
    """
    mycursor.execute(sql)
    mydb.commit()
    
def duplicateTable_Drop_employee_check():
    print("Dropping old data")    

    sql = """
    DELETE FROM employee_check;
    
    """
    mycursor.execute(sql)
    mydb.commit()
    
def check_empty():
    print("Checking table data")
    
    sql = """
    SELECT * FROM cte ;
    """
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    if not rows:
        print("It's empty")
        return True
    else:
        return False

def check_Satis_Empty():
    print("Checking table data")
    
    sql = """
    SELECT * FROM satisfaction ;
    """
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    if not rows:
        print("It's empty")
        return True
    else:
        return False

def ticketsYesterday():
    total_tickets = 0
    id_tickets = ''
    users = ''
    requestee = ''
    timespan = 0
    created_at = ''
    updated_at = ''
    ticket_Array = []
    status = ''
    tag = 'one_day'
    yesterday = datetime.datetime.now() - datetime.timedelta(days=2)
    result_generator = zenpy_client.search(created_after=(yesterday.strftime("%Y-%m-%d")), type='ticket')
    result_generator1 = zenpy_client.search(created_after=(yesterday.strftime("%Y-%m-%d")), type='ticket', sort_by='created_at')
    for count in result_generator:
        total_tickets += 1
        
    for ticket in result_generator1:
        #print(ticket.id, ticket.requester.name, ticket.assignee.name, ticket.created_at, ticket.updated_at)
        id_tickets = ticket.id
        
        if ticket.assignee is None:
            users is None
        else:
            users = ticket.assignee.name
                
    
        requestee = ticket.requester.name
        status = ticket.status
        
        created_at = ticket.created_at
        created_at = created_at.replace('T', ' ')
        created_at = created_at.replace('Z', '')
        created_at_dupe = created_at.split(" ")
        created_at_dupe = created_at_dupe[0]
    
    
        created_at_dupe_obj = datetime.datetime.strptime(created_at_dupe, "%Y-%m-%d").date()
        timespan = (datetime.date.today() - created_at_dupe_obj)
        timespan = str(timespan)
        timespan = timespan.split(" ")
        timespan = timespan[0]
    
        if timespan == "0:00:00":
            timespan = 0
    
    
   #print(int(timespan))
    
    #timespan = datetime.date.today - datetime.date(int(created_at_dupe))
        Created_at_obj = datetime.datetime.strptime(created_at,'%Y-%m-%d %H:%M:%S')
        Created_at_obj = Created_at_obj - datetime.timedelta(hours=5)
    
        updated_at = ticket.updated_at
        updated_at = updated_at.replace('T', ' ')
        updated_at = updated_at.replace('Z', '')
        Updated_at_obj = datetime.datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')
        Updated_at_obj = Updated_at_obj - datetime.timedelta(hours=5)
    
        ticket_Array.append(ticket.id)
    
    
        #searchData(id_tickets,users,requestee,times,total_tickets, Created_at_obj, Updated_at_obj, status)
        #print(Created_at_obj, Updated_at_obj)
        connection_big_bucket(id_tickets,users,requestee,timespan,total_tickets, created_at, updated_at, status)
        insertDUPE_table(id_tickets,users,requestee,timespan,total_tickets, created_at, updated_at, status, tag)
        time.sleep(1)
    replyTime(yesterday,tag)
    satisfactionRatings(yesterday,tag)
    print('Total Tickets = ', total_tickets)


def ticketsWeek():
    total_tickets = 0
    id_tickets = ''
    users = ''
    requestee = ''
    timespan = 0
    created_at = ''
    updated_at = ''
    ticket_Array = []
    status = ''
    tag = 'one_week'
    one_week = datetime.datetime.now() - datetime.timedelta(days=7)
    result_generator = zenpy_client.search(created_after=(one_week.strftime("%Y-%m-%d")), type='ticket')
    result_generator1 = zenpy_client.search(created_after=(one_week.strftime("%Y-%m-%d")), type='ticket', sort_by='created_at')
    for count in result_generator:
        total_tickets += 1
        
    for ticket in result_generator1:
        #print(ticket.id, ticket.requester.name, ticket.assignee.name, ticket.created_at, ticket.updated_at)
        id_tickets = ticket.id
            
        if ticket.assignee is None:
            users is None
        else:
            users = ticket.assignee.name
    
    
        requestee = ticket.requester.name
        status = ticket.status
    
        created_at = ticket.created_at
        created_at = created_at.replace('T', ' ')
        created_at = created_at.replace('Z', '')
        created_at_dupe = created_at.split(" ")
        created_at_dupe = created_at_dupe[0]
        
        
        created_at_dupe_obj = datetime.datetime.strptime(created_at_dupe, "%Y-%m-%d").date()
        timespan = (datetime.date.today() - created_at_dupe_obj)
        timespan = str(timespan)
        timespan = timespan.split(" ")
        timespan = timespan[0]
    
        if timespan == "0:00:00":
            timespan = 0
    
    
    #print(int(timespan))
    
        #timespan = datetime.date.today - datetime.date(int(created_at_dupe))
        Created_at_obj = datetime.datetime.strptime(created_at,'%Y-%m-%d %H:%M:%S')
        Created_at_obj = Created_at_obj - datetime.timedelta(hours=5)
    
        updated_at = ticket.updated_at
        updated_at = updated_at.replace('T', ' ')
        updated_at = updated_at.replace('Z', '')
        Updated_at_obj = datetime.datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')
        Updated_at_obj = Updated_at_obj - datetime.timedelta(hours=5)
    
        ticket_Array.append(ticket.id)
    
    
        #searchData(id_tickets,users,requestee,times,total_tickets, Created_at_obj, Updated_at_obj, status)
        #print(Created_at_obj, Updated_at_obj)
        connection_big_bucket(id_tickets,users,requestee,timespan,total_tickets, created_at, updated_at, status)
        insertDUPE_table(id_tickets,users,requestee,timespan,total_tickets, created_at, updated_at, status,tag)
        time.sleep(1)
    replyTime(one_week,tag)
    satisfactionRatings(one_week,tag)
    print('Total Tickets = ', total_tickets)


def ticketsWeek2():
    total_tickets = 0
    id_tickets = ''
    users = ''
    requestee = ''
    timespan = 0
    created_at = ''
    updated_at = ''
    ticket_Array = []
    status = ''
    tag = 'two_weeks'
    two_weeks = datetime.datetime.now() - datetime.timedelta(days=14)
    result_generator = zenpy_client.search(created_after=(two_weeks.strftime("%Y-%m-%d")), type='ticket')
    result_generator1 = zenpy_client.search(created_after=(two_weeks.strftime("%Y-%m-%d")), type='ticket', sort_by='created_at')
    for count in result_generator:
        total_tickets += 1
  
    for ticket in result_generator1:
        #print(ticket.id, ticket.requester.name, ticket.assignee.name, ticket.created_at, ticket.updated_at)
        id_tickets = ticket.id
            
        if ticket.assignee is None:
            users is None
        else:
            users = ticket.assignee.name
    
    
        requestee = ticket.requester.name
        status = ticket.status
        
        created_at = ticket.created_at
        created_at = created_at.replace('T', ' ')
        created_at = created_at.replace('Z', '')
        created_at_dupe = created_at.split(" ")
        created_at_dupe = created_at_dupe[0]
    
    
        created_at_dupe_obj = datetime.datetime.strptime(created_at_dupe, "%Y-%m-%d").date()
        timespan = (datetime.date.today() - created_at_dupe_obj)
        timespan = str(timespan)
        timespan = timespan.split(" ")
        timespan = timespan[0]
    
        if timespan == "0:00:00":
            timespan = 0
    
    
    #print(int(timespan))
        
        #timespan = datetime.date.today - datetime.date(int(created_at_dupe))
        Created_at_obj = datetime.datetime.strptime(created_at,'%Y-%m-%d %H:%M:%S')
        Created_at_obj = Created_at_obj - datetime.timedelta(hours=5)
    
        updated_at = ticket.updated_at
        updated_at = updated_at.replace('T', ' ')
        updated_at = updated_at.replace('Z', '')
        Updated_at_obj = datetime.datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')
        Updated_at_obj = Updated_at_obj - datetime.timedelta(hours=5)
    
        ticket_Array.append(ticket.id)
    
    
        #searchData(id_tickets,users,requestee,times,total_tickets, Created_at_obj, Updated_at_obj, status)
        #print(Created_at_obj, Updated_at_obj)
        connection_big_bucket(id_tickets,users,requestee,timespan,total_tickets, created_at, updated_at, status)
        insertDUPE_table(id_tickets,users,requestee,timespan,total_tickets, created_at, updated_at, status,tag)
        time.sleep(1)
    replyTime(two_weeks,tag)
    satisfactionRatings(two_weeks,tag)
    print('Total Tickets = ', total_tickets)
    

def ticketMonth():
    total_tickets = 0
    id_tickets = ''
    users = ''
    requestee = ''
    timespan = 0
    created_at = ''
    updated_at = ''
    ticket_Array = []
    status = ''
    tag = 'month'
    one_month = datetime.datetime.now() - datetime.timedelta(days=30)
    result_generator = zenpy_client.search(created_after=(one_month.strftime("%Y-%m-%d")), type='ticket')
    result_generator1 = zenpy_client.search(created_after=(one_month.strftime("%Y-%m-%d")), type='ticket', sort_by='created_at')
    for count in result_generator:
        total_tickets += 1
        
    for ticket in result_generator1:
        #print(ticket.id, ticket.requester.name, ticket.assignee.name, ticket.created_at, ticket.updated_at)
        id_tickets = ticket.id
    
        if ticket.assignee is None:
            users is None
        else:
            users = ticket.assignee.name
    
    
        requestee = ticket.requester.name
        status = ticket.status
        
        created_at = ticket.created_at
        created_at = created_at.replace('T', ' ')
        created_at = created_at.replace('Z', '')
        created_at_dupe = created_at.split(" ")
        created_at_dupe = created_at_dupe[0]
    
    
        created_at_dupe_obj = datetime.datetime.strptime(created_at_dupe, "%Y-%m-%d").date()
        timespan = (datetime.date.today() - created_at_dupe_obj)
        timespan = str(timespan)
        timespan = timespan.split(" ")
        timespan = timespan[0]
    
        if timespan == "0:00:00":
            timespan = 0
    
    
        #print(int(timespan))
    
        #timespan = datetime.date.today - datetime.date(int(created_at_dupe))
        Created_at_obj = datetime.datetime.strptime(created_at,'%Y-%m-%d %H:%M:%S')
        Created_at_obj = Created_at_obj - datetime.timedelta(hours=5)
    
        updated_at = ticket.updated_at
        updated_at = updated_at.replace('T', ' ')
        updated_at = updated_at.replace('Z', '')
        Updated_at_obj = datetime.datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')
        Updated_at_obj = Updated_at_obj - datetime.timedelta(hours=5)
    
        ticket_Array.append(ticket.id)
    
    
        #searchData(id_tickets,users,requestee,times,total_tickets, Created_at_obj, Updated_at_obj, status)
        #print(Created_at_obj, Updated_at_obj)
        connection_big_bucket(id_tickets,users,requestee,timespan,total_tickets, created_at, updated_at, status)
        insertDUPE_table(id_tickets,users,requestee,timespan,total_tickets, created_at, updated_at, status, tag)
        time.sleep(1)
    replyTime(one_month,tag)
    satisfactionRatings(one_month,tag)
    print('Total Tickets = ', total_tickets)
    

def satisfactionRatings(tq,tag):
        
    ticket_id = ''
    good_count = 0
    bad_count = 0
    no_reviews_count = 0
    rating = 0.0
    total_reviews = 0
    
    time_query = tq #add this to the function when returning back after break
    #one_month = datetime.datetime.now() - datetime.timedelta(days=30)
    result_generator = zenpy_client.search(created_after=(time_query.strftime("%Y-%m-%d")), type='ticket')
    for ticket in result_generator:
        ticket_id = ticket.id
        if(ticket.satisfaction_rating != None):
            #print(ticket.satisfaction_rating.score)
            if(ticket.satisfaction_rating.score == 'good'):
                #print("We did well")
                good_count += 1
            elif(ticket.satisfaction_rating.score == 'bad'):
                #print("We did bad")
                bad_count += 1
            elif(ticket.satisfaction_rating.score == 'unoffered'):
                #print("The customer did not respond")
                no_reviews_count +=1
        
    total_reviews = good_count + bad_count
    if (total_reviews == 0):
        rating = 0
    else:
        rating = good_count / total_reviews 
        rating = rating * 100
    
    insert_Satisfaction(ticket_id, rating, total_reviews, tag, good_count, bad_count)
    print("We scored :",good_count," Good reviews vs ", bad_count, "Bad reviews")
    print(no_reviews_count, " Customers did not leave a review")


def replyTime(tq,tag):
    metric = ''
    response_time = ''
    time_query = tq
    all_time = 0
    avg_time = 0.0
    total = 0
    #time = datetime.datetime.now() - datetime.timedelta(days=30)
    result_generator = zenpy_client.search(created_after=(time_query.strftime("%Y-%m-%d")), type='ticket')
    
    
    for ticket in result_generator:
        #print("Enter metrics")
        tick_id = ticket.id
        ticket_metric = zenpy_client.tickets.metrics(tick_id)
        if ticket_metric is None:
            response_time is None
        else:
            data = str(ticket_metric.reply_time_in_minutes)
            #print(data)
            metric = data.split(":")
            metric = metric[2]
            metric = metric.replace('}','')
            metric = metric.strip()
            #print(metric)
            if metric == 'None':
                metric = 'None'
            else:
                #print('test')
                all_time += all_time + int(metric)
                #print(all_time)
                response_time = str(metric)
                total += total + 1
                #print(total)
                avg_time = all_time / total
    insert_reply_time(tick_id, response_time, tag, avg_time)

def systemBuilds():
    id_tickets = ''
    users = ''
    requestee = ''
    created_at = ''
    ticket_Array = []
    status = ''
    subject = ''
    year = datetime.datetime.now() - datetime.timedelta(days=365)
    result_generator1 = zenpy_client.search(created_after=(year.strftime("%Y-%m-%d")), type='ticket', group = 'System Builds', sort_by='created_at')
    for ticket in result_generator1:
        
        id_tickets = ticket.id
        #print(ticket.subject)
        subject = ticket.subject
        
        if ticket.assignee is None:
            users is None
        else:
            users = ticket.assignee.name
    
    
        requestee = ticket.requester.name
        status = ticket.status
        
        created_at = ticket.created_at
        created_at = created_at.replace('T', ' ')
        created_at = created_at.replace('Z', '')
        created_at_dupe = created_at.split(" ")
        created_at_dupe = created_at_dupe[0]

        created_at_dupe_obj = datetime.datetime.strptime(created_at_dupe, "%Y-%m-%d").date()
        timespan = (datetime.date.today() - created_at_dupe_obj)
        timespan = str(timespan)
        timespan = timespan.split(" ")
        timespan = timespan[0]
    
        if timespan == "0:00:00":
            timespan = 0

        Created_at_obj = datetime.datetime.strptime(created_at,'%Y-%m-%d %H:%M:%S')
        Created_at_obj = Created_at_obj - datetime.timedelta(hours=5)
        ticket_Array.append(ticket.id)
        time.sleep(1)
        insert_system_builds(id_tickets,users,requestee,timespan,created_at,status,subject)
        
        
def empCheck():
    id_tickets = ''
    employee_name = ''
    start_date = ''
    ticket_Array = []
    department = ''
    subject = ''
    status = ''
    timespan = datetime.datetime.now() - datetime.timedelta(days=31)
    result_generator1 = zenpy_client.search(created_after=(timespan.strftime("%Y-%m-%d")), type='ticket', group = 'New Employee', sort_by='created_at')
    for ticket in result_generator1:
        id_tickets = ticket.id
        status = ticket.status
        
        subject = ticket.subject
        sample = subject.lower()
        
        result_start = ticket.description
        result_dept = ticket.description
        result_dept.splitlines()
        
        start_date = result_start[result_start.find("Start Date:"):result_start.find("End Date")]
        start_date = start_date.replace('Start Date: ','')
        start_date = start_date.strip()
        
        department = result_dept[result_dept.find("Department:"):result_dept.find('\nSupervisor Email:')]
        department = department.replace('Department: ','')
        department = department.strip()
        
        if ('new emp - ' in sample):
            employee_name = subject[subject.find("-")+2:subject.find("(")]
            insert_employee_check(id_tickets,start_date,employee_name,department,status)
            
            #print(employee_name)
            #print(start_date)
            #print(department)
            #print(status)
            
        ticket_Array.append(ticket.id)
        time.sleep(1)
        
##################################################################################################################
duplicateTable_Drop()
duplicateTable_Drop_Satis()
duplicateTable_Drop_metrics()
duplicateTable_Drop_systemBuilds()
duplicateTable_Drop_employee_check()
ticketsYesterday()
time.sleep(5)
ticketsWeek()
time.sleep(5)
ticketsWeek2()
time.sleep(5)
ticketMonth()
systemBuilds()
empCheck()
print("Finished rotation")
print("--- %s seconds ---" % (time.time() - start_time))
time.sleep(30)
mycursor.close()