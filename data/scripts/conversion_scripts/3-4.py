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

        print("\n[2/] Move Columns")
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

            col = input("Enter Column To Delete: ")
            if col not in columns:
                print("ERROR: Incorrect Column Entered")
                return
            c.execute("SELECT " + col + " FROM " + table_input + " GROUP BY " + col + ";")
            unique_col_values = [s[0] for s in c.fetchall()]
            if len(unique_col_values) > 1:
                print("ERROR: More than 1 Unique value for '" + col + "'")
                print(unique_col_values)
            unique_col_value = unique_col_values[0].replace(" ", "_")

            print("\nColumns:", columns)
            col1 = input("Enter Column To Attach Value To: ")
            if col1 not in columns:
                print("ERROR: Incorrect Column Entered")
                return
            
            new_col_name = col1 + "_" + unique_col_value

            c.execute("ALTER TABLE " + table_input + " RENAME COLUMN " + col1 + " TO " + new_col_name + ";")

            c.execute("ALTER TABLE " + table_input + " DROP COLUMN " + col + ";")
        
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