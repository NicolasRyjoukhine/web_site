import sqlite3

forhobbies = ['hockey', 'coding']

def get_connection():
    return sqlite3.connect('register.db')


def initdb():
    conn = sqlite3.connect('register.db')
    cur = conn.cursor()
    create_register_sql = "CREATE TABLE IF NOT EXISTS register (name varchar NOT NULL,\
                                        familly_name varchar NOT NULL,\
                                        age varchar NOT NULL,\
                                        birthday varchar NOT NULL,\
                                        email varchar NULL,\
                                        password varchar NULL,\
                                        register_id INTEGER PRIMARY KEY autoincrement)"
    print(create_register_sql)
    cur.execute(create_register_sql)

    create_hobbies_sql = "CREATE TABLE IF NOT EXISTS hobbies (name varchar NOT NULL,\
                                        hobby_id INTEGER PRIMARY KEY autoincrement)"
    print(create_hobbies_sql)
    cur.execute(create_hobbies_sql)

    create_register_hobby_sql = "CREATE TABLE IF NOT EXISTS register_hobby (register_id INTEGER,\
                                               hobby_id INTEGER,\
                                               PRIMARY KEY (register_id, hobby_id),\
                                                   FOREIGN KEY (register_id),\
                                               REFERENCES register (register_id),\
                                                   FOREIGN KEY (hobby_id),\
                                               REFERENCES hobbies (hobby_id))"
    print(create_register_hobby_sql)
    cur.execute(create_hobbies_sql)
#    conn.execute("CREATE TABLE IF NOT EXISTS register_img (image IMAGE)")
    cur.close()
    conn.close()


#check if exists#
#save if not#
#take idhobby add idregister

def save(name, family, age, birthday, hobby_name_register, new_hobby_name, email, password):
    conn = get_connection()
    cur = conn.cursor()
    total_hobbies = []
    total_hobbies.append(hobby_name_register)
    total_hobbies.append(new_hobby_name)
    '''
    register_hobbyid = cur.execute("SELECT register_id FROM register")
    i = []
    for row in register_hobbyid:
        i.append(row)
    insertIntoRegister_hobby1 = i[len(i)-1]

    hobbyid = cur.execute("SELECT hobby_id FROM register")
    b = []
    for row in hobbyid:
        b.append(row)
    insertIntoRegister_hobby2 = b[len(b)-1]
    '''
    ########################################hobbyGetId = [cur.execute("SELECT hobby_id FROM hobbies WHERE hobby_id = (?)", ([len(hobbyGetId)-1]))]
    checkHobby = cur.execute("SELECT count(*) FROM hobbies WHERE name=(?)", (new_hobby_name,))
    if checkHobby.fetchone()[0] == 0:
        cur.execute("INSERT INTO hobbies (name) VALUES (?)", (new_hobby_name,))

    if check_name(name, cur):
        cur.execute("UPDATE register SET name = (?),"
                                    "familly_name = (?),"
                                    "age = (?),"
                                    "birthday = (?),"
                                    "email = (?),"
                                    "password = (?) WHERE name = (?)",
                                    (name,family,age,birthday,email,password,name))
        for hobby in total_hobbies:
            if hobby != checkHobby[hobby]:
                for current_hobby in checkHobby:
                    hobby_last_id = cur.execute("SELECT hobby_id FROM hobbies WHERE name=(?)", (current_hobby,))
                    register_last_id = cur.execute("SELECT register_id FROM register WHERE email=(?)", (email,))
                    cur.execute("UPDATE register_hobby SET hobby_id, register_id VALUES (?,?)",(hobby_last_id, register_last_id,))
                    cur.execute("UPDATE hobbies SET name VALUES (?)", (current_hobby,))
    else:
        cur.execute("INSERT INTO register (name, familly_name, age, birthday, email, password) VALUES (?,?,?,?,?,?)",
                    (name, family, age, birthday, email, password,))
        #cur.execute("INSERT INTO hobbies (name) VALUES (?)", (new_hobby_name))
        hobby_last_id_new = cur.execute("SELECT hobby_id FROM hobbies WHERE name=(?)", (new_hobby_name,))
        register_last_id_new = cur.execute("SELECT register_id FROM register WHERE email=(?)", (email,))
        cur.execute("INSERT INTO register_hobby(register_id, hobby_id) values(?,?)", (str(register_last_id_new),
                                                                                      str(hobby_last_id_new),))

    forhobbies.append(hobby_name_register)
    forhobbies.append(new_hobby_name)
    conn.commit()
    cur.close()
    conn.close()


def check_name(name_to_check, cur):
    name_list = cur.execute("SELECT name FROM register")
    #name_familly_list = c.execute("SELECT familly_name FROM register")
    #to_check_name = (name_list + " " + name_familly_list)
    for name in name_list:
        if name == name_to_check:
            return True
    return False


def return_data():
    conn = get_connection()
    cur = conn.cursor()
    return_cur = cur.execute("SELECT name, familly_name, age, birthday, email FROM register")
    result = []
    global forhobbies
    for ho in forhobbies:
        if ho == cur.execute("SELECT name FROM register"):
            cur.execute("INSERT INTO hobbies (name) VALUES (?)", (forhobbies,))
    returenedHobby = cur.execute("SELECT r.name, h.name FROM register r, hobbies h, register_hobby rh "
                                 "WHERE r.register_id = rh.register_id AND h.hobby_id = rh.hobby_id")
    for row in returenedHobby.fetchall():
        result.append({'hobby':row})
    for row in return_cur.fetchall():
        result.append({'name': row[0],
                       'familly': row[1],
                       'age': row[2],
                       'birthday':row[3],
                       'email': row[5]})
    cur.close()
    conn.close()
    print(result)
    return result




def delete():
    pass





#select r.name, h.name FROM register r, hobbies h , register_hobby rh WHERE r.register_id = rh.register_id and
#h.hobby_id = rh.hobby_id ;


