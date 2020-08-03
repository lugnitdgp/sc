FROM python:3

ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip
RUN mkdir /var/app
WORKDIR /var/app    
COPY requirements.txt /var/app/
RUN pip install -r requirements.txt
COPY . /var/app/. 
EXPOSE 8000
