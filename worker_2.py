import os

from kafka import KafkaConsumer

from connection import get_connection

# Kafka Configuration
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'kafka_message'
kafka_group_id = 'csv_data_group'

# Raw Files Directory Configuration
raw_files_directory = 'raw_files'

# Create the directory for raw files if it doesn't exist
if not os.path.exists(raw_files_directory):
    os.makedirs(raw_files_directory)

# Create a Kafka consumer
consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=kafka_bootstrap_servers,
    group_id=kafka_group_id
)

# Read messages from Kafka
for message in consumer:
    # Get the message value as a string
    message_value = message.value.decode('utf-8')

    # Save the message as a raw file
    raw_file_path = os.path.join(raw_files_directory, f'message_{message.offset}.txt')
    with open(raw_file_path, 'w') as raw_file:
        raw_file.write(message_value)
    conn = None
    # Save the message in PostgreSQL database
    try:
        # Execute the insert statement
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO table_name (message) VALUES (%s)"
        values = (message_value,)
        cursor.execute(query, values)
        conn.commit()
        print("Message saved to PostgreSQL database successfully!")
        cursor.close()
    except Exception as e:
        conn.rollback()
        print("Error while saving the message to PostgreSQL database: ".format(e))
    finally:
        if conn is not None:
            conn.close()
            consumer.close()
