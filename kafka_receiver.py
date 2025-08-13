import json
import csv
import os
from kafka import KafkaConsumer

# Kafka configuration
topic = 'zeek_logs'
bootstrap_servers = ['192.168.1.29:9092']
group_id = 'zeek_csv_saver'

# Output CSV file
output_file = 'conn_hoic.csv'

# Fields you want to include in the CSV
required_fields = [
    'ts', 'uid', 'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p',
    'proto', 'service', 'duration', 'orig_bytes', 'resp_bytes', 
    'conn_state', 'local_orig', 'local_resp', 'missed_bytes', 
    'history', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'tunnel_parents'
]

# Initialize Kafka consumer
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id=group_id,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# State for CSV writing
fieldnames = required_fields
rows = []

print("[*] Listening for messages...")

try:
    for message in consumer:
        data = message.value
        
        # Filter the data to only include required fields
        filtered_data = {key: data[key] for key in required_fields if key in data}

        rows.append(filtered_data)
        print(f"[+] Collected {len(rows)} messages...")

except KeyboardInterrupt:
    print("\n[!] Stopped by user. Writing to CSV...")

    # Write to CSV with specified headers
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print("[*] CSV file saved:", output_file)

finally:
    consumer.close()
