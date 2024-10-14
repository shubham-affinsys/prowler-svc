#/bin/bash 
CRED=$(aws sts assume-role --role-arn arn:aws:iam::120462592044:role/prowler_role_wp --role-session-name "Prowlersession" --duration-seconds 900);\
export AWS_ACCESS_KEY_ID=$(echo $CRED | jq -r '.Credentials''.AccessKeyId');\
export AWS_SECRET_ACCESS_KEY=$(echo $CRED | jq -r '.Credentials''.SecretAccessKey');\
export AWS_SESSION_TOKEN=$(echo $CRED | jq -r '.Credentials''.SessionToken'); 
sudo docker run -it --rm -v /home/shubham/work/test-svc/prowler:/home/prowler/output \
--name prowler \
--env AWS_ACCESS_KEY_ID \
--env AWS_SECRET_ACCESS_KEY \
--env AWS_SESSION_TOKEN \
prowler:v2  \
--compliance aws_account_security_onboarding_aws \
aws_foundational_security_best_practices_aws \
aws_foundational_technical_review_aws \
aws_well_architected_framework_reliability_pillar_aws \
aws_well_architected_framework_security_pillar_aws \
cis_3.0_aws \
cisa_aws \
hipaa_aws \
iso27001_2013_aws \
mitre_attack_aws \
pci_3.2.1_aws \
rbi_cyber_security_framework_aws \
soc2_aws
echo "Setting up Dashboard"
sudo docker run -v /home/shubham/work/test-svc/prowler:/home/prowler/output --env HOST=0.0.0.0 --publish 127.0.0.1:11666:11666 prowler:v2 dashboard