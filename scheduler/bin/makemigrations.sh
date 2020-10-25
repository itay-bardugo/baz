if [ -z $1 ]
then
    echo "app name is missing. command should be like: makemigrations [appname]"
    sleep 3
    exit
fi

docker exec baz-wsgi-scheduler python3.8 scheduler/manage.py makemigrations $1
sleep 10