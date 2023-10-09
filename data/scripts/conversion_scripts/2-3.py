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

        print("\n[2/] Remove Columns")
        # Get All Tables We Want to Work With
        c.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
        tables = [s[0] for s in c.fetchall()]
        print("Tables:", tables)
        table_names = 0
        while(1):
            try:
                table_input = input("Enter Table Name File Path: ")
            except EOFError:
                break
            if table_input == "":
                break
            if table_input not in tables:
                print("\nERROR: Incorrect Table Name Entered")
                return
            table_names += 1
            c.execute("PRAGMA table_info(" + table_input + ")")
            columns = [s[1] for s in c.fetchall()]
            print("Columns:")
            print_list_index(columns)
            cols = input("Enter Columns to Remove: ").lower()
            if cols == "":
                print("\nERROR: Columns to Remove Not Entered")
                return
            cols = parse_tuple(cols)
            for col in cols:
                try:
                    col = int(col)
                except ValueError:
                    print("\nERROR: Please Enter an Integer for Index")
                    return
                if columns[col] not in columns:
                    print("\nERROR: Column '" + col + "' Not A Valid Column Name")
                    return
                c.execute("ALTER TABLE " + table_input + " DROP COLUMN " + columns[col] + ";") 
                
        if table_names == 0:
            print("\nZero Paths Entered")
            return

        print("\n[3/] Commit")
        conn.commit()

        print("[4/] DONE")
    except EOFError:
        print("\nERROR: No Input Given")
        return

if __name__ == '__main__':
    main()