

class SQLQueries:
    CREATE_DATABASE = '''CREATE TABLE IF NOT EXISTS work (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        work_completed INTEGER)'''
    GET_WORK_BY_DATE = 'SELECT * FROM work WHERE date=?'
    GET_TODAYS_WORK = 'SELECT work_completed FROM work WHERE date=?'
    GET_ALL_WORK_COMPLETED = 'SELECT date, work_completed FROM work'
    ADD_WORK_BY_DATE = 'INSERT INTO work (date, work_completed) VALUES (?, ?)'
    UPDATE_WORK_BY_DATE = 'UPDATE work SET work_completed=? WHERE date=?'
