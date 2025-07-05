FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]