FROM mambaorg/micromamba:2.9.0-debian13

# Rendering stack from conda-forge, which ships the latest Pango, cairo and PyGObject
RUN micromamba install -y -n base -c conda-forge python=3.12 pango pycairo pygobject && \
    micromamba clean -a -y

ARG MAMBA_DOCKERFILE_ACTIVATE=1
COPY --chown=$MAMBA_USER:$MAMBA_USER . /pixel-renderer
WORKDIR /pixel-renderer
RUN pip install --no-cache-dir ".[pangocairo]"

CMD ["python", "-c", "from pixel_renderer import render_text; print(render_text('test', 16, 12).shape); print('✅')"]

# docker build -t renderer .
# docker run -it --rm renderer
