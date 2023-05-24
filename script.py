import os

from kafka import KafkaProducer

from connection import get_connection

# Delete all from database
conn = None
try:
    conn = get_connection()
    cursor = conn.cursor()
    table_name = 'table_name'
    query = f"DELETE FROM {table_name}"
    cursor.execute(query)
    conn.commit()
    cursor.close()
except Exception as e:
    print('The error is : '.format(e))
finally:
    if conn is not None:
        conn.close()
# Kafka Configuration
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'kafka_message'

# Raw Files Directory Configuration
raw_files_directory = 'raw_files'

# Configure Kafka producer
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

# Republish messages from raw files to Kafka
for file_name in os.listdir(raw_files_directory):
    if file_name.endswith('.txt'):
        file_path = os.path.join(raw_files_directory, file_name)
        with open(file_path, 'r') as raw_file:
            message_value = raw_file.read()
            producer.send(kafka_topic, message_value.encode('utf-8'))

# Close the Kafka producer
producer.close()
