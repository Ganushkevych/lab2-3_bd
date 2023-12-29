import psycopg
import csv
from sqlalchemy import create_engine, and_, cast, Double
from sqlalchemy.orm import sessionmaker
from models import Student, Register, Result_Ukr, EO, PT_Ukr


def create_connection_string(filename):
    with open(filename) as f:
        lines = f.readlines()
        database_name, user, password = lines[0].strip(), lines[1].strip(), lines[2].strip()
        return f"postgres://{user}:{password}@localhost:5432/{database_name}"


def connect_to_db(connection_str):
    try:
        conn = psycopg.connect(connection_str)
        print("Connection to PostgreSQL successful!")
        return conn
    except psycopg.Error as e:
        print(f"Error: Unable to connect to the database: {e}")
        return None


def read_data_from_csv(filename):
    data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


def create_table(conn, header):
    if conn is not None:
        try:
            cur = conn.cursor()
            columns = ', '.join(f"{col} VARCHAR(255)" for col in header)
            create_query = f"CREATE TABLE IF NOT EXISTS ZNO2019 ({columns})"
            cur.execute(create_query)
            conn.commit()
            print("Table created successfully!")
        except psycopg.Error as e:
            print(f"Error: Unable to create table: {e}")
        finally:
            cur.close()


def insert_data_to_db(data, conn):
    if conn is not None:
        try:
            cur = conn.cursor()
            columns = ', '.join(data[0].keys())
            placeholders = ', '.join(['%(' + column + ')s' for column in data[0]])
            query = f"INSERT INTO ZNO2019 ({columns}) VALUES ({placeholders})"
            cur.executemany(query, data)
            conn.commit()
            print("Data inserted successfully!")
        except psycopg.Error as e:
            print(f"Error: Unable to insert data into the table: {e}")
        finally:
            cur.close()
            conn.close()
            print("Database connection closed.")


def drop_table(conn):
    if conn is not None:
        try:
            cur = conn.cursor()
            create_query = f"DROP TABLE IF EXISTS ZNO2019"
            cur.execute(create_query)
            conn.commit()
            print("Table droped successfully!")
        except psycopg.Error as e:
            print(f"Error: Unable to drop table: {e}")
        finally:
            cur.close()


def some_execution():
    # Create connection string based on settings file
    connection_str = create_connection_string("settings.txt")

    # Connect to the database
    conn = connect_to_db(connection_str)

    if conn is not None:
        try:
            cur = conn.cursor()
            create_query = f"SELECT * FROM ZNO2019 WHERE engball12 = '12'"
            cur.execute(create_query)
            print(cur.fetchone())
        except psycopg.Error as e:
            print(f"Error: {e}")
        finally:
            cur.close()


def create_and_fill_table():
    # Create connection string based on settings file
    connection_str = create_connection_string("settings.txt")

    # Connect to the database
    conn = connect_to_db(connection_str)

    # Read data from the CSV file
    data_from_csv = read_data_from_csv('opendatazno2019.csv')

    # Extract header from CSV
    csv_header = list(data_from_csv[0])

    # Create table based on CSV header
    create_table(conn, csv_header)

    # Insert data into the database
    insert_data_to_db(data_from_csv, conn)


# Створення підключення до бази даних PostgreSQL
# connection_str = create_connection_string("settings.txt")
engine = create_engine('postgresql://postgres:postgres@localhost:5432/ZNO2019')

Session = sessionmaker(bind=engine)
session = Session()


# Параметризований запит до БД
def get_students():
    students_with_ball_range = session.query(Student).join(Student.result_ukr).filter(
        and_(
            Result_Ukr.UkrBall100 != 'null',
            cast(Result_Ukr.UkrBall100, Double) >= 197,
            cast(Result_Ukr.UkrBall100, Double) <= 200
        )
    ).all()

    for student in students_with_ball_range:
        print(f"Student ID: {student.id}, UkrBall100: {student.result_ukr.UkrBall100}")


# Додавання нового студента з валідацією (якщо потрібно)
def add_student(out_id, birth, sex_type_name, class_profile_name, class_lang_name, eo_name,
                eo_type_name, eo_reg_name, eo_area_name, eo_ter_name, eo_parent, ukr_pt_name,
                ukr_pt_reg_name, ukr_pt_area_name, ukr_pt_ter_name, reg_name, area_name,
                ter_name, reg_type_name, ter_type_name, ukr_test, ukr_test_status, ukr_ball100,
                ukr_ball12, ukr_ball, ukr_adapt_scale):
    new_result_ukr = Result_Ukr(
        UkrTest=ukr_test,
        UkrTestStatus=ukr_test_status,
        UkrBall100=ukr_ball100,
        UkrBall12=ukr_ball12,
        UkrBall=ukr_ball,
        UkrAdaptScale=ukr_adapt_scale
    )
    new_register = Register(
        RegName=reg_name,
        AreaName=area_name,
        TerName=ter_name,
        RegTypeName=reg_type_name,
        TerTypeName=ter_type_name
    )
    new_eo = EO(
        EOName=eo_name,
        EOTypeName=eo_type_name,
        EORegName=eo_reg_name,
        EOAreaName=eo_area_name,
        EOTerName=eo_ter_name,
        EOParent=eo_parent
    )
    new_pt_ukr = PT_Ukr(
        UkrPTName=ukr_pt_name,
        UkrPTRegName=ukr_pt_reg_name,
        UkrPTAreaName=ukr_pt_area_name,
        UkrPTTerName=ukr_pt_ter_name
    )
    new_student = Student(
        OutId=out_id,
        Birth=birth,
        SexTypeName=sex_type_name,
        ClassProfileName=class_profile_name,
        ClassLangName=class_lang_name,
    )
    session.add(new_eo)
    session.add(new_register)
    session.add(new_pt_ukr)
    session.add(new_result_ukr)
    session.add(new_student)
    session.commit()


# Видалення студента за його id
def delete_student(student_id):
    student = session.query(Student).filter_by(id=student_id).first()
    if student:
        session.delete(student)
        session.commit()
    eo = session.query(EO).filter_by(id=student_id).first()
    if eo:
        session.delete(eo)
        session.commit()
    pt_ukr = session.query(PT_Ukr).filter_by(id=student_id).first()
    if pt_ukr:
        session.delete(pt_ukr)
        session.commit()
    register = session.query(Register).filter_by(id=student_id).first()
    if register:
        session.delete(register)
        session.commit()
    result_ukr = session.query(Result_Ukr).filter_by(id=student_id).first()
    if result_ukr:
        session.delete(result_ukr)
        session.commit()


if __name__ == '__main__':
    """add_student"') DROP TABLE student; --", "new", "new", "new", "new", "new", "new", "new", "new",
                "new", "new", "new", "new", "new", "new", "new", "new", "new", "new",
                "new", "new", "new", "new", "new", "new", "new")"""
    # get_students()
    # some_execution()
    delete_student(353820)
