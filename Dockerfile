FROM python:3.14-slim

# Setup package manager
RUN sed -i 's|http://|https://|g' /etc/apt/sources.list.d/*.sources
RUN apt-get update -q

# Install rendering system dependencies
RUN apt-get install -y libgirepository-1.0-1 libcairo2 gir1.2-pango-1.0 pkg-config libcairo2-dev libgirepository1.0-dev

COPY . /pixel-renderer
WORKDIR /pixel-renderer
RUN pip install .

CMD ["python", "-c", "from pixel_renderer import render_text; print(render_text('test', 16, 12).shape); print('✅')"]

# docker build -t renderer .
# docker run -it --rm renderer