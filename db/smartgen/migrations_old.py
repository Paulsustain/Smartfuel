import sys
import os
import sqlite3

def run_migrations():
    '''This is where the Table and Database are created if they do not exist before'''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    conn = sqlite3.connect(dir_path+'/sqlite.db')
    c = conn.cursor()

    #MIGRATION 1  DFM LOGS  
    c.execute(""" CREATE TABLE IF NOT EXISTS dfm_logs(
                id integer PRIMARY KEY AUTOINCREMENT,
                MacAddress VARCHAR(50) NOT NULL,
                DFM_Address INTEGER NOT NULL,
                Liters FLOAT NOT NULL,
                Hours INTEGER NOT NULL,
                ForwardLiters FLOAT NOT NULL,
                BackwardLiters FLOAT NOT NULL,
                ForwardFuelRate FLOAT NOT NULL,
                BackwardFuelRate FLOAT NOT NULL,
                Average FLOAT NOT NULL,
                DifferentialFuelRate FLOAT NOT NULL,
                Temperature INTEGER NOT NULL,
                EngineRunning INTEGER NOT NULL,
                Mode VARCHAR(50) NOT NULL,
                Uploaded integer DEFAULT 0,
                TimeStamp VARCHAR(50) NOT NULL);
            """)
    
    #MIGRATION 2 Digital Input logs
    c.execute(""" CREATE TABLE IF NOT EXISTS di_hours(
                id integer PRIMARY KEY AUTOINCREMENT,
                MacAddress VARCHAR(50) NOT NULL,
                lineID integer NOT NULL,
                Status integer NOT NULL,
                Uploaded integer DEFAULT 0,
                TimeStamp VARCHAR(50) NOT NULL);
            """)
    
    #MIGRATION 3 dfm_config
    c.execute("""CREATE TABLE IF NOT EXISTS dfm_config(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug VARCHAR(255) NOT NULL,
                value VARCHAR(255) NOT NULL,
                updated_at VARCHAR(50) DEFAULT NULL);
            """)
    
    #MIGRATION 4 last inserted dfm reading
    c.execute("""CREATE TABLE IF NOT EXISTS last_inserted_dfm_reading(
                id integer PRIMARY KEY AUTOINCREMENT,
                MacAddress VARCHAR(50) NOT NULL,
                DFM_Address INTEGER NOT NULL,
                Liters FLOAT NOT NULL,
                Hours INTEGER NOT NULL,
                ForwardLiters FLOAT NOT NULL,
                BackwardLiters FLOAT NOT NULL,
                ForwardFuelRate FLOAT NOT NULL,
                BackwardFuelRate FLOAT NOT NULL,
                Average FLOAT NOT NULL,
                DifferentialFuelRate FLOAT NOT NULL,
                Temperature INTEGER NOT NULL,
                EngineRunning INTEGER NOT NULL,
                Mode VARCHAR(50) NOT NULL,
                TimeStamp VARCHAR(50) NOT NULL);
            """)
    
    #MIGRATION 5
    query = "SELECT value FROM dfm_config where slug = 'DFM_Addresses'"
    c.execute(query)
    if(len(c.fetchall()) == 0): 
        c.execute("INSERT INTO dfm_config (slug, value) VALUES('DFM_Addresses', '[111]')")
        
    #MIGRATION 6
    query = "SELECT value FROM dfm_config where slug = 'FLOWMETER_DETAILS'"
    c.execute(query)
    if(len(c.fetchall()) == 0):
        import json
        fm_details = json.dumps([{'serial_number': 'FM-TEST', 'meter_type': 'DFM', 'address': 111}])
        c.execute("INSERT INTO dfm_config (slug, value) VALUES(?, ?)", ('FLOWMETER_DETAILS', fm_details))
    
    #MIGRATION 7
    try:
        c.execute("ALTER TABLE dfm_logs ADD serial_number VARCHAR(50) DEFAULT NULL NULL")

    except :
        print("serial number likely added already to dfm_logs table")
        
    #MIGRATION 8
    try:
        c.execute("ALTER TABLE last_inserted_dfm_reading ADD serial_number VARCHAR(50) DEFAULT NULL NULL")

    except :
        print("serial number likely added already to last_inserted_dfm_reading table")
        
    conn.commit()
    conn.close()
    print('done')

def main():
    run_migrations()
 
 
if __name__ == '__main__':
    main()





