FROM continuumio/miniconda3:latest

# Setup package manager
RUN sed -i 's|http://|https://|g' /etc/apt/sources.list.d/*.sources && \
    apt-get update -q

RUN apt-get install -y gobject-introspection libgirepository-1.0-1 \
    libcairo2 libcairo-gobject2 libpango-1.0-0 libpangocairo-1.0-0 \
    gir1.2-pango-1.0 gir1.2-cairo-1.0 gir1.2-gtk-4.0

RUN conda install python=3.12 -y

RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r && \
    conda tos accept --override-channels --channel conda-forge

RUN conda install -c conda-forge pycairo pygobject manimpango -y

RUN set -eux; cat > test_pango.py <<'PY'
from pixel_renderer import render_text
render_text(text="test", block_size=16, dpi=120, font_size=12)
print("✅ Successfully rendered text.")
PY

CMD ["python", "test_pango.py"]

# docker build -t renderer .
# docker run -it --rm renderer