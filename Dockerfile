# Dockerfile
# Use official Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . ./

# Expose Streamlit default port
EXPOSE 8501

# Set environment variables for Streamlit
ENV PYTHONUNBUFFERED=1

# Run the Streamlit app
CMD ["streamlit", "run", "app/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
