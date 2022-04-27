# syntax=docker/dockerfile:1

# specify python base version
FROM python:3
# define working directory
WORKDIR /code
# copy dependencies file
COPY ./requirements.txt /code
# install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# copy all code to working directory
COPY ./app /code/app
# execute our application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]