FROM python:alpine

WORKDIR /code

# Instala dependências
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia todo o projeto, incluindo a pasta "app/"
COPY . /code

# Exporta a pasta /code para o PYTHONPATH (contém a pasta "app/")
ENV PYTHONPATH="/code"

# Executa uvicorn usando o caminho correto para o app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
