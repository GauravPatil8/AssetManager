#DEFAULT DATABASE
import sqlite3
def close_connection(connection):
    connection.close()

def create_and_populate(file_path):
    conn=sqlite3.connect(file_path)
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
        ('4',"Mocap_data"),
        ('5',"Material_files"),
        ('6',"Video_files"),
        ('7',"Audio_files")
                        
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

