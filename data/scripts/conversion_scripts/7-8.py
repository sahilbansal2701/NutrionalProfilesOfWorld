#!/usr/bin/env python

import sqlite3
import shutil

def main():
    db_input_name = "data/7-joined_imports_exports/data.db"
    db_output_name = "data/8-aggregate/data.db"
    table_name = "diet_and_life1"
    command = "SELECT *, (other_c_pp_pd + alcohol_c_pp_pd + sugar_c_pp_pd + fat_c_pp_pd + meat_c_pp_pd + dairy_c_pp_pd + fruits_and_vegetables_c_pp_pd + starchy_roots_c_pp_pd + pulses_c_pp_pd + cereals_and_grains_c_pp_pd) as total_c_pp_pd FROM diet_and_life"
    shutil.copy(db_input_name, 
                db_output_name)
    conn = sqlite3.connect(db_output_name)
    c = conn.cursor()
    c.execute("CREATE TABLE " + table_name + " AS " + command + ";")
    c.execute("DROP TABLE diet_and_life;")
    c.execute("ALTER TABLE diet_and_life1 RENAME TO diet_and_life;")

    conn.commit()

if __name__ == '__main__':
    main()