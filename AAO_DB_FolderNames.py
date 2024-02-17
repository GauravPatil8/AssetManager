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

