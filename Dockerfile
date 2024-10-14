# Base Python image
FROM python:3.12-alpine

<<<<<<< HEAD
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    linux-headers
LABEL maintainer="https://github.com/prowler-cloud/prowler"

# Update system dependencies and install essential tools
# hadolint ignore=DL3018
RUN apk --no-cache upgrade && apk --no-cache add curl git
=======
# Maintainer information
LABEL maintainer="https://github.com/shubham-affinsys/prowler-svc"

# Update system dependencies and install essential tools
RUN apk --no-cache upgrade && \
    apk --no-cache add curl git gcc python3-dev musl-dev linux-headers
>>>>>>> parent of 1dc793b (update: removed unused function from myauth.auth)

# Create non-root user
RUN mkdir -p /home/prowler && \
    echo 'prowler:x:1000:1000:prowler:/home/prowler:' > /etc/passwd && \
    echo 'prowler:x:1000:' > /etc/group && \
    chown -R prowler:prowler /home/prowler

<<<<<<< HEAD
=======
# Switch to the non-root user
>>>>>>> parent of 1dc793b (update: removed unused function from myauth.auth)
USER prowler

# Set working directory
WORKDIR /home/prowler
<<<<<<< HEAD
=======

# Copy necessary files
COPY requirements.txt /home/prowler/requirements.txt
>>>>>>> parent of 1dc793b (update: removed unused function from myauth.auth)
COPY prowler/  /home/prowler/prowler/
COPY dashboard/ /home/prowler/dashboard/
COPY myauth/ /home/prowler/myauth/
COPY pyproject.toml /home/prowler/
<<<<<<< HEAD
COPY requirements.txt /home/prowler/  
COPY README.md /home/prowler

# Install Python dependencies
ENV HOME='/home/prowler'
ENV PATH="$HOME/.local/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt  
=======
COPY README.md /home/prowler/

# Upgrade pip, setuptools, and wheel, then install project dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r /home/prowler/requirements.txt
>>>>>>> parent of 1dc793b (update: removed unused function from myauth.auth)

# Add the local bin directory to PATH to ensure prowler command is available
ENV PATH="/home/prowler/.local/bin:${PATH}"

# Install the project, ensuring the prowler command is available
RUN pip install --no-cache-dir . && \
    echo "Prowler installed in: $(which prowler)"

# Uninstall deprecated dash dependencies (if not used anymore)
RUN pip uninstall dash-html-components -y && \
    pip uninstall dash-core-components -y

# Switch back to the root user to clean up unnecessary files
USER 0
RUN rm -rf /home/prowler/prowler /home/prowler/pyproject.toml /home/prowler/README.md /home/prowler/build /home/prowler/prowler.egg-info

<<<<<<< HEAD
# Set environment variables for Auth0
ENV AUTH0_CLIENT_ID=dAH2Ygr0Lk7m1LMJP6XxTI2HDnPpChud
ENV AUTH0_CLIENT_SECRET=9DKDv0hObCbiLiFAajFqi2ciraC2pdg2M6MsUaupdsywXN4Popn3iVzu7MZo1grC
ENV AUTH0_DOMAIN=dev-bc7mwy7zlu55zrov.us.auth0.com
ENV APP_SECRET_KEY=my_secret
=======
# Set environment variables for Auth0 (make sure to replace sensitive data with environment secrets in production)
>>>>>>> parent of 1dc793b (update: removed unused function from myauth.auth)


# Switch back to the prowler user
USER prowler
<<<<<<< HEAD
ENTRYPOINT ["prowler dashboard"] 
=======

# Entry point: run the Prowler dashboard
ENTRYPOINT ["sh", "-c", "prowler dashboard"]
>>>>>>> parent of 1dc793b (update: removed unused function from myauth.auth)
