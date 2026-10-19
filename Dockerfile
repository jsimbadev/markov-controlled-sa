FROM debian:bookworm-slim

ARG QUARTO_VERSION=1.9.37

# Install the complete HTML/PDF and validation toolchain up front. Quarto's
# automatic TeX package installation remains disabled in _quarto.yml.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        lmodern \
        make \
        python3 \
        texlive-fonts-recommended \
        texlive-latex-extra \
        texlive-luatex \
    && rm -rf /var/lib/apt/lists/*

RUN cd /tmp \
    && arch="$(dpkg --print-architecture)" \
    && curl --fail --location --retry 3 \
        "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${arch}.deb" \
        --output "quarto-${QUARTO_VERSION}-linux-${arch}.deb" \
    && curl --fail --location --retry 3 \
        "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-checksums.txt" \
        --output checksums.txt \
    && sha256sum --check --ignore-missing checksums.txt \
    && dpkg -i "quarto-${QUARTO_VERSION}-linux-${arch}.deb" \
    && rm "quarto-${QUARTO_VERSION}-linux-${arch}.deb" checksums.txt

WORKDIR /workspace
ENV USE_DOCKER=0 \
    HOME=/tmp \
    PREVIEW_HOST=0.0.0.0 \
    PREVIEW_FLAGS=--no-browser

EXPOSE 4200
CMD ["make", "preview"]
