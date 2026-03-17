import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import io

# Page Configuration
st.set_page_config(
    page_title="SecureShield Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    [data-testid="stSidebar"] { background-color: #111421; }
    h1, h2, h3 { color: #ffffff !important; }
    .stMarkdown { color: #d1d5db; }
    </style>
    """, unsafe_allow_html=True)

import os

# Load Data Functions with Auto-Generation for Deployment
@st.cache_data
def load_data():
    csv_files = ['secureshield_transactions.csv', 'secureshield_monitoring.csv', 'secureshield_crm.csv']
    
    # Check if files exist; if not, generate them (useful for Streamlit Cloud)
    if not all(os.path.exists(f) for f in csv_files):
        try:
            import generate_data
            df1 = generate_data.generate_transactions()
            df2 = generate_data.generate_system_monitoring()
            df3 = generate_data.generate_crm_data()
            df1.to_csv('secureshield_transactions.csv', index=False)
            df2.to_csv('secureshield_monitoring.csv', index=False)
            df3.to_csv('secureshield_crm.csv', index=False)
        except Exception as e:
            st.error(f"Error generating data: {e}")
            return None, None, None

    try:
        df_tx = pd.read_csv('secureshield_transactions.csv')
        df_system = pd.read_csv('secureshield_monitoring.csv')
        df_crm = pd.read_csv('secureshield_crm.csv')
        return df_tx, df_system, df_crm
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

df_tx, df_system, df_crm = load_data()

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/parakeet/512/security-shield.png", width=100)
    st.title("SecureShield AI")
    st.markdown("---")
    menu = st.radio(
        "Navigation",
        ["Dashboard Overview", "Financial Analysis", "Technical & Encryption", "System Monitoring", "CRM Insights", "Risk Center"]
    )
    st.markdown("---")
    st.info("Case Study 91: SME Cybersecurity Service")

if df_tx is not None:
    # --- DASHBOARD OVERVIEW ---
    if menu == "Dashboard Overview":
        st.title("🛡️ Executive Overview")
        st.markdown("Real-time operational and financial health of the SME Cybersecurity Service.")

        m1, m2, m3, m4 = st.columns(4)
        
        # Calculations
        tot_rev = 500 * 1.2
        avg_uptime = df_system['uptime_pct'].mean()
        avg_detection = df_system['threat_detection_rate_pct'].mean()
        avg_sat = df_crm['satisfaction_score'].mean()
        
        m1.metric("Target Clients", "500", "SMEs")
        m2.metric("Annual Revenue", f"₹{tot_rev}L", "₹6 Crores")
        m3.metric("System Uptime", f"{avg_uptime:.2f}%", f"Target 99.9%")
        m4.metric("Detection Rate", f"{avg_detection:.2f}%", "Healthy")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Industry Distribution")
            fig_ind = px.pie(df_crm, names='industry', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu, template="plotly_dark")
            st.plotly_chart(fig_ind, use_container_width=True)
        with col2:
            st.subheader("Churn Risk Profile (Based on CSAT)")
            fig_risk = px.bar(df_crm['churn_risk'].value_counts().reset_index(), x='churn_risk', y='count', color='churn_risk', 
                             color_discrete_map={'LOW':'#00cc96', 'MEDIUM':'#ffa15a', 'HIGH':'#ef553b'},
                             template="plotly_dark")
            st.plotly_chart(fig_risk, use_container_width=True)

    # --- FINANCIAL ANALYSIS ---
    elif menu == "Financial Analysis":
        st.title("💰 Business & Financials")
        st.sidebar.markdown("### Financial Parameters")
        growth_rate = st.sidebar.slider("Annual Client Growth (%)", 0, 50, 15)
        churn_rate = st.sidebar.slider("Annual Churn Rate (%)", 0, 30, 5)
        
        c1, c2 = st.columns([1, 1.5])
        with c1:
            st.markdown(f"### Dynamic Growth Model\n- **Unit Fee:** ₹1.2 Lakhs / year\n- **Net Growth:** {growth_rate - churn_rate}%")
            st.metric("Y1 Gross Revenue", "₹600L")
            # Business Logic for Question 2
            st.metric("Y1 Net Benefit", "₹50L", "-₹400L CAPEX")
            
        with c2:
            fig_fin = go.Figure(go.Waterfall(
                measure = ["relative", "relative", "relative", "total"],
                x = ["Gross Revenue", "Operational Cost", "Initial Investment", "Net Benefit"],
                y = [600, -150, -400, 0],
                increasing = {"marker":{"color":"#00cc96"}},
                decreasing = {"marker":{"color":"#ef553b"}},
                totals = {"marker":{"color":"#ab63fa"}},
                template="plotly_dark"
            ))
            fig_fin.update_layout(title="Year 1 Cash Flow Breakdown (₹ Lakhs)")
            st.plotly_chart(fig_fin, use_container_width=True)

        st.markdown("---")
        # 5 Year Projection
        years = [f"Year {i}" for i in range(1, 6)]
        client_list, rev_list, profit_list, cum_profit = [], [], [], []
        current_clients, current_cum = 500, 0
        for i in range(5):
            rev = current_clients * 1.2
            opex = 150 + (max(0, current_clients - 500) * 0.1) 
            capex = 400 if i == 0 else 0
            p = rev - opex - capex
            client_list.append(int(current_clients))
            rev_list.append(rev)
            current_cum += p
            profit_list.append(p)
            cum_profit.append(current_cum)
            current_clients *= (1 + (growth_rate - churn_rate) / 100)
            
        df_5yr = pd.DataFrame({"Financial Year": years, "Clients": client_list, "Revenue (₹L)": rev_list, "Annual Profit (₹L)": profit_list, "Cumulative Profit (₹L)": cum_profit})
        st.subheader(f"📅 5-Year Scaling Projection (Revenue at ₹{rev_list[-1]:.0f}L by Year 5)")
        st.dataframe(df_5yr.style.format(precision=1), use_container_width=True)
        
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_5yr.to_excel(writer, index=False)
        st.download_button("📥 Download 5-Year Analytics (Excel)", buffer.getvalue(), "SecureShield_Projections.xlsx")

    # --- TECHNICAL & ENCRYPTION ---
    elif menu == "Technical & Encryption":
        st.title("⚡ Technical Performance Metrics")
        col1, col2 = st.columns(2)
        with col1:
            succ_rate = (df_tx['encryption_success'].sum() / len(df_tx)) * 100
            st.plotly_chart(go.Figure(go.Indicator(
                mode="gauge+number", value=succ_rate, 
                title={'text': "Encryption Success Rate (%)"}, 
                gauge={'axis': {'range': [90, 100]}, 'bar': {'color': "#00cc96"}}
            )).update_layout(template="plotly_dark"), use_container_width=True)
        with col2:
            fp_rate = (df_tx['false_positive'].sum() / len(df_tx)) * 100
            st.metric("False Positive Rate (%)", f"{fp_rate:.2f}%", "-0.05% Improvement")
            st.plotly_chart(px.histogram(df_tx, x='tps', nbins=30, title="System Throughout (TPS Distribution)", color_discrete_sequence=['#ab63fa'], template="plotly_dark"), use_container_width=True)

    # --- SYSTEM MONITORING ---
    elif menu == "System Monitoring":
        st.title("🖥️ Infrastructure & Threat Monitoring")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Attacks Prevented", f"{df_system['attacks_prevented_count'].sum():,}")
        m2.metric("MTTD (Avg)", f"{df_system['mttd_sec'].mean():.1f} Sec")
        m3.metric("MTTR (Avg)", f"{df_system['mttr_min'].mean():.1f} Min")

        st.plotly_chart(px.line(df_system, x='date', y='uptime_pct', title="System Uptime (%) - 365 Day Performance", color_discrete_sequence=['#00cc96'], template="plotly_dark"), use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            st.subheader("Threat Activity vs Protection")
            fig_attacks = go.Figure()
            fig_attacks.add_trace(go.Scatter(x=df_system['date'], y=df_system['attacks_prevented_count'], name="Attacks Prevented", line=dict(color='#ab63fa')))
            fig_attacks.add_trace(go.Scatter(x=df_system['date'], y=df_system['firewall_block_events'], name="Firewall Block Events", line=dict(color='#ef553b', dash='dash')))
            fig_attacks.update_layout(template="plotly_dark", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_attacks, use_container_width=True)
        with c2: 
            st.subheader("Phishing Attacks Flagged")
            st.plotly_chart(px.area(df_system, x='date', y='phishing_attempts_flagged', color_discrete_sequence=['#ffa15a'], template="plotly_dark"), use_container_width=True)

    # --- CRM INSIGHTS ---
    elif menu == "CRM Insights":
        st.title("🤝 CRM & Satisfaction Metrics")
        
        avg_sat_ind = df_crm.groupby('industry')['satisfaction_score'].mean().reset_index()
        st.subheader("Industry Satisfaction Heatmap (CSAT)")
        st.plotly_chart(px.imshow([avg_sat_ind['satisfaction_score'].values], x=avg_sat_ind['industry'].values, color_continuous_scale="RdYlGn", template="plotly_dark"), use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1: 
            st.subheader("Financial Health: Renewal Probability")
            st.plotly_chart(px.histogram(df_crm, x='renewal_probability', nbins=20, title="Distribution of Client Renewal Probability", color_discrete_sequence=['#00cc96'], template="plotly_dark"), use_container_width=True)
        with c2: 
            st.subheader("Vulnerability Scan Score Distribution")
            avg_vuln = df_crm.groupby('industry')['vulnerability_scan_score'].mean().reset_index()
            st.plotly_chart(px.bar(avg_vuln, x='industry', y='vulnerability_scan_score', color='industry', title="Average Vulnerability Scan Score by Industry", template="plotly_dark"), use_container_width=True)

    # --- RISK CENTER ---
    elif menu == "Risk Center":
        st.title("🚨 Risk Stress Testing")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🔴 Breach Scenario Simulation")
            breach = st.selectbox("Select Scenario", ["Normal Operations (Secure)", "Minor Sensitive Data Leak", "Major Infrastructure Breach"])
            impact = "₹0L" if breach=="Normal Operations (Secure)" else ("₹20L" if breach=="Minor Sensitive Data Leak" else "₹100L")
            st.metric("Estimated Penalty Cost", impact)
            if breach != "Normal Operations (Secure)":
                st.error(f"High Churn Risk: { '10%' if 'Minor' in breach else '40%' } projected client loss.")
        with c2:
            st.subheader("⏱️ SLA & Downtime Risk")
            downtime = st.slider("System Downtime (Hours)", 0, 48, 0)
            st.metric("SLA Payout Liability", f"₹{downtime * 5}L")
            if downtime > 10:
                st.warning("Critical: Payout exceeds quarterly OpEx reserve.")
        
        st.plotly_chart(go.Figure(go.Indicator(
            mode="gauge+number", value=78, 
            title={'text': "Infrastructure Load at Current Scale (%)"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#ab63fa"}, 'steps': [{'range': [0, 80], 'color': "rgba(0, 204, 150, 0.2)"}, {'range': [80, 100], 'color': "rgba(239, 85, 59, 0.2)"}]}
        )).update_layout(template="plotly_dark"), use_container_width=True)
