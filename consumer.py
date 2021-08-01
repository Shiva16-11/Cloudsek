import pika
import sqlite3
import ast
import time
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))


def update(connector, table):
    sql = ''' UPDATE Answer_numberdata
     SET total = ?
     WHERE id = ?'''
    cur = connector.cursor()
    cur.execute(sql, table)
    connector.commit()


def consume():
    channel = connection.channel()
    channel.queue_declare(queue='q')

    def callback(ch, method, properties, body):
        time.sleep(10)
        body = body.decode('utf-8')
        body = ast.literal_eval(body)
        pk, num1, num2 = body[0], body[1], body[2]
        total = num1 + num2
        try:
            conn = sqlite3.connect('db.sqlite3')
            with conn:
                update(conn, (total, pk))

        except Exception as e:
            print(e)

    channel.basic_consume(queue='q', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


consume()
