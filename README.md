## Airbyte local setup 
https://docs.airbyte.com/platform/using-airbyte/getting-started/oss-quickstart

## components
* localhost:8000 airbyte
* localhost:8081 airflow
* localhost:3000 metabase
* localhost:9001 minio (create bucket raw-data)
* localhost:9047 dremio
* localhost:19120 nessie

## plugins
dremio-metabase custom plugin installed in the custom metabase image (https://github.com/Baoqi/metabase-dremio-driver/releases)

dremio:31010 (metabase endpoint)

## dependencies
uv add dbt-dremio

## run
docker compose -f docker-compose-pg-source.yml -f docker-compose-datalakehouse.yml -f docker-compose-airflow.yml -f docker-compose-metabase.yml up --build

## postgres-source 
Data producer with some test data

'''
CREATE TABLE public.users (
	id VARCHAR(10) PRIMARY KEY,
	name VARCHAR(20) not null,
	created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO public.users (id, name) VALUES ('U10001', 'Mark');
INSERT INTO public.users (id, name) VALUES ('U10002', 'Phil');
INSERT INTO public.users (id, name) VALUES ('U10003', 'John');

CREATE TABLE public.bookings (
	id SERIAL PRIMARY KEY,
	booking_date DATE NOT NULL,
	service_id INT NOT NULL,
	quantity INT NOT NULL,
	total_amount NUMERIC(10, 2) NOT null,
	user_id VARCHAR references users(id),
	created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO public.bookings (booking_date, service_id, quantity, total_amount, user_id) VALUES ('2023-01-01', 101, 3, 450.00, 'U10001');
INSERT INTO public.bookings (booking_date, service_id, quantity, total_amount, user_id) VALUES ('2023-02-01', 102, 1, 320.00, 'U10001');
INSERT INTO public.bookings (booking_date, service_id, quantity, total_amount, user_id) VALUES ('2023-03-01', 103, 4, 720.00, 'U10002');
'''

## airbyte
Create source, destination and connection
<img width="1899" height="730" alt="image" src="https://github.com/user-attachments/assets/2fdca6b0-5ddb-48b4-a2b1-eaa10cf891b5" />

Sync details
<img width="1891" height="885" alt="image" src="https://github.com/user-attachments/assets/87161e9e-8602-472e-8aaf-d11ff317c92e" />

Processing
<img width="1888" height="462" alt="image" src="https://github.com/user-attachments/assets/1824b1ed-2394-4ad6-a468-26a5a60f34b9" />

## minio
Load to storage
<img width="1892" height="414" alt="image" src="https://github.com/user-attachments/assets/47c87e14-540b-4209-80dc-a557f44bee72" />

## nessie
Table catalog updated
<img width="1155" height="377" alt="image" src="https://github.com/user-attachments/assets/379a963f-09ec-4f8c-b94b-17b851a9ec38" />

## dremio
Configure table catalog and storage
<img width="2187" height="517" alt="image" src="https://github.com/user-attachments/assets/32c40eec-ae42-42b6-9d4e-e27e74860bad" />

## metabase
Query data from the BI layer
<img width="1818" height="690" alt="image" src="https://github.com/user-attachments/assets/cd228618-bf33-4282-b077-eb9899c4967c" />



### Dremio UI config
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
