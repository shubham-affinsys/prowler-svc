# Base Python image
FROM python:3.12-alpine

# Maintainer information
LABEL maintainer="https://github.com/shubham-affinsys/prowler-svc"

# Update system dependencies and install essential tools
RUN apk --no-cache upgrade && \
    apk --no-cache add curl git gcc python3-dev musl-dev linux-headers

# Create non-root user
RUN mkdir -p /home/prowler && \
    echo 'prowler:x:1000:1000:prowler:/home/prowler:' > /etc/passwd && \
    echo 'prowler:x:1000:' > /etc/group && \
    chown -R prowler:prowler /home/prowler

# Switch to the non-root user
USER prowler

# Set working directory
WORKDIR /home/prowler

# Copy necessary files
COPY requirements.txt /home/prowler/requirements.txt
COPY prowler/  /home/prowler/prowler/
COPY dashboard/ /home/prowler/dashboard/
COPY myauth/ /home/prowler/myauth/
COPY pyproject.toml /home/prowler/
COPY README.md /home/prowler/

# Upgrade pip, setuptools, and wheel, then install project dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r /home/prowler/requirements.txt

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

# Set environment variables for Auth0 (make sure to replace sensitive data with environment secrets in production)


# Switch back to the prowler user
USER prowler

# Entry point: run the Prowler dashboard
ENTRYPOINT ["sh", "-c", "prowler dashboard"]
