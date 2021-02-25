FROM python:3.9-slim

RUN apt update && apt install -y ffmpeg wget

COPY requirements.txt ./
RUN pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

ENV PORT=3000
ENV py_env=production

COPY . ./
RUN cd api/models && wget -q https://dl.fbaipublicfiles.com/demucs/v2.0/demucs_extra.th -O model.th

CMD ["python", "api/main.py"]
