FROM python:3.11-alpine AS base


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apk update

RUN apk --no-cache add curl gnupg
RUN curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/msodbcsql18_18.3.2.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/mssql-tools18_18.3.1.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/msodbcsql18_18.3.2.1-1_amd64.sig
RUN curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/mssql-tools18_18.3.1.1-1_amd64.sig

RUN curl https://packages.microsoft.com/keys/microsoft.asc  | gpg --import -

RUN apk add --allow-untrusted msodbcsql18_18.3.2.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools18_18.3.1.1-1_amd64.apk

RUN apk add gcc libc-dev g++ libffi-dev libxml2 unixodbc-dev postgresql-dev

WORKDIR /app/
COPY requirements.txt .

RUN pip install --trusted-host pip.aptekar.local -i http://pip.aptekar.local -r requirements.txt && pip cache purge && rm requirements.txt

COPY ./ ./
ENTRYPOINT ["python", "-m"]
CMD ["vaptekecustomers"]


