import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
sender_email =os.getenv("SMTP_EMAIL")      
sender_password = os.getenv("SMTP_PASSWORD") 

def send_email(to_email, subject, body):
    if not sender_email or not sender_password:
        return "Mock Sent (No SMTP Credentials)"
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  
        server.login(sender_email, sender_password)
        
        server.send_message(msg)
        server.quit()
        print(f"[LIVE SENT] sucessfully sent -> {to_email}")
        return "Success"
    except Exception as e:
        return f"Failed: {str(e)}"

file_path = "techlead1.ods"  

excel_file = pd.ExcelFile(file_path, engine='odf')
all_sheets = excel_file.sheet_names

sheet_name = all_sheets[-1]

df = pd.read_excel(file_path, sheet_name=sheet_name, engine='odf')

df['Last Order Date'] = pd.to_datetime(df['Last Order Date'], format='%d/%m/%y', errors='coerce')

today = pd.to_datetime('2026-06-30')
sixty_days_ago = today - datetime.timedelta(days=60)

filtered_df = df[
    (df['Total Order Value'] > 100000) & 
    (df['Last Order Date'] <= sixty_days_ago)
]

testing_df = filtered_df

if api_key and not api_key.startswith("your_actual"):
    client = OpenAI(api_key=api_key)
    testing_mode = False
else:
    client = None
    testing_mode = True

log_data = []

for index, row in testing_df.iterrows():
    customer_name = row['Customer Name']
    customer_email = row['Email']
    last_items = row['Last 3 Items Ordered']
    
    prompt = (
        f"Write a warm win-back email to our B2B client '{customer_name}'. "
        f"Mention that they haven't ordered in 60+ days and we miss them. "
        f"Highlight their last ordered items: {last_items}."
    )
    
    if not testing_mode:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an automated client success manager."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            email_content = response.choices[0].message.content
            email_snippet = email_content[:120].replace('\n', ' ') + "..."
        except Exception as e:
            email_content = f"Mock Email for {customer_name} regarding {last_items}."
            email_snippet = "[API Error Fallback] Email content..."
    else:
        email_content = (
            f"Dear {customer_name},\n\nWe notice you haven't ordered in 60 days. "
            f"We would love to help you restock your favorite items: {last_items}.\n\nBest, Sales Team"
        )
        email_snippet = f"Dear {customer_name}, We notice you haven't ordered in 60 days..."


    subject_line = "We Miss You! Special check-in from Sales Team"
    delivery_status = send_email(customer_email, subject_line, email_content)

    log_data.append({
        "Sent Date": today.strftime("%Y-%m-%d"),
        "Customer Name": customer_name,
        "Customer Email": customer_email,
        "Prompt Used": prompt,
        "Email Snippet": email_snippet,
        "Delivery Status": delivery_status  
    })

log_df = pd.DataFrame(log_data)
output_file = "Project_3_Email_Logs.xlsx"
log_df.to_excel(output_file, index=False)
