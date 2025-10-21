FROM continuumio/miniconda3:latest

# Setup package manager
RUN sed -i 's|http://|https://|g' /etc/apt/sources.list.d/*.sources && \
    apt-get update -q

RUN apt-get install -y gobject-introspection libgirepository-1.0-1 libgirepository1.0-dev \
    libcairo2 libcairo2-dev libcairo-gobject2 libpango-1.0-0 libpangocairo-1.0-0 \
    gir1.2-pango-1.0 gir1.2-cairo-1.0 gir1.2-gtk-4.0 \
    pkg-config python3-dev

# Install Python and conda dependencies
RUN conda install python=3.12 -y && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r && \
    conda tos accept --override-channels --channel conda-forge && \
    conda install -c conda-forge manimpango -y

# Install pycairo and PyGObject via pip to ensure proper integration
# Use PyGObject < 3.48 which supports girepository-1.0
RUN pip install --no-cache-dir pycairo 'PyGObject<3.48'

COPY . /pixel_renderer
WORKDIR /pixel_renderer
RUN pip install .

RUN set -eux; cat > test_pango.py <<'PY'
from pixel_renderer import render_text
render_text(text="test", block_size=16, font_size=12)
print("✅ Successfully rendered text.")
PY

CMD ["python", "test_pango.py"]

# docker build -t renderer .
# docker run --rm renderer