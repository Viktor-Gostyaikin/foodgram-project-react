FROM surnet/alpine-python-wkhtmltopdf:3.7.3-0.12.6-full
WORKDIR /backend
COPY backend .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
