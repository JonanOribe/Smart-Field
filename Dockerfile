FROM python:3

RUN pip install --upgrade pip

WORKDIR ./

COPY requirements.txt .

ADD main.py /

RUN pip install -r requirements.txt

CMD [ "python", "./main.py IA" ]