## Airbyte local setup 
https://docs.airbyte.com/platform/using-airbyte/getting-started/oss-quickstart

## components
* localhost:8000 airbyte
* localhost:8081 airflow
* localhost:3000 metabase
* localhost:9001 minio
* localhost:9047 dremio
* localhost:19120 nessie

## plugins
dremio-metabase custom plugin installed in the custom metabase image (https://github.com/Baoqi/metabase-dremio-driver/releases)

dremio:31010 (metabase endpoint)

## dependencies
uv add dbt-dremio

## run
docker compose -f docker-compose-pg-source.yml -f docker-compose-datalakehouse.yml -f docker-compose-airflow.yml -f docker-compose-metabase.yml up --build


Dremio UI config
<Signin form>
create admin profile in login form
sources > add sources > Nessie
<General>
Name: nessie
Nessie Endpoint URL: http://nessie:19120/api/v2
Nessie Auth Type: none
<Storage> 
AWS Root Path: warehouse
Auth Type: AWS Access Key
AWS Access Key: admin
AWS Access Secret: password
IAM Role to Assume:
Connection Properties:
* fs.s3a.endpoint: minio:9000
* fs.s3a.path.style.access: true 
* fs.s3a.endpoint.region: eu-central-1 (Used by the Hadoop S3A filesystem driver)
* dremio.s3.compat: true (Compatibility mode for an S3 compatible storage)
* dremio.s3.region: eu-central-1 (Explicitly sets the region for Dremio S3 client)
- [ ] Uncheck "encrypt connection"