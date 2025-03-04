# Auto-Data-Analyst Agent

This repository hosts an **Auto Data Analyst Agent** application that allows you to analyze your data (CSV or Excel files) using natural language queries. The agent translates your queries into SQL, executes them against your uploaded dataset, and returns the results—all without requiring you to know SQL.

## Key Features

- **File Upload:** Upload CSV or Excel files (up to 200MB).  
- **Data Preview:** Automatically display the uploaded data in a table for quick inspection.  
- **Column Display:** Show the column names detected in the uploaded dataset.  
- **API Token Integration:** Enter your Hugging Face Inference API token in the sidebar to enable AI-driven query generation.  
- **Natural Language Queries:** Type questions like “Find the maximum petal length in the iris dataset.” The agent converts these questions to SQL.  
- **SQL Generation & Execution:** The generated SQL is shown to the user, and the query result is displayed in a table.  

## How It Works

1. **Set Your API Token**  
   - In the left sidebar, enter your Hugging Face API token. This token is used to access the AI model that translates your natural language queries into SQL statements.

2. **Upload a Dataset**  
   - Click on the “Upload a CSV or Excel file” widget and select your data file.  
   - The agent will read your file, display the data in a table, and show the detected column names.

3. **Ask a Question**  
   - In the text area labeled “Ask a query about the data,” type your question in natural language. For example, “Find the maximum petal length in the iris dataset named df.”

4. **Generate & Execute SQL**  
   - Click the “Submit Query” button.  
   - The agent generates an SQL query (e.g., `SELECT MAX(petal_length) FROM df`) and displays it.  
   - The query is then executed on your dataset, and the result is shown in the “Query Result” section.

5. **View the Result**  
   - Check the result of your query in the displayed table below.  
   - For more complex queries, you can reference multiple columns or filter rows, and the agent will produce the relevant SQL.

## Example Workflow

1. **Enter Hugging Face Token**  
   - In the sidebar, paste your Hugging Face API token (e.g., `hf_XXXXXXXXXX`).

2. **Upload `iris.csv`**  
   - The data is displayed in a table with columns `sepal_length`, `sepal_width`, `petal_length`, `petal_width`, and `species`.

3. **Ask a Query**  
   - Type: “Find the maximum petal length in the iris dataset named df.”  
   - Click “Submit Query.”

4. **Generated SQL**  
   - `SELECT MAX(petal_length) FROM df`  
   - The agent runs this query.

5. **Query Result**  
   - A table with one column and one row shows the maximum `petal_length`, e.g., `6.9`.

## Troubleshooting

- **503 or Service Unavailable:** The Hugging Face endpoint may be busy. Wait and try again, or confirm the model is publicly accessible.
- **Invalid API Token:** Ensure your token is valid and you have the right to use the chosen model.
- **Data Formatting Errors:** Make sure your CSV or Excel file is valid and not corrupt. For Excel files, only `.xlsx` format is supported.

## Contributing

1. **Fork** the repository.  
2. **Create** a new feature branch (`git checkout -b feature/my-feature`).  
3. **Commit** your changes (`git commit -m 'Add some feature'`).  
4. **Push** to the branch (`git push origin feature/my-feature`).  
5. **Open** a Pull Request.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

**Enjoy streamlined data analysis without the need to manually write SQL queries!**
