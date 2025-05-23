from fastapi import FastAPI, Query
from html import escape

app = FastAPI()

@app.get("/sanitize")
def sanitize_input(user_input: str = Query(..., min_length=1, max_length=100)):
    """
    Endpoint to sanitize user input.
    - Accepts a query parameter `user_input`.
    - Sanitizes the input to prevent security issues.
    """
    sanitized_input = escape(user_input)  
    return {"sanitized_input": sanitized_input}
