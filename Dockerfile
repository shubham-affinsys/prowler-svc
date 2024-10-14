FROM python:3.12
LABEL maintainer="https://github.com/prowler-cloud/prowler"
RUN apt-get update && apt-get install -y curl git
RUN mkdir -p /home/prowler && \
    echo 'prowler:x:1000:1000:prowler:/home/prowler:' > /etc/passwd && \
    echo 'prowler:x:1000:' > /etc/group && \
    chown -R prowler:prowler /home/prowler
WORKDIR /home/prowler
COPY myauth/  /home/prowler/
COPY myauth/  /home/prowler/myauth/
COPY prowler/  /home/prowler/prowler/
COPY dashboard/ /home/prowler/dashboard/
COPY pyproject.toml /home/prowler
COPY README.md /home/prowler
 
 
 
ENV HOME='/home/prowler'
ENV PATH="$HOME/.local/bin:$PATH"
ENV PYTHONPATH=/home/prowler:$PYTHONPATH
ENV AUTH0_CLIENT_ID=dAH2Ygr0Lk7m1LMJP6XxTI2HDnPpChud
ENV AUTH0_CLIENT_SECRET=9DKDv0hObCbiLiFAajFqi2ciraC2pdg2M6MsUaupdsywXN4Popn3iVzu7MZo1grC
ENV AUTH0_DOMAIN=dev-bc7mwy7zlu55zrov.us.auth0.com
ENV APP_SECRET_KEY=my_secret
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir .
RUN pip uninstall dash-html-components -y && \
    pip uninstall dash-core-components -y
RUN rm -rf /home/prowler/prowler /home/prowler/pyproject.toml /home/prowler/README.md /home/prowler/build /home/prowler/prowler.egg-info
ENTRYPOINT ["prowler"]
