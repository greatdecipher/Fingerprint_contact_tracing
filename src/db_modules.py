import sqlite3
import datetime


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

# fingerprint = convertToBinaryData("some_fingerprint.bin")


db_name = '/home/pi/Fingerprint_Contact_Tracing/Contact_Tracing.db'


def start_db():
    try:
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print("SQLite Database Version is: ", record)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def get_row_total():

    try:
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()

        sql_fetch_blob_query = """SELECT COUNT(*) from Contact"""

        cursor.execute(sql_fetch_blob_query)
        cur_result = cursor.fetchone()

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
        return False
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            return cur_result[0]


def start_table():
    try:
        sqliteConnection = sqlite3.connect(db_name)
        sqlite_create_table_query = '''CREATE TABLE Contact (
                                    id INTEGER NOT NULL,
                                    name TEXT NOT NULL,
                                    email TEXT NOT NULL,
                                    address TEXT NOT NULL,
                                    gender TEXT NOT NULL,
                                    phone TEXT NOT NULL,
                                    location_record TEXT NOT NULL,
                                    date TEXT NOT NULL,
                                    fingerprint BLOB NOT NULL
                                    );'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")


def insertdata(name, email, address, gender, phone, location_record, date, fingerprint):
    try:
        id = get_row_total()+1
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO Contact
                                  (id ,name, email, address, gender, phone, location_record, date, fingerprint) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        # empPhoto = convertToBinaryData(photo)
        # resume = convertToBinaryData(resumeFile)
        # Convert data into tuple format
        data_tuple = (id, name, email, address, gender, phone,
                      location_record, date, fingerprint)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert  data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")


def get_fingerprint_data(id_num):
    try:
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()

        sql_fetch_blob_query = """SELECT * from Contact where id = ?"""

        cursor.execute(sql_fetch_blob_query, (id_num,))

        record = cursor.fetchall()

        for row in record:
            # print("Id = ", row[0], "Name = ", row[1])

            name = row[1]
            email = row[2]
            location = row[3]
            gender = row[4]
            contact_num = row[5]
            location_list = row[6]
            date = row[7]

            # print("Done Loading Fingerprint")
            # writeTofile(fingerprint_data, "fingerprint_data.bin")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
        return False
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            return name, email, location, gender, contact_num, location_list, date


def save_fingerprint(id_num):
    try:
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()

        sql_fetch_blob_query = """SELECT fingerprint from Contact where id = ?"""

        cursor.execute(sql_fetch_blob_query, (id_num,))

        record = cursor.fetchall()

        writeTofile(
            record[0][0], "/home/pi/Fingerprint_Contact_Tracing/fingerprint_data.bin")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
        return False
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def get_list_fingerprint():

    try:
        sqliteConnection = sqlite3.connect(db_name)
        sqliteConnection.row_factory = lambda cursor, row: row[0]
        cursor = sqliteConnection.cursor()
        sql_fetch_blob_query = """SELECT fingerprint from Contact"""

        record = cursor.execute(sql_fetch_blob_query).fetchall()

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
        return False
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            return tuple(record)


def update_location(id, location):

    try:
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()

        sqlite_select_query = """SELECT location_record from Contact where id = {}""".format(
            id)
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        def Convert(string):
            li = list(string.split("~"))
            return li

        def listToString(s):

            # initialize an empty string
            str1 = "~"

            # return string
            return (str1.join(s))

        location_list = Convert(records[0][0])

        if location not in location_list:

            print("Updating Location")

            location_list.append(location)
            location_string = listToString(location_list)

            sqlite_update_query = """Update Contact set location_record = '{}' where id = {}""".format(
                location_string, id)
            cursor.execute(sqlite_update_query)
            sqliteConnection.commit()

        print("Updating Time in")

        sqlite_update_query = """Update Contact set date = '{}' where id = {}""".format(
            datetime.datetime.now(), id)
        cursor.execute(sqlite_update_query)
        sqliteConnection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
