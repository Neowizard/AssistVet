FROM mcr.microsoft.com/playwright/python:v1.47.0-noble
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install -e .
EXPOSE 10122
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10122"]