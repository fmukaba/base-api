import psycopg2

# todo: put into config file
db_params = {
    "host": "",
    "database": "",
    "user": "",
    "password": "",
    "port": ""
}

create_messages_table_command = """
        CREATE TABLE Messages (
            id BIGSERIAL PRIMARY KEY,
            group_id INTEGER NOT NULL,
            sender_id INTEGER NOT NULL,
            message VARCHAR(300) NOT NULL
        )
        """

commands = [
    create_messages_table_command
]

try:
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as curr:
            for command in commands:
                curr.execute(command)
except (psycopg2.DatabaseError, Exception) as error:
    print(error)
