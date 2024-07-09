FROM python:3.12.3-slim

WORKDIR /app

COPY . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app 
USER appuser

EXPOSE 8000

ENV PYTHONPATH "${PYTHONPATH}:/app/app"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]