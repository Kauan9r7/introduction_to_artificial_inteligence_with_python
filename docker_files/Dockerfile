FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /workspace

# Install essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and packaging tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install core Python packages for AI, Data Science, and Jupyter
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    scipy \
    matplotlib \
    scikit-learn \
    jupyter \
    notebook \
    ipykernel

EXPOSE 8888 5000

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
