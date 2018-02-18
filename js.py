# -*- coding: utf-8 -*-

import sys
import json, requests
import sqlite3
import random
import string


host = "http://150.254.76.229/EodService/AXDWService.asmx/"
wnioski_model = "wnioski_"
auth_ex_model = "auth_ex_"
domain = "@amu.edu.pl"
database = "db.sqlite3"
organization_descs = []
login = ""    # ze względu na publiczność, utajone
password = "" # ze względu na publiczność, utajone


# Parametry: EmpId
# urlEmpByEmpId = host + "GetEmpByEmpId?EmpId=string" + emp_id
EmpByEmpId = host + "GetEmpByEmpId"

# Parametry: Nazwisko
# urlEmpListByLastName = host + "GetEmpListByLastName?Nazwisko=" + name
EmpListByLastName = host + "GetEmpListByLastName"

# Parametry: OrganizationDesc
# urlEmpListByOrgDesc = host + "GetEmpListByOrgDesc?OrganizationDesc=" + org_desc
EmpListByOrgDesc = host + "GetEmpListByOrgDesc"

# Parametry: Uid, status
# urlEmpListByUid = host + "GetEmpListByUid?Uid=" + uid + "&status=" + status
EmpListByUid = host + "GetEmpListByUid"

# Parametry: OrgId
# urlOrgById = host + "GetOrgById?OrgId=" + org_id
OrgById = host + "GetOrgById"

# Parametry: OrgDesc
# urlOrgListByDesc = host + "GetOrgListByDesc?OrgDesc=" + org_desc
OrgListByDesc = host + "GetOrgListByDesc"


def EmpByEmpId(emp_id, login, password):
    urlEmpByEmpId = host + "GetEmpByEmpId?EmpId=%" + emp_id + "&login=" + login + "&password=" + password
    
    response = requests.get(url = urlEmpByEmpId)
    data = json.loads(response.text)
    # print (data)
    
def EmpListByLastName(name, login, password):
    urlEmpListByLastName = host + "GetEmpListByLastName?Nazwisko=%" + name + "&login=" + login + "&password=" + password
    
    response = requests.get(url = urlEmpListByLastName)
    data = json.loads(response.text)
    # print (data)
    return data

def EmpListByOrgDesc(org_desc, login, password):
    urlEmpListByOrgDesc = host + "GetEmpListByOrgDesc?OrganizationDesc=%" + \ 
    org_desc + "&login=" + login + "&password=" + password
    
    response = requests.get(url = urlEmpListByOrgDesc)
    data = json.loads(response.text)
    # print (data)
    return data
    
def EmpListByUid(uid, status, login, password):
    urlEmpListByUid = host + "GetEmpListByUid?Uid=%" + uid + "&status=" + status + "&login=" + login + "&password=" + password
    
    response = requests.get(url = urlEmpListByUid)
    data = json.loads(response.text)
    # print (data)
    
def OrgById(org_id, login, password):
    urlOrgById = host + "GetOrgById?OrgId=%" + org_id + "&login=" + login + "&password=" + password
    
    response = requests.get(url = urlOrgById)
    data = json.loads(response.text)
    # print (data)
    
def OrgListByDesc(org_desc, login, password):
    urlOrgListByDesc = host + "GetOrgListByDesc?OrgDesc=%" + org_desc + "&login=" + login + "&password=" + password
    
    response = requests.get(url = urlOrgListByDesc)
    data = json.loads(response.text)
    # print (data)
    return data


def start_org(login, password):
    organization_keys = []
    organization_labi = []
    organization_parent_keys = []

    org = OrgListByDesc("", login, password)
    amount = len(org)

    for i in range(amount):
        for key, value in org[i].items():
            if key == "OrganizationKey":
                organization_keys.append(value)
            # Przyjmuję, że czy_labi oznacza LABI lub ABI
            if key == "OrganizationLevel":
                if value == '1' or value == '0':
                    organization_labi.append(1)
                else:
                    organization_labi.append(0)
            if key == "OrganizationDesc":
                value = value.replace('\u0027', ' ')
                organization_descs.append(value)
            if key == "OrganizationParentKey":
                organization_parent_keys.append(value)

    connection = sqlite3.connect(database)

    cursor = connection.cursor()
    j = 0

    # print ("Amount: " + str(amount))
    for j in range(amount):
        query = "INSERT or REPLACE into auth_ex_jednorg(id, czy_labi, nazwa, parent_id) values('{}', '{}', '{}', '{}')".format(organization_keys[j], organization_labi[j], organization_descs[j], organization_parent_keys[j])
        cursor.execute(query)
        
    connection.commit()
    connection.close()

def start_typ(login, password):
    # sys.exit()
    employee_types = []
    
    connection = sqlite3.connect(database)
    select_cursor = connection.cursor()
    insert_cursor = connection.cursor()
    select2_cursor = connection.cursor()
    
    select_cursor.execute("SELECT nazwa from auth_ex_jednorg")
    # for row in select_cursor:
    if (True):
        # print ("Row: ")
        # print (row)
        # typ = EmpListByOrgDesc(row[0])
        typ = EmpListByOrgDesc("Matematyki", login, password)
        amount = len(typ)
        
        for i in range(amount):
            for key, value in typ[i].items():
                if key == "grupa_pracownika":
                    # employee_types.update(value)
                    employee_types.append(value)
    employee_types = set(employee_types)
    employee_types = list(employee_types)
    counts = len(employee_types)
    j = 0
    
    # rodzaje = []
    # select2_cursor.execute("SELECT rodzaj from auth_ex_rodzajpracownika")
    # for row in select2_cursor:
        # rodzaj = select2_cursor.fetchone()
        # rodzaje.append(row[0])
        
    # print ("Rodzaje: ")
    # print (rodzaje)
    # print ("ET: ")
    # print (employee_types)
    # for employee_type in employee_types:
        # if employee_type in rodzaje:
            # employee_types.remove(employee_type)
    # print ("Po usunięciu: ")
    # print (employee_types)
    for j in range(counts):
        query = "INSERT or REPLACE into auth_ex_rodzajpracownika(rodzaj) values('{}')".format(employee_types[j])
        insert_cursor.execute(query)
    connection.commit()
    connection.close()
    
def start_emp(login, password):
    employee_uids = []
    employee_ax = []
    employee_surnames = []
    employee_names = []
    employee_groups = []
    employee_organization_keys = []

    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    
    cursor.execute("SELECT nazwa from auth_ex_jednorg")
    # amount_jedn = cursor.rowcount
    # row = cursor.fetchone()
    # amount_jedn = row[0]
    
    # for row in cursor:
    if (True):
        # emp = EmpListByOrgDesc(row[0])
        emp = EmpListByOrgDesc("Matematyki", login, password)
        amount = len(emp)
        employee_ax = random.sample(range(100000, 999999), amount)
        
        logins_len = 0
        while logins_len <= amount:
            employee_uid = []
            for u in range(10):
                employee_uid.append(random.choice(string.ascii_letters))
            employee_uids.append(''.join(employee_uid))
            logins_len += 1
            if logins_len == amount + 1:
                employee_uids_set = set(employee_uids)
                employee_uids_set_len = len(employee_uids_set)
                employee_uids_len = len(employee_uids)
                employee_uids = list(employee_uids_set)
                if employee_uids_set_len != employee_uids_len:
                    logins_len = employee_uids_set_len
            
        
        for i in range(amount):
            for key, value in emp[i].items():
                if key == "status" and value == '0':
                    break
                # elif key == "uid":
                    # employee_uids.append(value)
                # elif key == "numer_AX":
                    # employee_ax.append(value)
                elif key == "nazwisko":
                    employee_surnames.append(value)
                elif key == "imie":
                    employee_names.append(value)
                elif key == "grupa_pracownika":
                    employee_groups.append(value)
                elif key == "OrganizationKey":
                    employee_organization_keys.append(value)

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
            groups_query = u"SELECT * from auth_ex_rodzajpracownika where rodzaj = '{}'".format(employee_groups[k])
            cursor.execute(groups_query)
            to_id = cursor.fetchone()
            employee_groups[k] = to_id[0]
    '''    
    k = 0
    while row is not None:
        if employee_groups[k] == row[1]:
            employee_groups[k] = row[0]
            k += 1
        print (str(row[0]) + ' ' + row[1])
        row = cursor.fetchone()
    '''
    
    # sys.exit()
    j = 0
    all = len(employee_names)
    
    # print ("Amount: " + str(amount))
    for j in range(all):
        query = u"INSERT or REPLACE into auth_ex_pracownik(login, imie, nazwisko, email, numer_ax, czy_aktywny, jedn_org_id, rodzaj_id, password, czy_user) values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(employee_uids[j],  employee_names[j], employee_surnames[j], employee_uids[j] + "@amu.edu.pl", employee_ax[j], '1', employee_organization_keys[j], employee_groups[j], None, '0')
        cursor.execute(query)
    
    connection.commit()
    connection.close()
    

# Automatyczne uzupełnianie danych na początku oraz ich prototypowa aktualizacja
start_org()
start_typ()
start_emp()
 
connection = sqlite3.connect(database)
cursor = connection.cursor()
cursor.execute("DELETE from auth_ex_jednorg where id = 'Brak danych'")
connection.commit()
connection.close()
    
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
