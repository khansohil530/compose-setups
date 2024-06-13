import pika

# connection to rabbitmq broker on host machine
connection  = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello') # create hello queue

# message goes through exchange. Here we used default exchange '' which lets
# us specify queue name in `routing_key` to send the message
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print("[x] Sent 'Hello World!'")
connection.close() # close connection before exiting program to flush network buffers

