FROM registry.access.redhat.com/hi/python:3.14-builder AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0 \
    UV_CACHE_DIR=/tmp/.cache/uv

USER root

# Copy and run tesseract installer script
COPY --chmod=755 install-tesseract.sh /tmp/install-tesseract.sh
RUN /tmp/install-tesseract.sh

WORKDIR /app
RUN --mount=type=cache,target=/tmp/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project
COPY . /app
RUN --mount=type=cache,target=/tmp/.cache/uv \
    uv sync --locked

# Download NLTK data to /app/nltk_data
RUN --mount=type=cache,target=/tmp/.cache/uv \
    uv run python -c "import nltk; \
    nltk.download('punkt', download_dir='/app/nltk_data'); \
    nltk.download('stopwords', download_dir='/app/nltk_data'); \
    nltk.download('punkt_tab', download_dir='/app/nltk_data'); \
    nltk.download('wordnet', download_dir='/app/nltk_data')"


# Final image
FROM registry.access.redhat.com/hi/python:3.14

# Copy tesseract static binary and traineddata from the builder
COPY --from=builder /opt/tesseract /opt/tesseract

# Copy the application from the builder
COPY --from=builder --chown=65532:0 /app /app

# Place executables in the environment at the front of the path
ENV PATH="/opt/tesseract/bin:/app/.venv/bin:$PATH"
ENV TESSDATA_PREFIX="/opt/tesseract/share/tessdata"
ENV NLTK_DATA="/app/nltk_data"

# Use `/app` as the working directory
WORKDIR /app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
