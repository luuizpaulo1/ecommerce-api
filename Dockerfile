FROM python:3.9.5

COPY . .

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

CMD [ "python", "manager.py" ]