FROM python:3.12-alpine

LABEL maintainer="https://github.com/prowler-cloud/prowler"

# Update system dependencies and install essential tools
#hadolint ignore=DL3018
RUN apk --no-cache upgrade && apk --no-cache add curl git

# Create nonroot user
RUN mkdir -p /home/prowler && \
    echo 'prowler:x:1000:1000:prowler:/home/prowler:' > /etc/passwd && \
    echo 'prowler:x:1000:' > /etc/group && \
    chown -R prowler:prowler /home/prowler
USER prowler

# Copy necessary files
WORKDIR /home/prowler
COPY myauth/ /home/prowler/myauth/
COPY prowler/  /home/prowler/prowler/
COPY dashboard/ /home/prowler/dashboard/
COPY pyproject.toml /home/prowler
COPY README.md /home/prowler
RUN python -c "import sys; print(sys.path)"


# Install Python dependencies
ENV HOME='/home/prowler'
ENV PATH="$HOME/.local/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir .

# Remove deprecated dash dependencies
RUN pip uninstall dash-html-components -y && \
    pip uninstall dash-core-components -y

# Remove Prowler directory and build files
USER 0
RUN rm -rf /home/prowler/prowler /home/prowler/pyproject.toml /home/prowler/README.md /home/prowler/build /home/prowler/prowler.egg-info

ENV AUTH0_CLIENT_ID=dAH2Ygr0Lk7m1LMJP6XxTI2HDnPpChud
ENV AUTH0_CLIENT_SECRET=9DKDv0hObCbiLiFAajFqi2ciraC2pdg2M6MsUaupdsywXN4Popn3iVzu7MZo1grC
ENV  AUTH0_DOMAIN=dev-bc7mwy7zlu55zrov.us.auth0.com
ENV  APP_SECRET_KEY=my_secret

USER prowler
ENTRYPOINT ["sh", "-c", "prowler dashboard"]

RUN python -c "import sys; print(sys.path)"