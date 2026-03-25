# 문제3 인화 물질을 찾아라
# Python Version: 3.9.6 

# 화성기지 입고 물질 목록 원본 데이터 
CSV_FILE_PATH = 'Mars_Base_Inventory_List.csv'


def find_flammables(target_path):
    # 입고 물질 목록 리스트 
    inventory_list = []
    header = []
    try:
        # 파일 열기 및 입고 물질 목록 읽기
        with open(target_path, 'r', encoding='utf-8') as file:
            # CSV 파일의 첫 줄은 헤더이므로 별도로 처리하여 리스트로 저장
            header = next(file).strip().split(',')  
            # [수행과제] List 객체로 변환 
            for line in file:
                inventory_list.append(line.strip().split(','))
        
        # [수행과제] 입고 물질 목록 전체 출력
        print(f'--- [전체 입고 물질 목록 출력: {len(inventory_list)} lines] ---') 
        for item in [header] + inventory_list:
            print(','.join(item))
            
        # [수행과제] 인화성 높은 순 정렬 
        inventory_list.sort(key=lambda x: float(x[-1]), reverse=True)
        
        
        
    except FileNotFoundError:
        print(f'Error: 파일 "{target_path}"을(를) 찾을 수 없습니다.')
    except Exception as e:
        print(f'Error: 예상치 못한 오류가 발생했습니다. {e}') 


if __name__ == '__main__':
    # 실행 환경에 구애받지 않도록 스크립트 위치 기준의 절대 경로 생성 (리뷰어 고려)
    absolute_log_path = __file__.replace('main.py', CSV_FILE_PATH)
    # 인화물질 탐색 함수 호출
    find_flammables(absolute_log_path)