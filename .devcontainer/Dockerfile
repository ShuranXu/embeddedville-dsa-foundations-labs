FROM ubuntu:24.04@sha256:a2d43bffc46670d7108bb3c0468c67c5557c4c92e83e1e34cbff1322ad1b94dc

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc-13 make python3 git ca-certificates \
    && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 100 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/embeddedville-dsa-foundations-labs

