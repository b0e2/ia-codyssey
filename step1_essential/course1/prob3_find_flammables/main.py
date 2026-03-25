# 문제3 인화 물질을 찾아라
# Python Version: 3.9.6 

# 원본 데이터 파일 (화성기지 입고 물질 목록 CSV 파일)
CSV_FILE_PATH = 'Mars_Base_Inventory_List.csv'
# 필터링 데이터 파일 (인화성 지수 0.7 이상인 물질 목록 CSV 파일)
CSV_DANGER_FILE_PATH = 'Mars_Base_Inventory_danger.csv'
# 이진 데이터 파일 (인화성 순서로 정렬된 배열의 내용을 이진 파일 형태로 저장)
BIN_FILE_PATH = 'Mars_Base_Inventory_List.bin'


def get_absolute_path(filename):
    """스크립트 위치 기준의 절대 경로를 생성하는 유틸리티 함수"""
    return __file__.replace('main.py', filename)


def load_inventory_data(target_path):
    """파일을 읽어 헤더와 데이터 리스트를 분리하여 반환합니다."""
    header = []
    inventory_list = []
    
    # 파일 열기 및 입고 물질 목록 읽기
    with open(target_path, 'r', encoding='utf-8') as file:
        # CSV 파일의 첫 줄은 헤더이므로 별도로 처리하여 리스트로 저장
        header = next(file).strip().split(',')  
        # [수행과제] List 객체로 변환 
        for line in file:
            if line.strip():  # 빈 줄 방지
                inventory_list.append(line.strip().split(','))
                
    return header, inventory_list


def print_inventory(prefix_title, header, data_list):
    """헤더와 데이터를 결합하여 일관된 포맷으로 터미널에 출력합니다."""
    print(f'{prefix_title} {len(data_list)} lines] ---') 
    for item in [header] + data_list:
        print(','.join(item))


def save_inventory_csv(target_path, header, data_list):
    """데이터를 지정된 경로에 CSV 파일로 저장합니다."""
    # [수행과제] 인화성 지수가 0.7 이상인 물질 목록을 별도의 CSV 파일로 저장 (utf-8 인코딩)    
    with open(target_path, 'w', encoding='utf-8') as f:
        f.writelines([','.join(item) + '\n' for item in [header] + data_list])
        
        
def save_inventory_binary(target_path, header, data_list):
    """[보너스 과제] 정렬된 배열의 내용을 이진 파일 형태로 저장합니다."""
    with open(target_path, 'wb') as f:
        for item in [header] + data_list:
            # 문자열로 합친 뒤 utf-8 바이트로 인코딩(encode)하여 저장
            line_data = ','.join(item) + '\n'
            f.write(line_data.encode('utf-8'))


def load_and_print_binary(target_path):
    """[보너스 과제] 저장된 이진 파일의 내용을 다시 읽어 들여서 화면에 출력합니다."""
    print('\n---[인화성 순서로 정렬된 이진 파일] ---')
    with open(target_path, 'rb') as f:
        for line in f:
            # 바이트 데이터를 다시 문자열로 디코딩(decode)하여 출력
            print(line.decode('utf-8').strip())       


def find_flammables(target_path):
    """전체 비즈니스 로직의 흐름을 통제하는 메인 함수"""
    try:
        # 입고 물질 헤더, 목록, 위험 물질 리스트 
        header, inventory_list = load_inventory_data(target_path)
        
        # [수행과제] 입고 물질 목록 전체 출력
        print_inventory('--- [전체 입고 물질 목록 출력:', header, inventory_list)
            
        # [수행과제] 인화성 높은 순 정렬 
        inventory_list.sort(key=lambda x: float(x[-1]), reverse=True)
                
        # 인화성 지수 0.7 이상인 물질 필터링
        inventory_danger_list = [item for item in inventory_list if float(item[-1]) >= 0.7]
                
        # [수행과제] 인화성 지수가 0.7 이상인 물질 출력        
        print_inventory('\n--- [인화성 지수 0.7 이상인 물질 목록', header, inventory_danger_list)
        
        # 스크립트 위치 기준의 절대 경로 생성 
        inventory_danger_list_path = get_absolute_path(CSV_DANGER_FILE_PATH)
        inventory_bin_path = get_absolute_path(BIN_FILE_PATH)
        
        # 파일 저장 호출
        save_inventory_csv(inventory_danger_list_path, header, inventory_danger_list)
        
        # [보너스 과제] 인화성 순서로 정렬된 배열의 내용을 이진 파일 형태로 저장
        save_inventory_binary(inventory_bin_path, header, inventory_list)
        
        # [보너스 과제] 저장된 이진 파일의 내용을 다시 읽어 들여서 화면에 출력
        load_and_print_binary(inventory_bin_path)
        
    except FileNotFoundError:
        print(f'Error: 파일 "{target_path}"을(를) 찾을 수 없습니다.')
    except Exception as e:
        print(f'Error: 예상치 못한 오류가 발생했습니다. {e}') 


if __name__ == '__main__':
    # 실행 환경에 구애받지 않도록 스크립트 위치 기준의 절대 경로 생성 (리뷰어 고려)
    absolute_log_path = get_absolute_path(CSV_FILE_PATH)
    # 인화물질 탐색 함수 호출
    find_flammables(absolute_log_path)