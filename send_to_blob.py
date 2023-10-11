from azure.storage.filedatalake import DataLakeFileClient, DataLakeServiceClient
from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient, BlobBlock, BlobType
import uuid, os, io

ACCOUNT_NAME = "omnistoragehierar"
ACCOUNT_KEY = "oCNEzgAm6qTdCqtYVfCxMbIDBTBwVay1O0gkqJbDY0YALjtWJHgWiouUueHyHH/I70C4LmJJAWbJ+AStcWhmfg=="

fs_container = "escalas-mma"
directory_file = "Entrada/Processar/Excel"
file_name_to_upload = ""
local_file_name = os.path.join(os.path.abspath("./"), file_name_to_upload)

CONN_STR = (f"DefaultEndpointsProtocol=https;AccountName={ACCOUNT_NAME};AccountKey={ACCOUNT_KEY};EndpointSuffix=core.windows.net")

def exists(file_client: DataLakeFileClient):
    try:
        file_size = file_client.get_file_properties().size
        if file_size == 0:
            return False
        else:
            return True
    except ResourceNotFoundError:
        return False


def download_file_from_blob(
    connection_string, container_name, file_path
) -> bytes:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(file_path)

    download = blob_client.download_blob()
    downloaded_bytes = download.readall()

    return downloaded_bytes


def upload_large_files_blob(conn_str, fs_container, blob_file_path, upload_data) -> str:
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=conn_str)
    container_client = blob_service_client.get_container_client(fs_container)
    access_blob_client = container_client.get_blob_client(blob_file_path)
    block_list = []
    chunk_size = 4 * 1024 * 1024
    for idx in range(0, len(upload_data), chunk_size):
        read_data = upload_data[idx : idx + chunk_size]
        block_id = str(uuid.uuid4())
        access_blob_client.stage_block(block_id=block_id, data=read_data)
        block_list.append(BlobBlock(block_id=block_id))
    access_blob_client.commit_block_list(block_list=block_list)
    return "Arquivo carregado com sucesso!"


def upload_variable_to_blob(connection_string, container_name, blob_name, data):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    blob_client = container_client.get_blob_client(blob_name)
    if blob_client.exists():
        blob_client.delete_blob()

    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(data, blob_type=BlobType.BlockBlob)


def export_dataframe_to_blob(df, container_name, blob_name):
    bytes_io = io.BytesIO()
    df.to_excel(bytes_io, index=False)
    exported_data = bytes_io.getvalue()
    exported_data_io = io.BytesIO(exported_data)
    upload_variable_to_blob(CONN_STR, container_name, blob_name, exported_data_io.getvalue())

#

