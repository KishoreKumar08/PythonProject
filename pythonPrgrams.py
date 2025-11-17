import sqlite3

import pandas as pd


class PythonSql:
    def diff_between_equals(self):
        a=[1,2,3]
        b=[1,2,3]
        c=a
        print(a==b)
        print(a is b)
        print (c is a)
        return 'look above for differences between == and is'

    def mutable_vs_immutable(self):
        a=[1,2,3]
        c="Change me if you can"
        try:
            a[0]="I changed to a string"
            print(f"{a} see i have changes my values as i am MUTABLE")
        except Exception as e:
            print(e)
        try:
            c[0]='I try'
        except:
            print(f"{c} \"You cannot change me for i am IMMUTABLE\"")

    def args_and_kwargs(self, defaultVar='***DEFAULTED***', *args, **kwargs):
        return defaultVar, args, kwargs

    def db_connection(self):
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS employees(name TEXT, id INTEGER, salary REAL)")
        cursor.execute("INSERT INTO employees VALUES (?,?,?)", ('testEmp1', 1, 12345))
        cursor.execute("INSERT INTO employees VALUES (?,?,?)", ('testEmp2', 2, 23456))
        conn.commit()
        cursor.execute("SELECT * FROM employees")
        print(cursor.fetchall())
        print(cursor.fetchone())
        print(cursor.fetchmany(3))
        df = pd.read_sql('SELECT * FROM employees', conn)
        print(df)
        conn.close()

    def fetch_pandas_data(self):
        conn = sqlite3.connect('test.db')
        df = pd.read_sql_query("SELECT * FROM employees",conn)
        return df


obj = PythonSql()
print(obj.diff_between_equals())
print(obj.mutable_vs_immutable())
print(obj.args_and_kwargs([123,456,'hey'],['name','age'], name='lots', lots='name'))
print(obj.args_and_kwargs())
print(obj.db_connection())
print(obj.fetch_pandas_data())
