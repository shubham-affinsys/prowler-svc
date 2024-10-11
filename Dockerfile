FROM python:3.12-alpine

LABEL maintainer="https://github.com/prowler-cloud/prowler"

# Update system dependencies and install essential tools
# hadolint ignore=DL3018
RUN apk --no-cache upgrade && apk --no-cache add curl git

# Create non-root user
RUN mkdir -p /home/prowler && \
    echo 'prowler:x:1000:1000:prowler:/home/prowler:' > /etc/passwd && \
    echo 'prowler:x:1000:' > /etc/group && \
    chown -R prowler:prowler /home/prowler

USER prowler

# Copy necessary files
WORKDIR /home/prowler
COPY prowler/  /home/prowler/prowler/
COPY dashboard/ /home/prowler/dashboard/
COPY myauth/ /home/prowler/myauth/
COPY pyproject.toml /home/prowler/
COPY requirements.txt /home/prowler/  
COPY README.md /home/prowler

# Install Python dependencies
ENV HOME='/home/prowler'
ENV PATH="$HOME/.local/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt  # Install from requirements.txt

# Remove deprecated dash dependencies
RUN pip uninstall dash-html-components -y && \
    pip uninstall dash-core-components -y

# Remove Prowler directory and build files
USER 0
RUN rm -rf /home/prowler/prowler /home/prowler/pyproject.toml /home/prowler/README.md /home/prowler/build /home/prowler/prowler.egg-info

# Set environment variables for Auth0
ENV AUTH0_CLIENT_ID=dAH2Ygr0Lk7m1LMJP6XxTI2HDnPpChud
ENV AUTH0_CLIENT_SECRET=9DKDv0hObCbiLiFAajFqi2ciraC2pdg2M6MsUaupdsywXN4Popn3iVzu7MZo1grC
ENV AUTH0_DOMAIN=dev-bc7mwy7zlu55zrov.us.auth0.com
ENV APP_SECRET_KEY=my_secret

USER prowler
ENTRYPOINT ["python", "-m", "prowler"]  # Change this to the main entry point of your application
