FROM python:3.9-slim

RUN apt update && apt install -y ffmpeg wget

COPY requirements.txt ./
RUN pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

ENV PORT=3000
ENV HOST=hoge
ENV py_env=production

COPY . ./
RUN cd api/models && wget https://github.com/Yotsuyubi/music-separater/releases/download/v1.0/model.th

CMD ["python", "api/main.py"]
