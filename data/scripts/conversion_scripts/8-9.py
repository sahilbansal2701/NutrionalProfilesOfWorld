#!/usr/bin/env python

import sqlite3
import shutil

def main():
    db_input_name = "data/8-aggregate/data.db"
    db_output_name = "data/9-percentages/data.db"
    command = "SELECT *, (CAST(other_c_pp_pd AS FLOAT)/total_c_pp_pd * 100) as other_percent_pp_pd FROM diet_and_life"
    command1 = "SELECT *, (CAST(sugar_c_pp_pd AS FLOAT)/total_c_pp_pd * 100) as sugar_percent_pp_pd FROM diet_and_life"
    command2 = "SELECT *, (CAST(fat_c_pp_pd AS FLOAT)/total_c_pp_pd * 100) as fat_percent_pp_pd FROM diet_and_life"   
    command3 = "SELECT *, (CAST(meat_c_pp_pd AS FLOAT)/total_c_pp_pd * 100) as meat_percent_pp_pd FROM diet_and_life"    
    command4 = "SELECT *, (CAST(dairy_c_pp_pd AS FLOAT)/total_c_pp_pd * 100) as dairy_percent_pp_pd FROM diet_and_life"    
    command5 = "SELECT *, (CAST(fruits_and_vegetables_c_pp_pd AS FLOAT)/total_c_pp_pd * 100) as fruits_and_vegetables_percent_pp_pd FROM diet_and_life" 
    command6 = "SELECT *, (CAST(starchy_roots_c_pp_pd AS FLOAT)/total_c_pp_pd * 100) as starchy_roots_percent_pp_pd FROM diet_and_life"    
    command7 = "SELECT *, (CAST(pulses_c_pp_pd AS FLOAT)/total_c_pp_pd * 100) as pulses_percent_pp_pd FROM diet_and_life"    
    command8 = "SELECT *, (CAST(cereals_and_grains_c_pp_pd AS FLOAT)/total_c_pp_pd * 100) as cereals_and_grains_percent_pp_pd FROM diet_and_life"    
    command9 = "SELECT *, (CAST(alcohol_c_pp_pd AS FLOAT)/total_c_pp_pd * 100) as alcohol_percent_pp_pd FROM diet_and_life"

    shutil.copy(db_input_name, 
                db_output_name)
    conn = sqlite3.connect(db_output_name)
    c = conn.cursor()

    c.execute("CREATE TABLE diet_and_life1 AS " + command + ";")
    c.execute("DROP TABLE diet_and_life;")
    c.execute("ALTER TABLE diet_and_life1 RENAME TO diet_and_life;")

    c.execute("CREATE TABLE diet_and_life1 AS " + command1 + ";")
    c.execute("DROP TABLE diet_and_life;")
    c.execute("ALTER TABLE diet_and_life1 RENAME TO diet_and_life;")

    c.execute("CREATE TABLE diet_and_life1 AS " + command2 + ";")
    c.execute("DROP TABLE diet_and_life;")
    c.execute("ALTER TABLE diet_and_life1 RENAME TO diet_and_life;")

    c.execute("CREATE TABLE diet_and_life1 AS " + command3 + ";")
    c.execute("DROP TABLE diet_and_life;")
    c.execute("ALTER TABLE diet_and_life1 RENAME TO diet_and_life;")

    c.execute("CREATE TABLE diet_and_life1 AS " + command4 + ";")
    c.execute("DROP TABLE diet_and_life;")
    c.execute("ALTER TABLE diet_and_life1 RENAME TO diet_and_life;")

    c.execute("CREATE TABLE diet_and_life1 AS " + command5 + ";")
    c.execute("DROP TABLE diet_and_life;")
    c.execute("ALTER TABLE diet_and_life1 RENAME TO diet_and_life;")

    c.execute("CREATE TABLE diet_and_life1 AS " + command6 + ";")
    c.execute("DROP TABLE diet_and_life;")
    c.execute("ALTER TABLE diet_and_life1 RENAME TO diet_and_life;")

    c.execute("CREATE TABLE diet_and_life1 AS " + command7 + ";")
    c.execute("DROP TABLE diet_and_life;")
    c.execute("ALTER TABLE diet_and_life1 RENAME TO diet_and_life;")

    c.execute("CREATE TABLE diet_and_life1 AS " + command8 + ";")
    c.execute("DROP TABLE diet_and_life;")
    c.execute("ALTER TABLE diet_and_life1 RENAME TO diet_and_life;")

    c.execute("CREATE TABLE diet_and_life1 AS " + command9 + ";")
    c.execute("DROP TABLE diet_and_life;")
    c.execute("ALTER TABLE diet_and_life1 RENAME TO diet_and_life;")

    conn.commit()

if __name__ == '__main__':
    main()