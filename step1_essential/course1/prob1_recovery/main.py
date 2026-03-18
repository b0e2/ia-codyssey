# 문제1 미션컴퓨터를 복구하고 사고 원인을 파악해 보자 / Python Version : 3.9.6 

def analyze_log(file_path):

    try:
        # 파일 열기 및 로그 읽기
        with open(file_path, 'r', encoding='utf-8') as file:
            logs = file.readlines()
            
            # 전체 로그 출력
            for line in logs:
                print(line.strip())
                
    except FileNotFoundError:
        print(f'Error: 로그 파일을 찾을 수 없습니다. 파일 경로를 확인하고 다시 시도해주세요.')
        
    except Exception as e:
        print(f'Error: 예상치 못한 오류가 발생했습니다 -> {e}')
    
        
def main():
    # 1. 설치 확인
    print('Hello Mars!')
    print('--- start ---')

    # 2. 로그 파일 지정 및 경로 설정 / 리뷰어의 환경 상관없이 파일을 찾을 수 있도록 구현 
    log_file = 'mission_computer_main.log'
    log_file_path = __file__.replace('main.py', log_file, 1)
    
    # 3. 로그 분석 함수 호출
    analyze_log(log_file_path)
    print('--- end ---')
        

if __name__ == '__main__':
    main()