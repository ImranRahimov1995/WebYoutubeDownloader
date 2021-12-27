FROM python:3.8.10

WORKDIR /project


COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -r requirements.txt
RUN ["chmod", "+x", "entrypoint.sh"]


COPY . .

ENTRYPOINT ["sh", "entrypoint.sh" ]