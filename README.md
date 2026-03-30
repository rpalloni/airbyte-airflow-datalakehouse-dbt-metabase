## Airbyte local setup 
https://docs.airbyte.com/platform/using-airbyte/getting-started/oss-quickstart

## components
Docker exposes the following ports to the host, so components UI are available at:
* localhost:8000 airbyte
* localhost:8081 airflow
* localhost:3000 metabase
* localhost:9001 minio *(create bucket: raw-data)*
* localhost:9047 dremio
* localhost:19120 nessie

## plugins
dremio-metabase custom plugin installed in the custom metabase image \ (https://github.com/Baoqi/metabase-dremio-driver/releases)

dremio:31010 (metabase endpoint)

<img width="701" height="1043" alt="image" src="https://github.com/user-attachments/assets/628db25e-8212-4580-9b7b-ad0997373277" />


## dependencies
`uv add dbt-dremio`

## run
```
docker compose \
-f docker/docker-compose-pg-source.yml \
-f docker/docker-compose-datalakehouse.yml \
-f docker/docker-compose-airflow.yml \
-f docker/docker-compose-metabase.yml \
-f docker/docker-compose-transformer.yml \
up --build
```
local dbt run: `uv run dbt run`


## postgres-source 
Data producer with some test data

```
CREATE TABLE public.users (
	id VARCHAR(10) PRIMARY KEY,
	name VARCHAR(20) not null,
	created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO public.users (id, name) VALUES ('U10001', 'Mark');
INSERT INTO public.users (id, name) VALUES ('U10002', 'Phil');
INSERT INTO public.users (id, name) VALUES ('M10003', 'John');

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
```

## airbyte
Create source, destination and connection
<img width="1899" height="730" alt="image" src="https://github.com/user-attachments/assets/2fdca6b0-5ddb-48b4-a2b1-eaa10cf891b5" />

Sync details
<img width="1891" height="885" alt="image" src="https://github.com/user-attachments/assets/87161e9e-8602-472e-8aaf-d11ff317c92e" />

Processing
<img width="1888" height="462" alt="image" src="https://github.com/user-attachments/assets/1824b1ed-2394-4ad6-a468-26a5a60f34b9" />

## minio
Load to storage and save as iceberg tables
<img width="1892" height="414" alt="image" src="https://github.com/user-attachments/assets/47c87e14-540b-4209-80dc-a557f44bee72" />

## nessie
Table catalog updated
<img width="1155" height="377" alt="image" src="https://github.com/user-attachments/assets/379a963f-09ec-4f8c-b94b-17b851a9ec38" />

## dremio
Configure table catalog and iceberg tables
<img width="2187" height="517" alt="image" src="https://github.com/user-attachments/assets/32c40eec-ae42-42b6-9d4e-e27e74860bad" />

## metabase
Query data from the BI layer
<img width="1818" height="690" alt="image" src="https://github.com/user-attachments/assets/cd228618-bf33-4282-b077-eb9899c4967c" />

## dbt
Transformations on source data using Dremio query engine, tracked in Nessie and stored in Minio
<img width="1195" height="623" alt="image" src="https://github.com/user-attachments/assets/8e326334-0a9b-49e1-add7-6d47b1b6a55f" />

<img width="1802" height="396" alt="image" src="https://github.com/user-attachments/assets/77fbfe67-f00e-46bb-a875-07019a2c6b1d" />

<img width="1565" height="346" alt="image" src="https://github.com/user-attachments/assets/54949898-2c1e-486d-85c4-a4ec40f01416" />

## airbyte 
DAG orchestrating the dbt transformation and updated data
<img width="1879" height="688" alt="image" src="https://github.com/user-attachments/assets/575b94b4-f7f1-4767-b702-a17e504d6c9c" />

<img width="1353" height="711" alt="image" src="https://github.com/user-attachments/assets/14e0ca08-69b9-4565-aee0-c092b1766691" />


###################################################################################################################################################################################################################################################

### Dremio UI config
```
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
```

### dbt config
https://docs.getdbt.com/docs/local/connect-data-platform/dremio-setup
```
uv add dbt-dremio
dbt init transformer (a dremio account is needed for the setup)
```

_Which database would you like to use?_
```
[1] dremio
[2] software_with_username_password
software_host: 127.0.0.1
port [9047]: 9047
user (username): admin
password (password): password1
```
_Desired storage configuration method option:_
```
[2] sources_and_spaces
```

_profiles.yml_ dbt-dremio parameters define exactly where dbt will create tables and views and where underlying data are stored. \
Because Dremio separates logical metadata (Spaces) from the physical storage (Sources), these settings act as a map for dbt output:
* `dremio_space`: this is the top level space in Dremio where dbt will create the virtual datasets.
* `dremio_space_folder`: (optional) this allows to organize models into a specific folder within the space (`dremio_space/dremio_space_folder/model_xyz`)
* `object_storage_source`: name of the physical source already configured in the Dremio instance
* `object_storage_path`: directory path within the storage where the data files will live (avoid writing everything in root repo)

WARNING: if only using `view` materializations, dbt relies on the Space settings. If models are `materialized='table'` the `object_storage_source` settings become mandatory because Dremio needs to know where to physically write the tables.

### dbt config with catalog
When using a catalog connected to storage instead of Dremio spaces, the logic for the parameters slightly differs: catalog acts as both the logical AND the physical organisation of the tables.

profiles dremio params config **with catalog**:
```
dremio_space: nessie              ---> in a catalog-first workflow, you want the views/tables to live in the same catalog as the source tables
dremio_space_folder: transformer  ---> dbt will create this namespace in the source to host transformations views/tables
object_storage_source: nessie     ---> dbt will use catalog (backed by storage) to manage the transformations physical iceberg tables
object_storage_path: transformer  ---> defines the namespace where the physical iceberg tables will be registered (usually matches dremio_space_folder)
```

