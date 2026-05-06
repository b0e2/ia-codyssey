# 도어 해킹 (ZIP 파일 암호 해독)

Python과 다중 프로세싱을 활용하여 ZIP 파일(`emergency_storage_key.zip`)의 
6자리 암호(숫자 및 소문자 알파벳)를 무차별 대입 방식으로 해독하는 스크립트입니다.

## 실행 결과
![실행 화면](./assets/course2:prob1:output.png)


## 주요 구현 로직

* **다중 프로세싱 적용:** `multiprocessing.Pool`을 사용하여 가용 CPU 코어에 작업을 분산시켜 병렬 연산 수행.
* **우선순위 탐색 알고리즘:** 설정 확률이 높은 조합(순수 숫자 등)을 우선 탐색 공간으로 배정하여 평균 탐색 시간 단축.
* **파일 I/O 최적화:** 워커 프로세스 초기화 시 압축 파일을 메모리에 한 번만 캐싱하여 디스크 읽기 병목 제거.

## 실행 방법
```bash
# pyzipper 라이브러리 설치
uv pip install pyzipper

# 해독 스크립트 실행
python door_hacking.py