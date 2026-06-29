# We switch from -jammy to -noble to get Python 3.12, which fully supports Pandas 3.0+
FROM mcr.microsoft.com/playwright/python:v1.44.0-noble

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port Gunicorn will run on
EXPOSE 10000

# Start the application with an increased timeout for long verifications
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "120", "app.gui:app"]