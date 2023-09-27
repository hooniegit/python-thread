def get_s3_client():
    from boto3 import client
    from configparser import ConfigParser

    config = ConfigParser()
    config.read("config/config.ini")

    access = config.get("AWS", "S3_ACCESS")
    secret = config.get("AWS", "S3_SECRET")

    s3_client = client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    return s3_client


def merge_files(s3_client, year, month, loc_code):
    BUCKET_NAME = 'sms-warehouse'
    SOURCE_PREFIX = f'kobis/{year}/boxOffice_{month}/loc_code={loc_code}'
    DEST_PREFIX = f'merged_kobis/loc_code={loc_code}'
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=SOURCE_PREFIX)
    
    for content in response.get('Contents', []):
        source_key = content['Key']
        dest_key = source_key.replace(SOURCE_PREFIX, DEST_PREFIX, 1)
        s3_client.copy_object(CopySource={'Bucket': BUCKET_NAME, 'Key': source_key}, Bucket=BUCKET_NAME, Key=dest_key)
        print(f'Merged: {source_key} -> {dest_key}')


def thread_single(s3_client, loc_code):
    year_list = ['2018', '2019', '2020', '2021', '2022', '2023']
    month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    print(f"start thread : {loc_code} >>>>>>>>>> ")
    for year in year_list:
        for month in month_list:
            try : merge_files(s3_client, year, month, loc_code)
            except : pass
    print(f"finish thread : {loc_code} <<<<<<<<<< ")


# 총 17개의 스레드 생성
def thread_all(s3_client):
    from threading import Thread

    loc_list = ["0105001", "0105002", "0105003", "0105004", "0105005", "0105006", "0105007", "010508",
                "0105009", "0105010", "0105011", "0105012", "0105013", "0105014", "0105015", "0105016", "0105017"]

    threads = []
    for loc_code in loc_list:
        thread = Thread(target=thread_single, args=(s3_client, loc_code))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    s3_client = get_s3_client("/Users/kimdohoon/git/config/config.ini")
    thread_all(s3_client)