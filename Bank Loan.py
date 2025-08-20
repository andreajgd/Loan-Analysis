import pandas as pd 
#used for working with structural files, cleaning and importing or processing data
import numpy as np 
#for algebraic operations 
import matplotlib.pyplot as plt
#used for creating two-dimensional graphs, for charts
import seaborn as sns
#used for statistical analysis, more advanced charts
import warnings 
#more structured warning message
import plotly.express as px
#creating interactive charts

warnings.filterwarnings("ignore")  # ignore warnings

# Cargar datos
df = pd.read_excel("D:/Prácticas- Python/Data Analysis/financial_loan.xlsx")

df.head()
df.tail()

# Metadata Of Data
print("Number of Rows: ", df.shape[0])
#shape gives the shape of the data: how many ROWS 

print("Number of Columns: ", df.shape[1])
#shape gives the shape of the data: how many COLUMNS 

df.info()
#to see what kind of data is available

# Data types
df.dtypes
#see the data types inside of the sheets

df.describe()
#to see the summary statistics of all the data

# Total Loan Applications
total_loan_application = df['id'].count()
print("Total Loan Applications: ", total_loan_application)

# MTD (Month To Date) Total Loan Applications
latest_issue_date = df['issue_date'].max()
latest_year = latest_issue_date.year
latest_month = latest_issue_date.month
mtd_data = df[(df['issue_date'].dt.year == latest_year) & (df['issue_date'].dt.month == latest_month)]
mtd_loan_applications = mtd_data['id'].count()
print(f"MTD Loan Applications (for {latest_issue_date.strftime('%B %Y')}): {mtd_loan_applications}")
#f indicates that it's an f-string.
#%B: full month name
#%Y: full year with century 

# Total Founded Amount
total_funded_amount = df['loan_amount'].sum()
total_funded_amount_millions = total_funded_amount / 1000000
print("Total Funded Amount: ${:.2f}M". format(total_funded_amount_millions))
#.2: This specifies the precision of the number, meaning it will display exactly two digits after the decimal point.
#f: This indicates that the number should be formatted as a fixed-point number (i.e., a decimal number).

# MTD - Total Founded Amount
mtd_total_funded_amount = mtd_data['loan_amount'].sum()
mtd_total_funded_amount_millions = mtd_total_funded_amount/1000000
print("MTD Total Funded Amount: ${:.2f}M". format(mtd_total_funded_amount_millions))

# Total Amount Recieved
total_amount_recived = df['total_payment'].sum()
total_amount_recieved_millions = total_funded_amount/1000000
print("Totald Amount Recived : ${:.2f}M". format(total_amount_recieved_millions))

# MTD Total Amount Recieved
mtd_total_amount_recieved = mtd_data['total_payment'].sum()
mtd_total_amount_recieved_millions = mtd_total_amount_recieved/1000000
print("MTD Total Funded Amount: ${:.2f}M". format(mtd_total_amount_recieved_millions))

# Average Interest Rate
average_interest_rate = df['int_rate'].mean()*100
print("Average Interest Rage: {:.2f}%".format(average_interest_rate))

# Average Debt-to-Income Ratio (DTI)
average_idti = df['dti'].mean()*100
print("Average Debt-to-Income Radio (DTI): {:.2f}%".format(average_idti))

# Good Loan Metrics
good_loans = df[df['loan_status'].isin(["Fully Paid", "Current"])]
#isin function is used to check if its inside 

total_loan_applications = df['id'].count()
good_loan_applications = good_loans['id'].count()
good_loan_funded_amount = good_loans['loan_amount'].sum()
good_loan_received = good_loans['total_payment'].sum()

good_loan_funded_amount_millions = good_loan_funded_amount / 1000000
good_loan_received_millions = good_loan_received / 1000000

good_loan_percentage = (good_loan_applications / total_loan_applications) * 100

print("Good Loan Applications:", good_loan_applications)
print("Good Loan Funded Amount (in Millions): ${:.2f}M".format(good_loan_funded_amount_millions))
print("Good Loan Total Received (in Millions): ${:.2f}M".format(good_loan_received_millions))
print("Percentage of Good Loan Applications: {:.2f}%".format(good_loan_percentage))

# Bad Loan Metrics
bad_loans = df[df['loan_status'].isin(["Charged Off"])]

bad_loan_applications = bad_loans['id'].count()
bad_loan_funded_amount = bad_loans['loan_amount'].sum()
bad_loan_received = bad_loans['total_payment'].sum()

bad_loan_funded_amount_millions = bad_loan_funded_amount / 1000000
bad_loan_received_millions = bad_loan_received / 1000000
bad_loan_percentage = (bad_loan_applications / total_loan_applications) * 100

print("Bad Loan Applications:", bad_loan_applications)
print("Bad Loan Funded Amount (in Millions): ${:.2f}M".format(bad_loan_funded_amount_millions))
print("Bad Loan Total Received (in Millions): ${:.2f}M".format(bad_loan_received_millions))
print("Percentage of Bad Loan Applications: {:.2f}%".format(bad_loan_percentage))

# Monthly Trends By Issue Date For Total Funded Amount
monthly_funded = (
    df.sort_values('issue_date') 
        .assign(month_name=lambda x: x['issue_date'].dt.strftime('%b %Y'))  
        .groupby('month_name', sort=False)['loan_amount'] 
        .sum() 
        .div(1000000) 
        .reset_index(name='loan_amount_millions')
)

plt.figure(figsize=(10, 5))  
plt.fill_between(monthly_funded['month_name'], monthly_funded['loan_amount_millions'], color='pink', alpha=0.5)
plt.plot(monthly_funded['month_name'], monthly_funded['loan_amount_millions'], color='skyblue', linewidth=2)

for i, row in monthly_funded.iterrows():
    plt.text(i, row['loan_amount_millions'] + 0.1, f"{row['loan_amount_millions']:.2f}",
             ha='center', va='bottom', fontsize=8, rotation=0, color='black')

plt.title('Total Funded Amount by Month', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Funded Amount (R Millions)')
plt.xticks(ticks=range(len(monthly_funded)), labels=monthly_funded['month_name'], rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Monthly Trends By Issue Date For Total Funded Amount Received
monthly_received = (
    df.sort_values('issue_date')
    .assign(month_name=lambda x: x['issue_date'].dt.strftime('%b %Y'))
    .groupby('month_name', sort=False)['total_payment']
    .sum()
    .div(1000000)
    .reset_index(name='received_amount_millions')
)

plt.figure(figsize=(10, 5))
plt.fill_between(monthly_received['month_name'], monthly_received['received_amount_millions'], color='lightblue', alpha=0.5)
plt.plot(monthly_received['month_name'], monthly_received['received_amount_millions'],
         color='lightgreen', linewidth=2)

for i, row in monthly_received.iterrows():
    plt.text(i, row['received_amount_millions'] + 0.1, f'{row["received_amount_millions"]:.2f}',
             ha='center', va='bottom', fontsize=9, rotation=0, color='black')

plt.title('Total Received Amount by Month', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Received Amount (R Millions)')
plt.xticks(ticks=range(len(monthly_received)), labels=monthly_received['month_name'], rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Monthly Trends By Issue Date For Total Loan Applications
monthly_applications = (
    df.sort_values('issue_date')
    .assign(month_name=lambda x: x['issue_date'].dt.strftime('%b %Y'))
    .groupby('month_name', sort=False)['total_payment']
    .count()
    .reset_index(name='received_amount_millions_count')
)

plt.figure(figsize=(10, 5))
plt.fill_between(monthly_received['month_name'], monthly_received['received_amount_millions_count'], color='orange', alpha=0.5)
plt.plot(monthly_received['month_name'], monthly_received['received_amount_millions_count'],
         color='yellow', linewidth=2)

for i, row in monthly_received.iterrows():
    plt.text(i, row['received_amount_millions_count'] + 0.1, f'{row["received_amount_millions_count"]}',
             ha='center', va='bottom', fontsize=9, rotation=0, color='black')

plt.title('Monthly Trends By Issue Date For Total Loan Applications', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Received Amount (R Millions)')
plt.xticks(ticks=range(len(monthly_received)), labels=monthly_received['month_name'], rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Regional Analysis By State For Total Funded Amount
state_funding = df.groupby('address_state')['loan_amount'].sum().sort_values(ascending=True)
state_funding_thousands = state_funding / 1000

plt.figure(figsize=(10, 8))
bars = plt.barh(state_funding_thousands.index, state_funding_thousands.values, color='lightcoral')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 10, bar.get_y() + bar.get_height()/2,
             f'{width:.0f}K', va='center', fontsize=9)

plt.title('Total Funded Amount by State (in Thousands)')
plt.xlabel('Funded Amount (₹ \'000)')
plt.ylabel('State')
plt.tight_layout()
plt.show()

# Loan Term Analysis By Total Funded Amount
term_funding_millions = df.groupby('term')['loan_amount'].sum() / 1000000

plt.figure(figsize=(5, 5))
plt.pie(
    term_funding_millions,
    labels=term_funding_millions.index,
    autopct=lambda p: f"{p:.1f}%\n${p*sum(term_funding_millions)/100:.1f}M",
    startangle=90,
    wedgeprops={'width': 0.4}
)
plt.gca().add_artist(plt.Circle((0, 0), 0.70, color='white'))
plt.title("Total Funded Amount by Term (in $ Millions)")
plt.show()

# Employee Length By Total Funded Amount
emp_funding = df.groupby('emp_length')['loan_amount'].sum().sort_values()/1000

plt.figure(figsize=(10, 6))
bars = plt.barh(emp_funding.index, emp_funding, color='skyblue')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 5, bar.get_y() + bar.get_height() / 2,
             f"{width:,.0f}K",
             va='center',
             fontsize=9)

plt.xlabel("Funded Amount (₹ Thousands)")
plt.title("Total Funded Amount by Employment Length")
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# Loan Purpose Breakdown By Total Funded Amount
purpose_funding_millions = (df.groupby('purpose')['loan_amount'].sum().sort_values() / 1000000)

plt.figure(figsize=(10, 6))
bars = plt.barh(purpose_funding_millions.index, purpose_funding_millions.values, color='skyblue')

for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.1, bar.get_y() + bar.get_height()/2,
             f'{width:.2f}M',
             va='center',
             fontsize=9)

plt.title('Total Funded Amount by Loan Purpose (₹ Millions)', fontsize=14)
plt.xlabel('Funded Amount (₹ Millions)')
plt.ylabel('Loan Purpose')
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Home Ownership By Total Funded Amount
home_funding = df.groupby('home_ownership')['loan_amount'].sum().reset_index()
home_funding['loan_amount_millions'] = home_funding['loan_amount'] / 1000000

fig = px.treemap(
    home_funding,
    path=['home_ownership'],
    values='loan_amount_millions',
    color='loan_amount_millions',
    color_continuous_scale='Blues',
    title='Total Funded Amount by Home Ownership (₹ Millions)'
)
fig.show()
