FROM amazon/aws-eb-python:3.4.2-onbuild-3.5.1

# Expose port
EXPOSE 8080
ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip
RUN mkdir /var/app
WORKDIR /var/app    
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /var/app/. 
 EXPOSE 8000
