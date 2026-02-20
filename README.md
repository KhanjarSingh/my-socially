# my-socially

## Description
My Socially is a comprehensive project that analyzes marketing spend data and exposes it via a Node.js backend. The project consists of a Python script that reads marketing spend data, cleans it, calculates key metrics (ROAS, CPC, CPA), generates channel-wise and monthly summaries, produces actionable insights, and exports the results to a JSON file. The Node.js backend then serves this data through a RESTful API endpoint.

## Requirements and Libraries

### Python
- Python 3.x
- `pandas`
- `numpy`
- `json` (built-in)
- `sys` (built-in)

### Node.js
- Node.js (v14 or higher recommended)
- `express`: Fast, unopinionated, minimalist web framework for Node.js.
- `cors`: Express middleware to enable Cross-Origin Resource Sharing.
- `fs`: File system standard library (built-in).

## How to Run the Python Analysis Script
1. Navigate to the project root directory.
2. Ensure your data file (`marketing_spend_data.csv`) is present in the root directory.
3. Run the analysis script using Python:
   ```bash
   python spend_analysis.py [optional_path_to_csv]
   ```
   If no argument is passed, it defaults to reading `marketing_spend_data.csv`.

## How to Generate `summary_data.json`
The `summary_data.json` file is automatically generated when you run the Python analysis script (`spend_analysis.py`). The script processes the raw CSV data, calculates the metrics, and exports the findings directly to `summary_data.json` in the current working directory.

## How to Run the Node.js Backend and Access the API
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install the necessary dependencies:
   ```bash
   npm install
   ```
3. Start the server:
   ```bash
   node server.js
   ```
4. The server will run on port `3000` by default (or the port specified in your `PORT` environment variable).
5. **Access the API endpoint:**
   Open a browser or use a tool like Postman or `curl` to visit:
   `http://localhost:3000/summary`

## Key Metrics and Findings
- **Overall ROAS:** 3.61x
- **Total Spend:** ~$46.3M
- **Total Revenue:** ~$167.0M
- **Total Conversions:** 760,490
- **Best Channel:** Email has the highest ROAS at 7.28x. Scaling budget here is highly recommended.
- **Worst Channel:** Instagram has the lowest ROAS at 2.91x, requiring immediate optimization.
- **Monthly Performance:** Stable performance month-over-month with ROAS consistently hovering around 3.57x - 3.63x.

## Example Output Snippets

### Python Console Output Snippet
```
Loading data...
Rows loaded: 7600
Calculating metrics...
Generating summary...
{'total_spend': 46303442.9, 'total_revenue': 166979422.66, 'total_conversions': 760490, 'overall_roas': 3.606198852655943}

Insights:
- Email is the highest performing channel with ROAS of 7.28x. Consider scaling budget.
- Instagram has the lowest ROAS of 2.91x. Optimization required.
...
summary_data.json exported successfully.
```

### JSON API Output (`/summary`) Snippet
```json
{
    "overall_metrics": {
        "total_spend": 46303442.9,
        "total_revenue": 166979422.66,
        "total_conversions": 760490,
        "overall_roas": 3.606198852655943
    },
    "insights": [
        "Email is the highest performing channel with ROAS of 7.28x. Consider scaling budget.",
        "Instagram has the lowest ROAS of 2.91x. Optimization required."
    ]
}
```

## Suggested Next Steps for Frontend/Dashboard Integration
1. **Develop a Frontend Dashboard:** Use modern frameworks like React, Vue, or Next.js to fetch data from `/summary` and visualize it.
2. **Chart Integration:** Use libraries like Chart.js, Recharts, or D3.js to render visually appealing pie charts for channel performance, line charts for monthly ROAS trends, and bar charts for total spend vs. revenue.
3. **Data Caching:** To reduce backend load from frequent API calls, implement caching (e.g., Redis) or save aggregated data temporarily on the backend.
4. **Dynamic Data Uploads:** Build a frontend flow that allows the marketing team to upload new CSVs and automatically trigger the Python script, rendering updated metrics seamlessly.
