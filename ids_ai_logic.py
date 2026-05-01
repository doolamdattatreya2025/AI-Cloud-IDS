import pandas as pd
from sklearn.ensemble import IsolationForest
import boto3
import io
import gzip

# CONFIGURATION
BUCKET_NAME = 'your-bucket-name'
SNS_TOPIC_ARN = 'your-sns-topic-arn'
REGION = 'eu-north-1'

s3 = boto3.client('s3', region_name=REGION)
sns = boto3.client('sns', region_name=REGION)

def send_alert(message):
    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="!!! AI SECURITY ALERT !!!",
            Message=message
        )
        print("Alert notification sent successfully!")
    except Exception as e:
        print(f"Failed to send alert: {e}")

def train_and_detect():
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='AWSLogs/')
    latest_file = sorted(response['Contents'], key=lambda x: x['LastModified'])[-1]['Key']
    
    print(f"AI Brain analyzing: {latest_file}")
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=latest_file)
    
    with gzip.GzipFile(fileobj=io.BytesIO(obj['Body'].read())) as gf:
        df = pd.read_csv(gf, sep=' ', skiprows=1, names=[
            'version', 'account-id', 'interface-id', 'srcaddr', 'dstaddr', 
            'srcport', 'dstport', 'protocol', 'packets', 'bytes', 
            'start', 'end', 'action', 'log-status'
        ])

    features = df[['packets', 'bytes', 'srcport', 'dstport']]
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(features)
    
    df['anomaly_score'] = model.predict(features)
    anomalies = df[df['anomaly_score'] == -1]

    if not anomalies.empty:
        alert_msg = f"AI detected {len(anomalies)} anomalies in the cloud traffic.\n\n"
        alert_msg += anomalies[['srcaddr', 'dstport', 'action']].head(5).to_string(index=False)
        
        print(f"!!! AI ALERT: {len(anomalies)} anomalies detected!")
        send_alert(alert_msg)
    else:
        print("AI confirms: Traffic patterns look normal.")

if __name__ == "__main__":
    train_and_detect()