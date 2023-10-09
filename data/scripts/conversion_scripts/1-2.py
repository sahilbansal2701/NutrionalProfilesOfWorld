#!/usr/bin/env python

import sqlite3
import re

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
    COMMA_SPLIT = re.compile(',(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)')
    try:
        print("[1/] Input CSV Files")
        csv_paths = []
        while(1):
            csv_input = input("Enter CSV File Path: ")

            if csv_input == "":
                break

            if csv_input[-4:] != ".csv":
                print("\nERROR: Input needs to be a CSV file")
                return
            
            csv_paths.append(csv_input)
        
        if len(csv_paths) == 0:
            print("Zero Paths Entered")
            return
        
        print("[2/] Creating a DB File")
        db_name = input("Enter DB Path: ")
        if db_name == "":
            raise EOFError
        if db_name[-3:] != ".db":
            print("\nERROR: Input needs to be a DB file")
            return
        
        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        # Deleting Any Tables From db so it looks like creating new file if file already exists
        c.execute("SELECT name FROM sqlite_schema WHERE type='table';")
        tables = c.fetchall()
        for table, in tables:
            sql = "DROP TABLE " + table + ";"
            c.execute(sql)


        print("\n[3/] Create Tables")
        for i in range(len(csv_paths)):

            # Read CSV File
            split_data = []
            with open(csv_paths[i], 'r') as f:
                for line in f:
                    split_data.append(re.split(COMMA_SPLIT, line))
        
            header = split_data[0]
            data = split_data[1:]
            
            # Set Table Name
            table_name = input("Enter Table Name for " + csv_paths[i] + ": ")
            if table_name == "":
                raise EOFError
            if "-" in table_name:
                print("ERROR: Table Name Cannot Contain Character '-'")
                return
            
            # Fix Column Names
            header = [s.strip().lower() for s in header]
            print("Columns: ")
            print_list_index(header)
            headers_to_rename = input("Enter Index of Columns You Would Like To Rename: ")
            if headers_to_rename == "":
                raise EOFError
            headers_to_rename = parse_tuple(headers_to_rename)
            headers_to_rename_temp = []
            for col in headers_to_rename:
                try:
                    col = int(col)
                except ValueError:
                    print("\nERROR: Please Enter an Integer for Index")
                    return
                if col < 0 or col >= len(header):
                    print("\nERROR: Please Enter a Valid Index")
                    return
                headers_to_rename_temp.append(col)
            headers_to_rename = headers_to_rename_temp
                
            headers_new_name = input("What are the Columns New Names? ")
            if headers_new_name == "":
                raise EOFError
            headers_new_name = parse_tuple(headers_new_name)
            
            if len(headers_to_rename) != len(headers_new_name):
                print("ERROR: Number of Columns to Rename, and Number of New Names Length Do Not Match")
                return
            
            for i in range(len(headers_to_rename)):
                header[headers_to_rename[i]] = headers_new_name[i].lower()

            # Create Table Specifics
            print("Columns: ", header)
            print("Printing Example Row: ", [s.strip() for s in data[0]])
            specifics = input("Enter Columns' SQL Specifics: ")
            if headers_new_name == "":
                raise EOFError
            specifics = parse_tuple(specifics)

            if len(specifics) != len(header):
                print("ERROR: Number of Specifics Entered, and Number of Columns Do Not Match")
                return

            # Enter Primary Key
            print("Columns: ", header)
            primary_key = input("Enter Primary Key: ").lower()
            if primary_key == "":
                print("\nERROR: Primary Key Not Entered")
                return
            primary_key_cols = parse_tuple(primary_key)
            for key in primary_key_cols:
                if key not in header:
                    print("\nERROR: Primary Key Columns '" + key + "' Not A Column Name")
                    return

            # Create Table
            create_sql = "CREATE TABLE " + table_name + "("

            # Create Table: Attribute Types
            for i in range(len(header)):
                create_sql += header[i] + " " + specifics[i] + ", "

            # Create Table: Primary Key
            create_sql += "PRIMARY KEY " + primary_key

            create_sql += ");"
            
            try:
                c.execute(create_sql)
            except Exception as e:
                print("\nERROR: Table Creation Failed:", e)
                print(create_sql)
                return

            # Insert Values
            insert_sql = "INSERT INTO " + table_name + " VALUES ("
            for i in range(len(header)):
                insert_sql += "?, "
            insert_sql = insert_sql[:-2] + ")"
            for row in data:
                # want to remove double quotes around faostat data entries
                row = [s.strip().lower().replace("\"", "") for s in row]

                # specific check for our world in data datasets
                if "less developed regions" in row[0]:
                    continue

                try:
                    c.execute(insert_sql, row)
                except Exception as e:
                    print("ERROR: Inserting Values Failed:", e)
                    print("Insert SQL: ", insert_sql)
                    print("Columns: ", header)
                    print("Row of Data Attempting To Insert: ", row)
                    return

        print("\n[8/] Commit")
        conn.commit()

        print("[9/] DONE")
    except EOFError:
        print("\nERROR: No Input Given")
        return

if __name__ == '__main__':
    main()