# sudo apt-get update
cd .. 

[ -d venv ] && echo "File exist" || (echo "creating virtualenv" && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt)

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
