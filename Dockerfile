FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg libegl1-mesa libglvnd-dev libglvnd0

RUN mkdir -p /usr/share/glvnd/egl_vendor.d

RUN echo '{"file_format_version":"1.0.0","ICD":{"library_path":"/usr/lib/x86_64-linux-gnu/libEGL_nvidia.so.0"}}' > /usr/share/glvnd/egl_vendor.d/10_nvidia.json

ENV __EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/10_nvidia.json

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python", "-u", "rp_handler.py"]