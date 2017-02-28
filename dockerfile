FROM tiangolo/uwsgi-nginx-flask:flask

COPY requirements.txt /tmp/

COPY . /tmp/PerformanceSummary/

COPY resources/performance.db /resources/

RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

COPY ./app /app

WORKDIR /tmp/PerformanceSummary

RUN python setup.py install

WORKDIR /app

WORKDIR /app

ENV MESSAGE "PerformanceSummary is running..."


