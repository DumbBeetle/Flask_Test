FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV DEPLOY_DATE=${DEPLOY_DATE}
ENV DEPLOY_TIME=${DEPLOY_TIME}
ENV GIT_SHA=${GIT_SHA}
ENV HOST=0.0.0.0
ENV PORT=5000

COPY . .

# Expose port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]