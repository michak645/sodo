# -*- coding: utf-8 -*-

import sys
#from importlib import reload
#reload(sys)
#sys.setdefaultencoding("UTF8")
import json, requests
import sqlite3
#import mysql.connector
import MySQLdb
import os.path
import chardet

#   TERMINY ODNOŚNIE PRACY
#   - obrony od 7 do 12 stycznia
#   - egzamin jest powiązany z pracą
#   

#   Na za tydzień szkielet pracy dyplomowej
#   - spis treści (początkowy)
#   - co znajduje się w projekcie
#   - jak to zostało rozwiązane
#   - jak coś zrobić (zalety, wady, trudności)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "PupilPremiumTable.db")

host = "http://150.254.76.229/EodService/AXDWService.asmx/"
#model = "wnioski_"
domain = "@amu.edu.pl"

# Parametry: EmpId
#urlEmpByEmpId = host + "GetEmpByEmpId?EmpId=string" + emp_id
EmpByEmpId = host + "GetEmpByEmpId"

'''
# Parametry: EmpId, year, uid, password
urlEmpHolidayHoursEmpId = host + "GetEmpHolidayHours?EmpId=" + emp_id + "&year=" + year + "&uid=" + uid + "&password=" + password
EmpHolidayHoursEmpId = host + "GetEmpHolidayHours"
'''

# Parametry: Nazwisko
#urlEmpListByLastName = host + "GetEmpListByLastName?Nazwisko=" + name
EmpListByLastName = host + "GetEmpListByLastName"

# Parametry: OrganizationDesc
#urlEmpListByOrgDesc = host + "GetEmpListByOrgDesc?OrganizationDesc=" + org_desc
EmpListByOrgDesc = host + "GetEmpListByOrgDesc"

# Parametry: Uid, status
#urlEmpListByUid = host + "GetEmpListByUid?Uid=" + uid + "&status=" + status
EmpListByUid = host + "GetEmpListByUid"

# Parametry: OrgId
#urlOrgById = host + "GetOrgById?OrgId=" + org_id
OrgById = host + "GetOrgById"

# Parametry: OrgDesc
#urlOrgListByDesc = host + "GetOrgListByDesc?OrgDesc=" + org_desc
OrgListByDesc = host + "GetOrgListByDesc"

#print ("Wybierz opcję")
#print ()


def EmpByEmpId(emp_id):
    #parameters = dict(EmpId = emp_id)
    urlEmpByEmpId = host + "GetEmpByEmpId?EmpId=%" + emp_id
    
    #response = requests.get(url = EmpByEmpId, params = parameters)
    response = requests.get(url = urlEmpByEmpId)
    data = json.loads(response.text)
    print (data)

'''
def EmpHolidayHoursEmpId(emp_id, year, uid, password):
    parameters = dict(EmpId = emp_id, year = year, uid = uid, password = password)
    
    
    response = requests.get(url = EmpHolidayHoursEmpId, params = parameters)
    data = json.loads(response.text)
    print (data)
'''
    
def EmpListByLastName(name):
    #parameters = dict(Nazwisko = name)
    urlEmpListByLastName = host + "GetEmpListByLastName?Nazwisko=%" + name
    
    #response = requests.get(url = EmpListByLastName, params = parameters)
    response = requests.get(url = urlEmpListByLastName)
    data = json.loads(response.text)
    #print (data)
    return data

def EmpListByOrgDesc(org_desc):
    #parameters = dict(OrganizationDesc = org_desc)
    urlEmpListByOrgDesc = host + "GetEmpListByOrgDesc?OrganizationDesc=%" + org_desc
    
    #response = requests.get(url = EmpListByOrgDesc, params = parameters)
    response = requests.get(url = urlEmpListByOrgDesc)
    data = json.loads(response.text)
    #print (data)
    return data
    
def EmpListByUid(uid, status):
    #parameters = dict(Uid = uid, status = status)
    urlEmpListByUid = host + "GetEmpListByUid?Uid=%" + uid + "&status=" + status
    
    #response = requests.get(url = EmpListByUid, params = parameters)
    response = requests.get(url = urlEmpListByUid)
    data = json.loads(response.text)
    print (data)
    
def OrgById(org_id):
    #parameters = dict(OrgId = org_id)
    urlOrgById = host + "GetOrgById?OrgId=%" + org_id
    
    #response = requests.get(url = OrgById, params = parameters)
    response = requests.get(url = urlOrgById)
    data = json.loads(response.text)
    print (data)
    
def OrgListByDesc(org_desc):
    #parameters = dict(OrgDesc = org_desc)
    urlOrgListByDesc = host + "GetOrgListByDesc?OrgDesc=%" + org_desc
    #print (urlOrgListByDesc)
    
    #response = requests.get(url = OrgListByDesc, params = parameters)
    response = requests.get(url = urlOrgListByDesc)
    #print (response)
    data = json.loads(response.text)
    #print (data)
    return data

'''    
def AllEmp():
    parameters = dict()
    
    response = requests.get(url = OrgListByDesc, params = parameters)
    data = json.loads(response.text)
    print data
'''

def start_org():
    organization_keys = []
    organization_descs = []

    org = OrgListByDesc("")
    amount = len(org)
    #up_org = org.replace("'", '"')
    # org_list to dictionary
    #org_list = json.loads(org)
    
    #print (org[0])
    #sys.exit()
    
    no_special = True
    
    for i in range(amount):
        for key, value in org[i].items():
            #print (key)
            #print (value)
            #sys.exit()
            if key == "OrganizationKey":
                #chardet.detect(value)
                organization_keys.append(value)
            if key == "OrganizationDesc":
                #u_value = str(value, "utf-8")
                #print ("Value: " + value)
                #try:
                #    value.encode("latin1")
                #    print ("Value after encoding: " + value)
                #except UnicodeEncodeError:
                #    no_special = False
                #if (no_special == False):
                #    value.encode(encoding="UTF-8", errors="strict")
                #    print ("Value after encoding UTF-8: " + value)
                #value.encode("utf8")
                '''
                value = value.replace('ą', 'a')
                value = value.replace('ć', 'c')
                value = value.replace('ę', 'e')
                value = value.replace('ł', 'l')
                value = value.replace('ń', 'n')
                value = value.replace('ó', 'o')
                value = value.replace('ś', 's')
                value = value.replace('ź', 'z')
                value = value.replace('ż', 'z')
                value = value.replace('Ą', 'A')
                value = value.replace('Ć', 'C')
                value = value.replace('Ę', 'E')
                value = value.replace('Ł', 'L')
                value = value.replace('Ń', 'N')
                value = value.replace('Ó', 'O')
                value = value.replace('Ś', 'S')
                value = value.replace('Ź', 'Z')
                value = value.replace('Ż', 'Z')
                value = value.replace('\u2026', "...")
                value = value.replace('\u0150', 'O')
                '''
                value = value.replace('\u0027', ' ')
                organization_descs.append(value)
            
            #organization_key = org_list.get("OrganizationKey", None)
            #organization_key = org.get("OrganizationKey", None)
            #organization_desc = org_list.get("OrganizationDesc", None)
            #organization_desc = org.get("OrganizationDesc", None)
        
            #if organization_key:
            #    organization_keys.append(organization_key)
            #if organization_desc:
            #    organization_descs.append(organization_desc)
    #for j in range(len(organization_keys)):
    
    #database = "db.sqlite3"
    #connection = sqlite3.connect("db.sqlite3", timeout = 10)
    
    database = MySQLdb.connect(host="localhost", user="root", passwd="password", db="sodo", charset="utf8")
    #print ("Database: ")
    #print (database)
    #query = """INSERT into " + model + "jednorg VALUES(%d, %s, %s)"""
    cursor = database.cursor()
    #print ("Cursor: ")
    #print (cursor)
    #print (query)
    #print ((organization_keys[0], organization_descs[0]))
    j = 0
    values = []
    
    #select_query = "SELECT COUNT(id) from auth_ex_jednorg"
    #cursor.execute(select_query)
    #row = cursor.fetchone()
    #count = row[0]

    print ("Amount: " + str(amount))
    for j in range(amount):
        #print ("Id jednostki: " + organization_keys[j] + "    nazwa jednostki: " + organization_descs[j])
        #with connection:
        
        #values = (organization_keys[j], organization_descs[j])
        #print ("Values: " + str(values))
        #cursor.execute(query, values)
        #print (organization_keys[j])
        #print (organization_descs[j])
        
        #values.append((organization_keys[j], organization_descs[j]))
        query = "INSERT into auth_ex_jednorg(id, nazwa) values('{}', '{}') on duplicate key UPDATE id=id, nazwa=nazwa".format(organization_keys[j], organization_descs[j])
        print ("Query: ")
        print (query)
        cursor.execute(query)
        #print (values)
        #print (cursor)
        #print ("Cursor: " + str(cursor))
    #print (values)
    
    #cursor.execute("INSERT into wnioski_jednorg(id_jedn, nazwa) values('{0}', '{1}')", [values])
    database.commit()
    #database.rollback()
    database.close()

def start_typ():
    # ZAKŁADAM, ŻE KAŻDY NA POCZĄTKU JEST "ZWYKŁY"
    #sys.exit()
    employee_types = []
    
    typ = EmpListByOrgDesc("%Matematyki")
    amount = len(typ)
    
    for i in range(amount):
        for key, value in typ[i].items():
            if key == "grupa_pracownika":
                '''
                value = value.replace('ą', 'a')
                value = value.replace('ć', 'c')
                value = value.replace('ę', 'e')
                value = value.replace('ł', 'l')
                value = value.replace('ń', 'n')
                value = value.replace('ó', 'o')
                value = value.replace('ś', 's')
                value = value.replace('ź', 'z')
                value = value.replace('ż', 'z')
                value = value.replace('Ą', 'A')
                value = value.replace('Ć', 'C')
                value = value.replace('Ę', 'E')
                value = value.replace('Ł', 'L')
                value = value.replace('Ń', 'N')
                value = value.replace('Ó', 'O')
                value = value.replace('Ś', 'S')
                value = value.replace('Ź', 'Z')
                value = value.replace('Ż', 'Z')
                '''
                #employee_types.update(value)
                employee_types.append(value)
    employee_types = set(employee_types)
    employee_types = list(employee_types)
    counts = len(employee_types)
    database = MySQLdb.connect(host="localhost", user="root", passwd="password", db="sodo", charset="utf8")
    cursor = database.cursor()
    #j = 0
    #values = []
    
    for j in range(counts):
        query = "INSERT into auth_ex_rodzajpracownika(nazwa) values('{}') on duplicate key UPDATE nazwa=nazwa".format(employee_types[j])
        cursor.execute(query)
    database.commit()
    database.close()
    
def start_emp():
    employee_uids = []
    employee_ax = []
    employee_surnames = []
    employee_names = []
    employee_groups = []
    employee_organization_keys = []
    employee_statuses = []

    emp = EmpListByOrgDesc("%Matematyki")
    amount = len(emp)
    
    for i in range(amount):
        for key, value in emp[i].items():
            '''
            value = value.replace('ą', 'a')
            value = value.replace('ć', 'c')
            value = value.replace('ę', 'e')
            value = value.replace('ł', 'l')
            value = value.replace('ń', 'n')
            value = value.replace('ó', 'o')
            value = value.replace('ś', 's')
            value = value.replace('ź', 'z')
            value = value.replace('ż', 'z')
            value = value.replace('Ą', 'A')
            value = value.replace('Ć', 'C')
            value = value.replace('Ę', 'E')
            value = value.replace('Ł', 'L')
            value = value.replace('Ń', 'N')
            value = value.replace('Ó', 'O')
            value = value.replace('Ś', 'S')
            value = value.replace('Ź', 'Z')
            value = value.replace('Ż', 'Z')
            '''
            if key == "uid":
                employee_uids.append(value + "@amu.edu.pl")
            elif key == "numer_AX":
                employee_ax.append(value)
            elif key == "nazwisko":
                employee_surnames.append(value)
            elif key == "imie":
                employee_names.append(value)
            elif key == "grupa_pracownika":
                employee_groups.append(value)
            elif key == "OrganizationKey":
                employee_organization_keys.append(value)
            elif key == "status":
                employee_statuses.append(value)
    
    
    
    database = MySQLdb.connect(host="localhost", user="root", passwd="password", db="sodo", charset="utf8")
    cursor = database.cursor()
    
    '''
    organizations_query = "SELECT * from wnioski_jednorg"
    cursor.execute(organizations_query)
    row = cursor.fetchone()
    
    k = 0   
    while row is not None:
        while k < amount:
            if employee_organization_keys[k] == row[1]:
                employee_organization_keys[k] = row[0]
            k += 1
            print (str(row[0]) + ' ' + row[1] + ' ' + row[2])
        row = cursor.fetchone()
    '''
    
    for k in range(amount):
        groups_query = u"SELECT * from auth_ex_rodzajpracownika where nazwa = '{}'".format(employee_groups[k])
        cursor.execute(groups_query)
        row = cursor.fetchone()
        employee_groups[k] = row[0]
    '''    
    k = 0
    while row is not None:
        if employee_groups[k] == row[1]:
            employee_groups[k] = row[0]
            k += 1
        print (str(row[0]) + ' ' + row[1])
        row = cursor.fetchone()
    '''
    #sys.exit()
    #j = 0
    #values = []
    
    print ("Amount: " + str(amount))
    for j in range(amount):
        query = u"INSERT into auth_ex_pracownik(imie, nazwisko, email, jedn_org_id, rodzaj_id, numer_ax, czy_pracuje) values('{}', '{}', '{}', '{}', '{}', '{}', '{}') on duplicate key UPDATE imie=imie, nazwisko=nazwisko, email=email, jedn_org_id=jedn_org_id, rodzaj_id=rodzaj_id, numer_ax=numer_ax, czy_pracuje=czy_pracuje".format(employee_names[j], employee_surnames[j], employee_uids[j], employee_organization_keys[j], employee_groups[j], employee_ax[j], employee_statuses[j])
        print ("Query: ")
        print (query)
        cursor.execute(query)
        #print (values)
        #print (cursor)
        #print ("Cursor: " + str(cursor))
    #print (values)
    
    #cursor.execute("INSERT into wnioski_jednorg(id_jedn, nazwa) values('{0}', '{1}')", [values])
    database.commit()
    #database.rollback()
    database.close()
    
'''    
def start_emp():
    return None

    organization_keys = []
    organization_descs = []

    org = OrgListByDesc("")
    amount = len(org)
    #up_org = org.replace("'", '"')
    # org_list to dictionary
    #org_list = json.loads(org)
    
    print (org[0])
    #sys.exit()
    
    for i in range(amount):
        for key, value in org[i].items():
            #print (key)
            #print (value)
            #sys.exit()
            if key == "OrganizationKey":
                organization_keys.append(value)
            if key == "OrganizationDesc":
                organization_descs.append(value)
            
            #organization_key = org_list.get("OrganizationKey", None)
            #organization_key = org.get("OrganizationKey", None)
            #organization_desc = org_list.get("OrganizationDesc", None)
            #organization_desc = org.get("OrganizationDesc", None)
        
            #if organization_key:
            #    organization_keys.append(organization_key)
            #if organization_desc:
            #    organization_descs.append(organization_desc)
    #for j in range(len(organization_keys)):
    database = "db.sqlite3"
    connection = sqlite3.connect("db.sqlite3")
    
    for j in range(20):
        print ("Id jednostki: " + organization_keys[j] + "    nazwa jednostki: " + organization_descs[j])
        with connection:
            sql = "INSERT into " + model + "jednorg(id_jedn, nazwa) VALUES(?, ?)"
            cursor = connection.cursor()
            values = (organization_keys[j], organization_descs[j])
            cursor.execute(sql, values)
'''
'''        
def start_typ():
    employee_types = []

    #emp = EmpListByOrgDesc("Matematyki i Informatyki")
    emp = EmpListByLastName("kow")
    amount = len(emp)
    
    for i in range(amount):
        for key, value in emp[i].items():
            if key == "grupa_pracownika":
                employee_types.append(value)

    database = "db.sqlite3"
    connection = sqlite3.connect(database)
    
    for j in range(20):
        print ("Rodzaj pracownika: " + employee_types[j])
        if employee_types[j] not in employee_types:
            with connection:
                sql = "INSERT into " + model + "rodzajpracownika(nazwa) VALUES(?)"
                cursor = connection.cursor()
                values = (employee_types[j])
                cursor.execute(sql, values)
'''
# Zmiany: id [numer_AX], nazwisko [nazwisko], imie [imie], rodzaj_id (-) [grupa_pracownika], jedn_org_id (jednorg.id_jedn), email [uid]
def update_employees(): 
    json_uids = []
    json_ax = []
    json_surnames = []
    json_names = []
    json_groups = []
    json_organization_keys = []
    json_statuses = []
    
    uids = []
    ax = []
    surnames = []
    names = []
    groups = []
    organization_keys = []
    statuses = []

    json_emp = EmpListByOrgDesc("%Matematyki")
    json_amount = len(json_emp)
    
    for i in range(json_amount):
        for key, value in json_emp[i].items():
            '''
            value = value.replace('ą', 'a')
            value = value.replace('ć', 'c')
            value = value.replace('ę', 'e')
            value = value.replace('ł', 'l')
            value = value.replace('ń', 'n')
            value = value.replace('ó', 'o')
            value = value.replace('ś', 's')
            value = value.replace('ź', 'z')
            value = value.replace('ż', 'z')
            value = value.replace('Ą', 'A')
            value = value.replace('Ć', 'C')
            value = value.replace('Ę', 'E')
            value = value.replace('Ł', 'L')
            value = value.replace('Ń', 'N')
            value = value.replace('Ó', 'O')
            value = value.replace('Ś', 'S')
            value = value.replace('Ź', 'Z')
            value = value.replace('Ż', 'Z')
            '''
            if key == "uid":
                json_uids.append(value + "@amu.edu.pl")
            elif key == "numer_AX":
                json_ax.append(value)
            elif key == "nazwisko":
                json_surnames.append(value)
            elif key == "imie":
                json_names.append(value)
            elif key == "grupa_pracownika":
                json_groups.append(value)
            elif key == "OrganizationKey":
                json_organization_keys.append(value)
            elif key == "status":
                json_statuses.append(value)

    database = MySQLdb.connect("localhost", "root", "password", "sodo")
    cursor = database.cursor()
    #j = 0
    #values = []
    '''
    count_query = "SELECT * from wnioski_pracownik"
    counts = cursor.execute(count_query)
    for k in range(counts):
        select_query = u"SELECT * from wnioski_pracownik"
        cursor.execute(select_query)
        data_from_database = cursor.fetchall()
        for row in data_from_database:
    '''        
    
    print ("Amount: " + str(json_amount))
    for j in range(json_amount):
        update_query = u"UPDATE wnioski_pracownik(imie, nazwisko, email, jedn_org_id, rodzaj_id, numer_ax, czy_pracuje) values('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(employee_names[j], employee_surnames[j], employee_uids[j], 4610, 8, employee_ax[j], employee_statuses[j])
        print ("Query: ")
        print (query)
        cursor.execute(query)
        #print (values)
        #print (cursor)
        #print ("Cursor: " + str(cursor))
    #print (values)
    
    #cursor.execute("INSERT into wnioski_jednorg(id_jedn, nazwa) values('{0}', '{1}')", [values])
    database.commit()
    #database.rollback()
    database.close()
    #sql = "UPDATE " + model + "pracownik SET "
    return None

def update_types():
    return None
    
# Zmiany: id_jedn [OrganizationKey], nazwa [OrganizationDesc]
def update_organizations():
    return None

# Automatyczne uzupełnianie danych na początku oraz ich prototypowa aktualizacja
start_org()
start_typ()
start_emp()
    
'''
print ("Opcje: ")
print ("a) EmpByEmpId\nb) EmpHolidayHoursEmpId\nc) EmpListByLastName\nd) EmpListByOrgDesc\ne) EmpListByUid\nf) OrgById\ng) OrgListByDesc")
opcja = input("Wybierz opcję\n")

if (opcja == "so"):
    start_org()
elif (opcja == "se"):
    start_emp()
elif (opcja == "st"):
    start_typ()
elif (opcja == 'a'):
    id = input("Podaj id pracownika: ")
    EmpByEmpId(id)
elif (opcja == 'c'):
    n = input("Podaj nazwisko pracownika: ")
    EmpListByLastName(n)
elif (opcja == 'd'):
    o_d = input("Podaj nazwę jednostki organizacyjnej: ")
    EmpListByOrgDesc(o_d)
elif (opcja == 'e'):
    u = input("Podaj uid pracownika: ")
    s = input("Podaj status pracownika: ")
    EmpListByUid(u, s)
elif (opcja == 'f'):
    o_i = input("Podaj id jednostki organizacyjnej: ")
    OrgById(o_i)
elif (opcja == 'g'):
    o_d = input("Podaj nazwę jednostki organizacyjnej: ")
    OrgListByDesc(o_d)    
'''    
'''
elif (opcja = 'b'):
    id = input("Podaj id pracownika")
    y = input("Podaj rok urlopu pracownika")   
    EmpHolidayHoursEmpId(id, y, uid, password)
'''    
    
    
    
    
