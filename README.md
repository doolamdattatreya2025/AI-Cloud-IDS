# 🚀 Cloud-Native AI Intrusion Detection System (IDS)

## 💡 Why I Built This

Traditional Intrusion Detection Systems (IDS) rely heavily on signature-based detection, which limits their ability to identify new or evolving threats. In a cloud environment where traffic patterns change rapidly, this approach is often not enough.

This project focuses on building an **AI-driven IDS** that learns normal network behavior and identifies deviations. Instead of searching for known attack patterns, it detects **unusual activity that may indicate potential security threats**, including previously unseen ones.

---

## 🧠 Core Idea

The system uses an **Isolation Forest algorithm**, an unsupervised machine learning technique designed to detect anomalies in data without requiring labeled datasets.

* Normal traffic behaves consistently
* Anomalies are rare and significantly different
* The model isolates these anomalies and flags them for review

---

## ⚙️ How It Works

### Pipeline Overview:

1. **Data Collection**
   AWS VPC Flow Logs capture network traffic data

2. **Storage**
   Logs are stored as compressed `.gz` files in an Amazon S3 bucket

3. **Data Processing**
   A Python script fetches the most recent log file using `boto3` and processes it in memory using `gzip` and `io.BytesIO`

4. **Feature Engineering**
   The following features are extracted:

   * Packets
   * Bytes
   * Source Port
   * Destination Port

5. **Anomaly Detection**
   The Isolation Forest model is trained on the current dataset and assigns anomaly scores

6. **Alerting**
   If anomalies are detected, an alert is sent via AWS SNS with key traffic details

---

## 🏗️ Architecture & Stack

* **Cloud Services:** AWS (S3, EC2, SNS, VPC Flow Logs)
* **Programming Language:** Python
* **Libraries:**

  * pandas
  * scikit-learn
  * boto3
* **Machine Learning:** Isolation Forest (Unsupervised Learning)

---

## 🚧 Challenges & Learnings

* **Handling Compressed Logs**
  AWS stores logs in compressed `.gz` format. I implemented in-memory decompression using `io.BytesIO` to avoid disk overhead and improve performance

* **Selecting Relevant Features**
  Choosing meaningful network features (packets, bytes, ports) was critical for effective anomaly detection

* **Reducing False Positives**
  Initial runs flagged too many normal events as anomalies. Tuning the `contamination` parameter helped balance sensitivity and accuracy

---

## 📸 Sample Alert Output

![AI Security Alert](images/ai-security-alert.png)

*This alert was triggered after detecting unusual traffic patterns in AWS VPC Flow Logs.*

---

## 📂 Project Structure

```
AI-Cloud-IDS/
│
├── ids_ai_logic.py        # Main detection script
├── README.md              # Documentation
├── requirements.txt       # Dependencies
├── .gitignore
└── images/
    └── ai-security-alert.png
```

---

## ▶️ Getting Started

### 1. Clone the Repository

```
git clone https://github.com/doolamdattatreya2025/AI-Cloud-IDS.git
cd AI-Cloud-IDS
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Configure Environment

Update the following variables in the script:

* S3 Bucket Name
* SNS Topic ARN
* AWS Region

*(Tip: Use environment variables for better security.)*

### 4. Run the Script

```
python ids_ai_logic.py
```

---

## 📈 Results

* Successfully detected simulated intrusion attempts (e.g., unauthorized SSH access)
* Generated real-time alerts within seconds
* Identified unusual traffic patterns without relying on predefined rules

---

## 🔮 Future Improvements

* Persist trained models instead of retraining each run
* Automate execution using cron jobs or AWS Lambda
* Add visualization dashboards for traffic insights
* Integrate with SIEM tools for advanced monitoring

---

## 👨‍💻 Author

**Ram**
Cybersecurity & Forensics Student
Interested in Cloud Security, Threat Detection, and AI in Security

---

## ⭐ If you found this project interesting, feel free to star the repository!
