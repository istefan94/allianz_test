FROM python:3.12

WORKDIR /user_management

COPY requirements.txt api_client.py logger.py set_user_emails.py ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./set_user_emails.py" ]
