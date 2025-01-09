import streamlit as st
import pandas as pd
import json
import requests
import time

# Load protocol analysis results from JSON
def load_analysis():
    try:
        with open("defi_analysis_results.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Analysis file not found. Run the protocol analysis script first.")
        return {}

# Fetch real-time prices (Mock Data)
def fetch_prices():
    return {
        "THORChain": {"ETH": 1800.50},
        "Synapse": {"ETH": 1795.30},
        "Rubic": {"ETH": 1797.20}
    }

# Detect arbitrage opportunities
def find_arbitrage(prices):
    arbitrage_opportunities = []
    protocols = list(prices.keys())
    for i in range(len(protocols)):
        for j in range(i + 1, len(protocols)):
            p1, p2 = protocols[i], protocols[j]
            price1, price2 = prices[p1]["ETH"], prices[p2]["ETH"]
            diff = abs(price1 - price2) / ((price1 + price2) / 2) * 100
            if diff > 2.0:  # Example: Arbitrage threshold set to 2%
                arbitrage_opportunities.append({
                    "Protocol1": p1,
                    "Protocol2": p2,
                    "Price1": price1,
                    "Price2": price2,
                    "Difference (%)": diff
                })
    return arbitrage_opportunities

# Streamlit Dashboard
st.title("DeFi Protocol Dashboard")
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a View", ["Protocol Analysis", "Arbitrage Monitoring"])

if options == "Protocol Analysis":
    st.header("Protocol Analysis")
    analysis = load_analysis()

    if analysis:
        for protocol, data in analysis.items():
            st.subheader(protocol)
            st.write("**Key Metrics:**")
            st.json(data.get("key_metrics", {}))
            st.write("**Unique Features:**")
            st.write(data.get("unique_features", []))
            st.write("**Risks:**")
            st.write(data.get("risks", []))
            st.write("**Arbitrage Opportunities:**")
            st.write(data.get("arbitrage_opportunities", []))

elif options == "Arbitrage Monitoring":
    st.header("Real-Time Arbitrage Monitoring")

    st.write("Fetching real-time prices...")
    prices = fetch_prices()
    st.write("Prices:", prices)

    st.write("Calculating arbitrage opportunities...")
    opportunities = find_arbitrage(prices)

    if opportunities:
        st.write("### Arbitrage Opportunities")
        st.table(pd.DataFrame(opportunities))
    else:
        st.write("No arbitrage opportunities detected.")

