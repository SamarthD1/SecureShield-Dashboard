import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)

NUM_CLIENTS = 500

def generate_transactions():
    data = []
    for i in range(1000):
        tps = np.random.normal(6500, 500)
        success = 1 if random.random() < 0.985 else 0
        false_positive = 1 if random.random() < 0.02 else 0 # 2% False Positive Rate
        data.append({
            'transaction_id': f"TXN-{1000+i}",
            'tps': round(tps, 2),
            'encryption_success': success,
            'false_positive': false_positive,
            'tamper_detected': 1 if random.random() < 0.005 else 0,
            'timestamp': datetime.now() - timedelta(minutes=random.randint(0, 10000))
        })
    return pd.DataFrame(data)

def generate_system_monitoring():
    data = []
    base_date = datetime.now() - timedelta(days=365)
    for i in range(365):
        uptime = np.random.normal(99.94, 0.03)
        attacks = np.random.poisson(25)
        # MTTD: Mean Time to Detect (Seconds)
        mttd = np.random.normal(45, 10) 
        # MTTR: Mean Time to Respond (Minutes) - Industry standard name
        mttr = np.random.normal(3.2, 0.4)
        
        data.append({
            'date': base_date + timedelta(days=i),
            'uptime_pct': round(min(100, uptime), 3),
            'attacks_prevented_count': attacks,
            'firewall_block_events': attacks + random.randint(5, 15),
            'phishing_attempts_flagged': random.randint(2, 8),
            'mttd_sec': round(mttd, 2),
            'mttr_min': round(mttr, 2),
            'threat_detection_rate_pct': round(random.uniform(99.1, 99.9), 2)
        })
    return pd.DataFrame(data)

def generate_crm_data():
    # Expanded Industry list for more colors and diversity
    industries = ['FinTech', 'Healthcare', 'E-commerce', 'Manufacturing', 'Retail', 'Logistics', 'Education', 'Real Estate']
    data = []
    for i in range(NUM_CLIENTS):
        sat = np.random.normal(8.8, 0.5)
        sat = max(1, min(10, sat))
        renewal_prob = min(0.99, sat / 10 + random.uniform(-0.02, 0.02))
        
        # Vulnerability Scan Score (Higher is safer/better)
        vuln_score = random.randint(85, 100)
        
        data.append({
            'client_id': f"SME-{5000+i}",
            'industry': random.choice(industries),
            'satisfaction_score': round(sat, 1),
            'vulnerability_scan_score': vuln_score,
            'subscription_months': random.randint(6, 24),
            'renewal_probability': round(renewal_prob, 2),
            'clv_lakhs': 4.32,
            'churn_risk': 'LOW' if sat > 8 else ('MEDIUM' if sat > 6 else 'HIGH')
        })
    return pd.DataFrame(data)

if __name__ == "__main__":
    df1 = generate_transactions()
    df2 = generate_system_monitoring()
    df3 = generate_crm_data()
    
    df1.to_csv('secureshield_transactions.csv', index=False)
    df2.to_csv('secureshield_monitoring.csv', index=False)
    df3.to_csv('secureshield_crm.csv', index=False)
    print("Updated Dashboard Datasets with 8 industries generated successfully.")
