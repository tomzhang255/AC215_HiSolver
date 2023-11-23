FROM python:3.9

WORKDIR /hisolver-py

COPY requirements.txt .
COPY ./src ./src
COPY ./config.json ./config.json

RUN apt-get update && \
    apt-get install -y build-essential python3-dev libcairo2-dev libpango1.0-dev ffmpeg texlive texlive-latex-extra

RUN pip install -r requirements.txt

CMD ["uvicorn", "src.chromadb:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]