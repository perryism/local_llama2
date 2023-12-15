FROM pytorch/pytorch

RUN apt update && apt install -y \
    git \
    build-essential

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

RUN CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python

COPY . /app

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0
