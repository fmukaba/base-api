import psycopg2

from schemas import Message

# todo: put into config file
db_params = {
    "host": "",
    "database": "",
    "user": "",
    "password": "",
    "port": ""
}

try:
    conn = psycopg2.connect(**db_params)
    curr = conn.cursor()
except (Exception, psycopg2.Error) as error:
    print(f"Error connecting to the database: {error}")


def create_message(message: Message):
    try:
        query = f"INSERT INTO Messages (group_id, sender_id, message) VALUES (%d, %d, %s);"
        curr.execute(query, (message.group_id, message.sender_id, message.message))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")


def delete_message(message_id: int):
    try:
        query = f"DELETE FROM Messages WHERE id = %d;"
        curr.execute(query, (message_id,))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")


def list_messages_by_group_id(group_id: int):
    try:
        query = f"SELECT * FROM Messages WHERE group_id = %d;"
        curr.execute(query, (group_id,))
        return curr.fetchall()
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")
