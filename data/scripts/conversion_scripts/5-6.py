#!/usr/bin/env python

import sqlite3
import shutil

def parse_tuple(string):
    if "," not in string:
        return [string[1:][:-1]]
    else:
        split_string = string.split(",")
        split_string = [s.strip() for s in split_string]
        split_string[0] = split_string[0][1:]
        split_string[-1] = split_string[-1][:-1]
        return split_string

def print_list_index(lst):
    print("[")
    for i in range(len(lst)):
        print("\t", i, ": ", lst[i])
    print("]")

def main():
    try:
        print("[1/] Copy DB File")
        db_input_name = input("Enter Input DB Path: ")
        if db_input_name[-3:] != ".db":
            print("\nERROR: Input needs to be a DB file")
            return
        if db_input_name == "":
            raise EOFError        

        db_output_name = input("Enter Output DB Path: ")
        if db_output_name[-3:] != ".db":
            print("\nERROR: Input needs to be a DB file")
            return
        if db_output_name == "":
            raise EOFError   

        shutil.copy(db_input_name, db_output_name)

        conn = sqlite3.connect(db_output_name)
        c = conn.cursor()

        print("\n[2/] Join Tables")
        c.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
        tables = [s[0] for s in c.fetchall()]
        new_table_name = input("Enter New Table Name: ")
        if new_table_name in tables:
            print("ERROR: Table Name Already Exists")
            return
        
        print("Tables: ", tables)
        com = input("Enter SQL Command to Create New Table From: ")

        if com == "":
            print("ERROR: Need to Input a SQL Command")
            return
        if "JOIN" not in com:
            print("ERROR: There should be a JOIN in the command")
            return
    
        c.execute("CREATE TABLE " + new_table_name + " AS " + com + ";")

        print("Tables: ", tables)

        tables_to_remove = input("Enter Tables to Remove: ").lower()
        if tables_to_remove == "":
            print("\nERROR: Tables to Remove Not Entered")
            return
        tables_to_remove = parse_tuple(tables_to_remove)
        for tab in tables_to_remove:
            if tab not in tables:
                print("\nERROR: Table '" + tab + "' Not A Valid Table Name")
                return
            c.execute("DROP TABLE " + tab + ";") 

        print("\n[3/] Commit")
        conn.commit()

        print("[4/] DONE")
    except EOFError:
        print("\nERROR: No Input Given")
        return

if __name__ == '__main__':
    main()