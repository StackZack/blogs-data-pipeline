#! /bin/sh

set -e

export VAULT_ADDR=http://vault:8200
export SECRET_CONN_PATH=/data/secrets_backend/connections
export SECRET_VAR_PATH=/data/secrets_backend/variables

# Wait for vault
sleep 15

# login with root token at $VAULT_ADDR
vault login root

# create airflow connections
vault kv put -mount=secret connections/DATAWAREHOUSE @$SECRET_CONN_PATH/DATAWAREHOUSE.json
vault kv put -mount=secret connections/INBOUND_SFTP @$SECRET_CONN_PATH/INBOUND_SFTP.json
vault kv put -mount=secret connections/SPARK @$SECRET_CONN_PATH/SPARK.json

# create airflow variables
vault kv put -mount=secret variables/blogs_batch_load_params @$SECRET_VAR_PATH/blogs_batch_load_params.json
