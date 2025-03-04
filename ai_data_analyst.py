import json
import tempfile
import csv
import streamlit as st
import pandas as pd
import duckdb
import requests
import re
import time

# Function to preprocess and save the uploaded file
def preprocess_and_save(file):
    try:
        # Read the uploaded file into a DataFrame
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, encoding='utf-8', na_values=['NA', 'N/A', 'missing'])
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file, na_values=['NA', 'N/A', 'missing'])
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None, None, None
        
        # Ensure string columns are properly quoted
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).replace({r'"': '""'}, regex=True)
        
        # Parse dates and attempt numeric conversion
        for col in df.columns:
            if 'date' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')
            elif df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    # Keep as is if conversion fails
                    pass
        
        # Create a temporary file to save the preprocessed data
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_path = temp_file.name
            # Save the DataFrame to the temporary CSV file with quotes around string fields
            df.to_csv(temp_path, index=False, quoting=csv.QUOTE_ALL)
        
        return temp_path, df.columns.tolist(), df  # Return the DataFrame as well
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None, None, None

# Function to generate a SQL query using Hugging Face Inference API with the DeepSeek model

def generate_sql(user_query, hf_token, max_retries=3):
    API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
    headers = {"Authorization": f"Bearer {hf_token}"}
    system_prompt = (
        "translate English to SQL: "
        "You are an expert data analyst. Generate a SQL query to solve the user's query. "
        "Return only the SQL query, enclosed in triple backticks with 'sql' as the language marker."
    )
    prompt = f"{system_prompt}\nUser query: {user_query}"
    payload = {"inputs": prompt, "parameters": {"temperature": 0.67}}

    for attempt in range(max_retries):
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        if response.status_code == 503:
            # If service unavailable, wait before retrying
            wait_time = 2 ** attempt
            st.warning(f"Service unavailable. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            continue
        elif response.status_code != 200:
            raise Exception(f"Error: Received status code {response.status_code} with message: {response.text}")
        
        try:
            result = response.json()
        except ValueError:
            raise Exception("Invalid JSON response: " + response.text)
        
        if isinstance(result, dict) and "error" in result:
            raise Exception(result["error"])
        
        # Extract generated text from the first result
        generated_text = ""
        if isinstance(result, list) and result and "generated_text" in result[0]:
            generated_text = result[0]["generated_text"]
        else:
            generated_text = str(result)
        
        match = re.search(r"```sql\s*(.*?)\s*```", generated_text, re.DOTALL)
        if match:
            sql_query = match.group(1)
        else:
            sql_query = generated_text.strip()
        return sql_query
    
    raise Exception("Max retries exceeded. Service remains unavailable.")

# Streamlit app
st.title("📊 Auto Data Analyst Agent")

# Sidebar for API tokens
with st.sidebar:
    st.header("API Keys")
    hf_token = st.text_input("Enter your Hugging Face API token:", type="password")
    if hf_token:
        st.session_state.hf_token = hf_token
        st.success("API token saved!")
    else:
        st.warning("Please enter your Hugging Face API token to proceed.")

# File upload widget
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None and "hf_token" in st.session_state:
    # Preprocess and save the uploaded file
    temp_path, columns, df = preprocess_and_save(uploaded_file)
    
    if temp_path and columns and df is not None:
        # Display the uploaded data as an interactive table
        st.write("Uploaded Data:")
        st.dataframe(df)
        st.write("Uploaded columns:", columns)
        
        # Create a DuckDB in-memory connection and register the CSV file as a table
        con = duckdb.connect(database=':memory:')
        con.execute(f"CREATE TABLE uploaded_data AS SELECT * FROM read_csv_auto('{temp_path}')")
        
        # Main query input widget
        user_query = st.text_area("Ask a query about the data:")
        
        st.info("💡 Check your terminal for a clearer output of the agent's response")
        
        if st.button("Submit Query"):
            if user_query.strip() == "":
                st.warning("Please enter a query.")
            else:
                try:
                    with st.spinner('Processing your query...'):
                        # Generate SQL query using the Hugging Face API with the new model
                        sql_query = generate_sql(user_query, st.session_state.hf_token)
                        st.write("Generated SQL Query:")
                        st.code(sql_query, language='sql')
                        
                        # Execute the generated SQL query using DuckDB
                        result_df = con.execute(sql_query).fetchdf()
                        
                        st.write("Query Result:")
                        st.dataframe(result_df)
                except Exception as e:
                    st.error(f"Error processing query: {e}")
                    st.error("Please try rephrasing your query or check if the data format is correct.")
