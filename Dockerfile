# FROM python:3.10

FROM amazon/aws-lambda-python:3.10
# RUN yum groupinstall "Development Tools" -y

COPY ./api ./api
COPY ./log ./log 
COPY ./response ./response
COPY ./tags ./tags
COPY ./techno_check ./techno_check
COPY ./util ./util
COPY ./main.py ./main.py
COPY ./requirements.txt ./requirements.txt
# COPY ./api/__init__.py __init__.py


# RUN chmod 777 ./api/*
# RUN chmod 777 ./*
RUN pip install -r ./requirements.txt


#for lambda

CMD ["api.main.handler"] 



# EXPOSE 8001
# CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8001"]