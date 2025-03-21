import pika
import os
import sys
import time

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    print(f" [x] Done")


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs',exchange_type='direct')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    severities = sys.argv[1:]
    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]" % sys.argv[0])
        sys.exit(1)

    for severity in severities:
        channel.queue_bind(exchange='direct_logs',
                           queue=queue_name,
                           routing_key=severity) 

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
