import os
import time
import pyzipper
import itertools
import multiprocessing as mp

def init_worker(zip_path, target_file, shared_dict):
    global zf, target, state
    zf = pyzipper.AESZipFile(zip_path, 'r')
    target = target_file
    state = shared_dict

def check_password(pwd_str):
    # 다른 워커에서 이미 비밀번호를 찾았다면 즉시 작업 종료
    if state['found']:
        return None
        
    try:
        with zf.open(target, pwd=pwd_str.encode('utf-8')):
            pass
        
        state['found'] = True
        return pwd_str
    except (RuntimeError, pyzipper.zipfile.BadZipFile):
        return None
    except Exception:
        return None

# [수행과제] 다중 프로세싱(Multiprocessing)을 통해 zip 파일의 암호를 해독
def unlock_zip() -> dict:
    zip_file_path = 'emergency_storage_key.zip'
    output_file_path = 'password.txt'
    
    start_time = time.time()
    start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    print('계정 출력 시작 시간:', start_time_str)
    
    try:
        with pyzipper.AESZipFile(zip_file_path, 'r') as zf_test:
            target_filename = zf_test.namelist()[0]
    except Exception:
        print('오류: 압축 파일을 열 수 없습니다.')
        return {'status': 'error', 'password': ''}
        
    manager = mp.Manager()
    shared_state = manager.dict({'found': False})
    
    # [보너스과제] 지능형 탐색(Tiered Search) 알고리즘 적용
    # 1단계: 유력 키워드 및 순수 숫자 6자리 
    common_words = ['python', 'hacker', 'system', 'codyse', 'secret', 'escape', '123456', '000000']
    num_gen = (''.join(p) for p in itertools.product('0123456789', repeat=6))
    
    # 2단계: 순수 영문자 6자리 
    alpha_gen = (''.join(p) for p in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=6))
    
    # 3단계: 전체 조합 
    all_chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    all_gen = (''.join(p) for p in itertools.product(all_chars, repeat=6))
    
    search_space = itertools.chain(common_words, num_gen, alpha_gen, all_gen)
    
    found_pwd = None
    count = 0
    
    num_cores = os.cpu_count() or 4
    with mp.Pool(processes=num_cores, initializer=init_worker, initargs=(zip_file_path, target_filename, shared_state)) as pool:
        try:
            for result in pool.imap_unordered(check_password, search_space, chunksize=10000):
                count += 1
                
                if count % 100000 == 0:
                    elapsed = time.time() - start_time
                    print('\r진행 시간: {:.2f}초 | {}개 탐색 완료...'.format(elapsed, count), end='', flush=True)
                    
                if result:
                    found_pwd = result
                    pool.terminate()  # 정답을 찾으면 남은 작업 즉시 강제 취소
                    break
        except KeyboardInterrupt:
            pool.terminate()
            print('\n사용자에 의해 탐색이 중단되었습니다.')
    
    end_time = time.time()
    
    print('\n\n[해독 결과]')
    print('총 탐색 횟수:', count, '회')
    print('최종 진행 시간:', round(end_time - start_time, 2), '초')
    
    if found_pwd:
        print('비밀번호를 찾았습니다:', found_pwd)
        try:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(found_pwd)
        except Exception:
            pass
        return {'status': 'success', 'password': found_pwd}
    else:
        print('비밀번호를 찾지 못했습니다.')
        return {'status': 'fail', 'password': ''}

if __name__ == '__main__':
    unlock_zip()