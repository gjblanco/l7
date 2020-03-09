import psycopg2
from datetime import datetime
import io
import psycopg2.extras

_db = None

def initdb(app):
    print("INIT DB...")
    global _db
    app.config.from_object("project.config.Config")
    _db = psycopg2.connect(
        host=app.config['DB_HOST'],
        database=app.config['DB_NAME'], 
        user=app.config['DB_USER'], 
        password=app.config['DB_PASSWORD'])

def drop_all():
    commands = (
        """
        DROP TABLE IF EXISTS uploaded_data
        """,
    )
    cur = _db.cursor()
    
    for command in commands:
        cur.execute(command)
    _db.commit()

def create_all():
    print("Creating tables...")
    commands = (
        """
        CREATE TABLE uploaded_data (
            filename VARCHAR,
            file_id SERIAL,
            contents TEXT,
            piece_id SERIAL PRIMARY KEY,
            is_last_piece BOOLEAN,
            last_upload_time TIMESTAMP 
        )
        """,
    )
    cur = _db.cursor()
    # create table one by one
    for command in commands:
        print('EXECUTING => ', command)
        res = cur.execute(command)
    _db.commit()
    print("All tables created")

def list_files():
    command = """
       SELECT file_id, filename, min(last_upload_time) as upload_time
       FROM uploaded_data
       GROUP BY file_id, filename
       ORDER BY upload_time DESC
       LIMIT 5 
    """
    cur = _db.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute(command)
    rows = cur.fetchall()

    ret = []
    for row in rows:
        ret.append({'fileId': row['file_id'], 'filename': row['filename'], 'uploadTime': row['upload_time']})
    return ret

def read_file_linebyline(fileid):
    cur = _db.cursor(cursor_factory = psycopg2.extras.DictCursor)
    lastpieceid = -1
    islastpiece = False
    chunks = ['']
    while(islastpiece == False):
        cur.execute("""
                SELECT is_last_piece, piece_id, filename, contents 
                    FROM uploaded_data 
                    WHERE file_id = %s AND piece_id > %s
                ORDER BY piece_id
                LIMIT 1
                """, (fileid, lastpieceid))
        row = cur.fetchall()
        if(len(row) == 0):
            break;
        islastpiece = row[0]['is_last_piece']
        lastpieceid = row[0]['piece_id']
        newchunks = (chunks[len(chunks) - 1] + row[0]['contents']).split('\n')
        chunks.pop()
        chunks.extend(newchunks)
        current_index = 0
        while(current_index < len(chunks) - 1):
            yield chunks[current_index]
            current_index += 1
        chunks = [chunks[current_index]]
    if(len(chunks[0].strip()) > 0):
        yield chunks[0]
        
        


def save_file_piece(filename, contents, order, islastpiece, fileid=None):
    print('PARAMSSAVEFILEPIECE', filename, contents, order, islastpiece, fileid)
    cur = _db.cursor()
    query = """
        INSERT INTO uploaded_data(filename, file_id, contents, is_last_piece, last_upload_time)
        VALUES (%s, {0}, %s, %s, %s)
        RETURNING file_id
    """.format('DEFAULT' if fileid is None else '%s')
    params = (filename, contents, islastpiece, datetime.now()) if fileid is None else (filename, fileid, contents, islastpiece, datetime.now())
    cur.execute(query, params)
    ret = cur.fetchall()
    return ret
