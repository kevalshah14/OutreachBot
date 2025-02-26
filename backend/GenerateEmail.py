import pandas as pd
from google import genai
import os
import time

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def generate_email(name, company, description, context, company_description):
    sender_name = "Sara Filipcic"
    sender_position = "CEO"
    sender_website = "https://www.behumane.ai/"
    prompt = f"""
    Write a professional email to {name} at {company}.
    
    Context:
    {context}
    
    Recipient's Company Description:
    {description}
    
    Our Company Description:
    {company_description}
    
    The email should include:
    - Polite introduction
    - Mention our interest in potential collaboration
    - Propose a follow-up meeting
    - Professional closing
    - Signed by {sender_name}, {sender_position}
    - Include our company website: {sender_website}

    Please ensure the output is in markdown format. Use headers, bullet points, and links as needed. The email should be concise (3-4 short paragraphs max).
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    
    print(f"Generated email for {name} at {company}: {response.text}")
    return response.text if response else "Error generating email"

def process_csv(file_path, company_description):
    df = pd.read_csv(file_path, delimiter=',', encoding='utf-8')
    
    # Drop rows with NaN values in required columns
    df.dropna(subset=["Name", "Company"], inplace=True)
    
    email_contents = []
    
    for index, row in df.iterrows():
        # Convert to string and strip any whitespace
        name = str(row.get("Name", "")).strip()
        company = str(row.get("Company", "")).strip()
        description = str(row.get("Description", "No description available")).strip()
        context = str(row.get("Context", "No context provided")).strip()
        
        if not name or not company:
            print(f"Skipping row {index} due to missing name or company.")
            continue
        
        print(f"Processing {name} at {company}...")
        
        try:
            email_content = generate_email(name, company, description, context, company_description)
            email_contents.append(email_content)
            print(f"Email for {name} at {company} generated successfully.\n")
        except Exception as e:
            print(f"Error generating email for {name}: {str(e)}")
            email_contents.append("Error generating email")
        
        # Update the DataFrame with the generated email
        df.at[index, "Generated Email"] = email_content
        
        # Save the DataFrame to the CSV file after each email generation
        output_file = file_path.replace(".csv", "_with_emails.csv")
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Updated CSV saved as {output_file}")

my_company_description = "Be Human(e) is a digital mental health startup that has developed RHEA, an AI-driven parenting coaching platform. RHEA is designed to empower parents of pre-teens and teens by providing emotionally intelligent AI support, guided by experts and grounded in over 40 years of research and evidence-based practices. The platform aims to assist families in navigating the complexities of modern parenting by offering personalized solutions that enhance parent-child relationships and promote overall family well-being."

process_csv("Untitled spreadsheet - Fundraising.csv", my_company_description)
