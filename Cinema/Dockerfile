From alpine:latest

RUN apk add --no-cache py-pip
RUN pip3 install --upgrade pip

COPY . /service
WORKDIR /service/demo

RUN pip3 install -r requirements.txt

EXPOSE 5001

WORKDIR /service/demo/demo-ui
ENTRYPOINT ["python3"]
CMD ["__init__.py"]