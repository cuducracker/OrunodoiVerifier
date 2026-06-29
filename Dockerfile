# Use the stable Python 3.12 environment from Microsoft Playwright
FROM mcr.microsoft.com/playwright/python:v1.50.0-noble

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first
COPY requirements.txt .

# FIX: Force upgrade pip and explicitly install the missing compilation tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install your project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port Gunicorn will run on
EXPOSE 10000

# Start the application with an increased timeout for long verifications
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "120", "app.gui:app"]