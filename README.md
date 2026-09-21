# 💰 Finora AI

### Intelligent Personal Finance & Bank Statement Analytics Platform

Finora AI is a web-based personal finance analytics application that helps users understand their financial transactions through automated statement processing, transaction categorization, spending analytics, anomaly detection, recurring payment analysis, forecasting, and financial health insights.

The application is built using Python and Streamlit and is deployed on Streamlit Community Cloud with a cloud-based MySQL-compatible database.

---

## 🚀 Live Demo

🌐 **Live Application:**  
[Open Finora AI] https://finora-ai.streamlit.app/ 

---

## 📌 GitHub Repository

💻 **Source Code:**  
https://github.com/akshat142005/Finora-AI

---

## 🎯 Problem Statement

Bank statements contain a large amount of raw transaction data, but manually analyzing this information can be time-consuming.

Users often need to manually determine:

- Where their money is being spent
- How much they are saving
- Which categories consume most of their income
- Which transactions appear unusual
- Which payments are recurring
- How their future expenses may look

Finora AI aims to simplify this process by converting raw bank statement data into meaningful financial insights.

---

## 💡 Solution

Finora AI provides an end-to-end workflow:

```text
User
 ↓
Login / Registration
 ↓
Bank Account Management
 ↓
Upload Bank Statement
 ↓
Data Extraction
 ↓
Data Cleaning & Normalization
 ↓
Transaction Categorization
 ↓
Database Storage
 ↓
Financial Analytics
 ↓
AI/ML-Based Insights
 ↓
Interactive Dashboard



✨ Key Features
🔐 User Authentication
User registration
User login
Password-based authentication
User-specific financial data
🏦 Multiple Bank Accounts

Users can manage multiple bank accounts.

Examples:

HDFC Bank
State Bank of India
ICICI Bank
Axis Bank
Other accounts

Only the last four digits of the account number are stored.

📄 Bank Statement Processing

Supports:

CSV
XLSX
PDF

The uploaded statement is extracted and converted into structured transaction data.

🧹 Transaction Cleaning

The application processes raw transaction data by:

Standardizing transaction information
Processing dates
Handling debit and credit values
Identifying transaction types
Cleaning transaction descriptions
Preparing data for analysis
🤖 Transaction Categorization

Transactions can be organized into meaningful categories such as:

Food
Shopping
Transport
Bills
Entertainment
Income
Other
📊 Financial Analytics

The dashboard provides information such as:

Total income
Total expenses
Net savings
Savings rate
Transaction count
Category-wise spending
Monthly spending patterns
🔍 Anomaly Detection

The application identifies potentially unusual transactions based on transaction and spending patterns.

This helps users identify transactions that may require further attention.

An anomaly does not automatically mean that a transaction is fraudulent.

🔄 Recurring Payment Analysis

The application can help identify repeated financial payments such as:

Subscriptions
Bills
Memberships
Other recurring expenses
📈 Expense Forecasting

Historical transaction information can be used to analyze spending patterns and estimate future expenses.

❤️ Financial Health

Finora AI combines financial indicators such as income, expenses, savings, and spending behavior to provide a financial health insight.

🛡️ Duplicate Transaction Detection

To prevent duplicate transactions when the same statement is uploaded multiple times, Finora AI generates a SHA-256 transaction hash.

The system checks the hash before inserting a transaction into the database.

Transaction
     ↓
SHA-256 Hash
     ↓
Check Database
   ↙       ↘
Exists     New
  ↓          ↓
Skip       Save
🛠️ Tech Stack
Programming Language
Python
Frontend / Application
Streamlit
Data Science
Pandas
NumPy
Scikit-learn
Visualization
Plotly
File Processing
PDF processing
CSV processing
Excel processing
pdfplumber
PyMuPDF
openpyxl
Database
MySQL-compatible database
TiDB Cloud
Authentication
bcrypt
Reporting
ReportLab
Deployment
Streamlit Community Cloud
TiDB Cloud
Version Control
Git
GitHub
🗄️ Database Architecture

Finora AI uses a relational database with three main entities:

┌──────────────┐
│    Users     │
└──────┬───────┘
       │
       │ user_id
       ↓
┌──────────────────┐
│  Bank Accounts   │
└────────┬─────────┘
         │
         │ account_id
         ↓
┌──────────────────┐
│   Transactions   │
└──────────────────┘
Users Table

Stores user authentication information.

Main fields:

id
name
email
password
created_at
Bank Accounts Table

Stores bank account information.

Main fields:

id
user_id
bank_name
account_name
account_number_last4
account_type
created_at
Transactions Table

Stores financial transaction information.

Main fields:

id
user_id
account_id
transaction_date
merchant
description
transaction_type
amount
category
balance
transaction_hash
created_at

Foreign keys are used to maintain relationships between users, bank accounts, and transactions.

THANK YOU 
