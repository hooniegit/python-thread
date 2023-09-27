# 🔬 Intro
python thread에 대한 이해를 목적으로 python 환경에서 multi-thread 생성 및 활용을 실습합니다.

### need to know
- thread를 위한 target 함수에 args 를 전달할 때, set의 형태로 전달해야 합니다(데이터가 1개인 경우도 포함).

### target
- print 함수를 응용해 multi-thread를 적용하는 간단한 실습을 진행합니다.
- AWS s3 환경에 있는 대량의 데이터들을 다른 디렉토리로 이전하는 실습을 진행합니다.
- 

# thread structure
python thread의 단순 구조에 대해서 설명합니다.

### 반복 실행할 단일 thread 함수
``` python
def thread_single(param):
    print(f"START THREAD : {param} >>>>>>>>>>")

    # 이 곳에 반복작업의 내용이 들어갑니다.

    print(f"FINISH THREAD : {param} <<<<<<<<<<")
```

### 다중 thread를 순차 생성할 함수
``` python
def thread_all(s3_client):
    from threading import Thread

    # 반복 수행 단위
    params_list = [ .. ]

    # 병렬 작업을 위한 thread 리스트
    threads = []
    for param in params_list:
        # args는 set의 형태로 전달해야 합니다.
        thread = Thread(target=thread_single, args=(param, ..))
        threads.append(thread)
        # 각 param에 대하여 단일 thread 시작
        thread.start()
    
    # 각 스레드에 대하여 전체 종료 시까지 대기
    for thread in threads:
        thread.join()
```

# 🪧 notice
1. This repository runs in python3.10
2. `/src/aws_s3` 이하의 모든 스크립트는 AWS s3 접속을 위한 key 정보를 포함하고 있습니다.
해당 레포지토리에서는 AWS와 관련된 내용에 대해서는 다루지 않습니다. 이 점을 참조 부탁드립니다.