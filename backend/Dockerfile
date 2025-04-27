FROM alpine

RUN apk add --no-cache python3 py3-pip

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

ADD requirements.pip requirements.pip
RUN pip install -r requirements.pip

ADD src src

EXPOSE 5000

CMD ["python", "/src/run.py"]
