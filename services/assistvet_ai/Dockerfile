FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install -e .
EXPOSE 10120
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10120"]