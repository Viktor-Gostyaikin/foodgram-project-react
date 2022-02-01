FROM python:3.7-slim
WORKDIR /backend
COPY backend .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "127.0.0.1:8000" ]
