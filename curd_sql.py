import sqlite3
import pandas as pd

db_path = "employees.db"

expected_data = [
    {"id": 1, "name": "Lti", "salary": 11000},
    {"id": 3, "name": "Tree", "salary": 30000}
]


def create_table():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS employees")
        cursor.execute("CREATE TABLE IF NOT EXISTS employees (name TEXT, id INTEGER, salary REAL)")
        conn.commit()

def insert_employee(name,id,salary):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees VALUES(?,?,?)",(name,id,salary))
        conn.commit()

def get_employee():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        data = cursor.execute("SELECT id, name, salary FROM employees")
        conn.commit()
        df = pd.DataFrame(data)
    return df

def update_employee(query):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

def delete_employee(query):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

def verify_db_expected_data_raw(expected_data):
    for index,dict in enumerate(expected_data):
        for k,v in dict.items():
            expected_data[index][k] = str(v).lower()
    db_data = get_employee()
    exp_df = pd.DataFrame(expected_data)
    db_data = db_data.rename(columns={0:'id',1:'name',2:"salary"})
    db_data['salary']=db_data['salary'].astype(int)
    db_data = db_data.astype(str)
    exp_df = exp_df.astype(str)
    assert db_data.equals(exp_df)

def verify_db_exp(expected_data):
    db_data = get_employee()
    db_data = db_data.rename(columns={0:"id", 1:"name", 2:"salary"})
    db_data['salary'] = db_data['salary'].astype(int)
    db_data = db_data.to_dict(orient='records')
    for i,dict in enumerate(db_data):
        for k,v in dict.items():
            if k == 'name':
                db_data[i][k] = str(v).title()
    assert db_data == expected_data
    if db_data == expected_data:
        print("Test passed")
    else:
        raise Exception("Test failed")

def verify_db(expected):
    with sqlite3.connect(db_path) as conn:
        db_df = pd.read_sql_query("SELECT id, name, salary FROM employees", conn) #pay attention
    db_df['salary'] = db_df['salary'].astype(int)
    db_df['name'] = db_df['name'].str.title()  # Normalize case
    expected_df = pd.DataFrame(expected)
    print(db_df)
    print(expected_df)
    if db_df.equals(expected_df):
        print("✅ Test Passed: DB matches expected data")
    else:
        print("❌ Test Failed: Mismatch found")


try:
    create_table()
    insert_employee("lti", 1, "10000")
    insert_employee("mind", 2, "20000")
    insert_employee("tree", 3, "30000")
    print(get_employee())
    update_employee("UPDATE employees SET salary=salary+1000 WHERE id=1")
    delete_employee("DELETE FROM employees WHERE id=2")
    print(get_employee())
    # verify_db_expected_data_raw(expected_data)
    verify_db_exp(expected_data)
    verify_db(expected_data) #gave by copilot (check the query and method used)


except Exception as e:
    print(f"Error: {e}")



