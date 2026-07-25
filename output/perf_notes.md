# Performance Notes

## Load Testing

- Endpoint: `/api/v1/screener`
- Concurrent Requests: 10
- Total Execution Time: 0.15 seconds
- Result: Passed

## Dashboard Performance

- Screen Tested: Company Profile
- Number of Tickers: 5
- Load Time: Under 3 seconds for each company
- Result: Passed

## End-to-End Testing

- FastAPI: Running on Port 8000
- Streamlit: Running on Port 8501
- Port Conflict: None
- Dashboard Data Loading: Successful

## Bottlenecks

No significant performance bottlenecks were observed during testing.

## Recommendations

- SQLite indexes added on frequently queried columns.
- Current response times satisfy the project requirements.