#DEFAULT DATABASE
import sqlite3
def close_connection(connection):
    connection.close()

def create_and_populate():
    conn=sqlite3.connect("foldername_database.db")
    cursor=conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Folder_Name(
                id INTEGER PRIMARY KEY UNIQUE,
                folder_name TEXT NOT NULL
        )
    """)

    cursor.execute ("""
        INSERT OR IGNORE INTO Folder_Name 
        (id,folder_name) 
        VALUES
        ('1',"Textures"),
        ('2',"Project_Files"),
        ('3',"Models"),
        ('4',"Mocap_data")
                        
    """)
    conn.commit()
    cursor.close()
    return conn
    


def fetch_folder_name(connection,idx):
    cursor=connection.cursor()
    cursor.execute("SELECT folder_name FROM Folder_name where id=?",(idx,))
    folder_name=cursor.fetchone()
    cursor.close()
    return folder_name[0]

def update_folder_name(connection,idx,folder_name):
    cursor=connection.cursor()
    cursor.execute("UPDATE Folder_name SET folder_name=? where id=?",(folder_name,idx))
    connection.commit()
    cursor.close()

#END OF DEFAULT DATABASE
#FUNCTIONS TO STORE TIMESTAMP IN MEMORY

def table_inMemory(connection):
    memcursor=connection.cursor()
    memcursor.execute("""
    CREATE TABLE IF NOT EXISTS timestamps(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      timestamp TIMESTAMP
    )
    """)
    #CHANGELOG TABLE
    memcursor.execute("""
    CREATE TABLE IF NOT EXISTS changelog(
                      ID INTEGER PRIMARY KEY AUTOINCREMENT,
                      file_name TEXT,
                      file_path TEXT
    )
    """)

def insert_inMemory(connection,tstamp):
    memcursor=connection.cursor()
    memcursor.execute("""
    INSERT INTO timestamps (timestamp) VALUES (?)
    """,(tstamp,))

def get_Tstamp(connection):
    memcursor=connection.cursor()
    memcursor.execute("""
    SELECT * FROM timestamps 
    """)

    ts=memcursor.fetchone()
    return ts[1]

#END OF TEMPERORY FUNCTIONS

#START OF CHANGE LOG DATABASE CREATION


def insert_inCL(connection,fileName,filePath):
    cl_cursor=connection.cursor()

    cl_cursor.execute("""
    INSERT OR IGNORE INTO changelog(file_name,file_path)
                      VALUES (?,?)
    """,(fileName,filePath))

    cl_cursor.close()

def get_CL(connection):
    cl_cursor=connection.cursor()
    cl_cursor.execute("""
    SELECT * FROM changelog
    """)

    Changelog=cl_cursor.fetchall()
    return Changelog

# END OF CHANGELOG DATABASE
    
#START OF PROJECT SPECIFIC FOLDERNAME DATABASE
    
def psfn_createT(connection,project_name):        #psfn-> project specific folder name

    
    psfn_cursor=connection.cursor()

    psfn_cursor.execute("""
    CREATE TABLE IF NOT EXISTS {project_name} (
                        idx INTEGER PRIMARY KEY AUTOINCREMENT,
                        folder_name TEXT
    )
    """)

    psfn_cursor.execute ("""
        INSERT OR IGNORE INTO {project_name} 
        (folder_name) 
        VALUES
        ("Textures"),
        ("Project_Files"),
        ("Models"),
        ("Mocap_data")
                        
    """)
    connection.commit()
    psfn_cursor.close()

def psfn_updateName(connection,folder_name,index,project_name):
    psfn_cursor=connection.cursor()
    psfn_cursor.execute("""
        UPDATE {project_name} SET folder_name=? WHERE idx=?
    """,(folder_name,index))
    connection.commit()

def psfn_fetch_folder_name(connection,idx,project_name):
    cursor=connection.cursor()
    cursor.execute("SELECT folder_name FROM {project_name} where idx=?",(idx,))
    folder_name=cursor.fetchone()
    cursor.close()
    return folder_name[0]

def psfn_closeconn(connection):
    connection.close()

# END OF PSFN DATABASE AND TABLE