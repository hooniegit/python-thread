# 해당 연도의 date list 생성
def create_date_list(year):
    from datetime import datetime, timedelta

    date_list = []

    start_date = f"{year}-01-01"
    now_date = datetime.strptime(start_date, "%Y-%m-%d")
    date_list.append(start_date)

    while True:
        now_date += timedelta(days = 1)
        now_date_str = now_date.strftime("%Y-%m-%d")
        date_list.append(now_date_str)

        if now_date_str >= f"{year + 1}-01-01":
            break

    return date_list


# 연도별로 반복 작업할 thread 내용
def thread_single(year):
    import time
    print(f"START THREAD : {year} >>>>>>>>>>")

    date_list = create_date_list(year)
    for date in date_list:
        print(f"Hello, World! Today is {date}")
        time.sleep(0.05)

    print(f"FINISH THREAD : {year} <<<<<<<<<<")


# multi-thread
def thread_all():
    from threading import Thread

    threads = []
    years = [2018, 2019, 2020, 2021, 2022]
    for year in years:
        thread = Thread(target=thread_single, args=(year,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


# 스크립트 실행
if __name__ == "__main__":
    thread_all()