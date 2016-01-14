# mesos-admin
Mesos admin


# dev

```sh
# run dev container
docker-compose up -d python

# execute into container
docker exec -it mesosadmin_python_1 bash

# install runtime
apt-get install -y git libpq-dev

pip3 install -r requirements.txt

# migrate database
./manage.py migrate

# run app
./manage.py runserver 0.0.0.0:8000
```

Access:
http://127.0.0.1:8000/token-gdrive/



# TODO
1. demo data



