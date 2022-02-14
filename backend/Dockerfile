FROM surnet/alpine-python-wkhtmltopdf:3.9.9-0.12.6-small
WORKDIR /backend
COPY backend .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
