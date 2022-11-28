FROM python:3.7

WORKDIR /app

COPY requirements.txt ./
COPY entrypoint.sh ./

# install requirements
RUN pip install -U "setuptools<46" 

RUN pip install -r ./requirements.txt

COPY . ./

EXPOSE 5001

# CMD ["gunicorn", "-b", "0.0.0.0:5001", "run:app"]
RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["sh", "./entrypoint.sh"]
