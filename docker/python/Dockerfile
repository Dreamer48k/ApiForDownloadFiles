FROM python:3.10.12

WORKDIR /app
COPY . .

#for bonsai
# RUN apt-get update && apt-get upgrade -y
# RUN apt-get install -y libldap2-dev ldap-utils 
# RUN apt-get install -y libsasl2-dev

#RUN python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt



CMD python ./main.py
