# Author: Cuong Tran
#
# Build: docker build -t tranhuucuong91/mesos-admin:0.1 .
# Run: docker run -d -p 8080:8080 --name mesos-admin-run tranhuucuong91/mesos-admin:0.1
#

FROM ubuntu:14.04
MAINTAINER Cuong Tran "tranhuucuong91@gmail.com"

# using apt-cacher-ng proxy for caching deb package
RUN echo 'Acquire::http::Proxy "http://172.17.0.1:3142/";' > /etc/apt/apt.conf.d/01proxy

ENV REFRESHED_AT 2015-01-14

RUN apt-get update -qq

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip build-essential python3-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git libpq-dev

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-pip

# clear apt-cacher-ng proxy
RUN rm -f /etc/apt/apt.conf.d/01proxy

RUN pip install -e git+https://github.com/tranhuucuong91/PyDrive.git#egg=PyDrive-master

COPY requirements.txt /mesos-admin/requirements.txt
RUN pip3 install -r /mesos-admin/requirements.txt

COPY . /mesos-admin/
WORKDIR /mesos-admin/

EXPOSE 8000

CMD ["./manage.py", "runserver", "0.0.0.0:8000"]

