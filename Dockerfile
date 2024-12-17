FROM python:3.10
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install poetry
COPY . .
RUN make install