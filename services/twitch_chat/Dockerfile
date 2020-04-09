FROM python:3.7.3

RUN apt-get update && apt-get install -y cmake bison flex

ENV PYTHONPATH=/usr/src/app/
ENV PATH="$PATH:/root/.local/bin"

WORKDIR /usr/src/app

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

CMD ["/usr/src/app/entrypoint.sh"]
