# Use the official Microsoft Playwright image which comes with Python and ALL browser dependencies pre-installed
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port Gunicorn will run on
EXPOSE 10000

# Start the application with an increased 5-minute timeout for long verifications
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "300", "app.gui:app"]