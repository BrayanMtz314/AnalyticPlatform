# Analytics Platform

## API layer

## Streamlit layer

## infraestructure layer

you need:

- terraform installed 

- you need an external backend, here we use a S3 bucket, you can use one that you have, make reference using the backend.hcl.example (remove .example)

- use this init command to use your external bucket:
```bash
terraform init -backend-config="backend.hcl"
```

- To use a s3 as backend, be sure about have logged in your terminal using aws cli

- create a rsa_key public and secret, called as:
    - rsa_key.p8
    - rsa_key.pub
- the public key must be set with your snowflake user, you can use the next command:
```sql
ALTER USER your_user SET RSA_PUBLIC_KEY='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...';
```

you can create your credential using openssl in linux:
```bash
# 1. Generate the unencrypted private key (keep this safe!)
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt

# 2. Extract the public key
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```
saved it in the infraestructure folder, be sure about adding them to the .gitignore file!

- remember fill out the .env.example, the terraform.tfvars.example and the terraform.hcl, add those to the .gitignore file!


- run the proyect
```bash
# watch the resources
terraform plan

# set up the resources
terraform apply

#useful if you want to see the resources
terraform state list

# set in the enviroment
source .venv/bin/activate

# run the script
uv run python scripts/init_db.py
```



