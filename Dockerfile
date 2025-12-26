FROM python:3.10-slim

# Create working directory
WORKDIR /app

# Copy only necessary files
COPY flaskApi.py /app/
COPY model /app/model/
COPY requirements.txt /app/

# Install requirements
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run Flask app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "flaskApi:app"]
