# 문제1 미션 컴퓨터를 복구하고 사고 원인을 파악해 보자
# Python Version: 3.9.6 
"""
    로그 분석, 이상 징후 기록 및 기술 보고서 생성을 통합 수행합니다.
    예외 처리를 통해 프로세스 안정성을 확보하고 PEP 8 표준을 준수합니다.
"""
# 설정부 - 파일명
SOURCE_LOG = 'mission_computer_main.log'
ANOMALY_LOG = 'mission_computer_anomalies.log'
ANALYSIS_REPORT = 'log_analysis.md'

# 시스템 장애 또는 미션 리스크를 식별하기 위한 핵심 키워드 리스트
INCIDENT_KEYWORDS = ['error', 'critical', 'fail', 'unstable', 'explosion', 'oxygen']

# 템플릿부 - 보고서 양식
REPORT_TEMPLATE = '''# 미션 컴퓨터 로그 분석 보고서

## 1. 분석 개요
- **분석 대상:** `{target_file}`
- **분석 환경:** Python {py_version}
- **데이터 규모:** {total_count} 줄(lines)
- **탐지된 이상 징후:** {prob_count}건

## 2. 이상 징후 탐지 결과 (Anomaly Detection)
{log_list}

## 3. 종합 결론 (Final Conclusion)
{conclusion}
'''

def get_incident_summary():
    # 결론부 - 분석 결과를 바탕으로 사고 원인에 대한 최종 판단을 기술
    return (
        '- 미션 완료(11:30) 직후 산소 공급 계통의 불안정(unstable) 현상 확인\n'
        '- 연쇄적인 폭발(explosion)로 인한 하드웨어 및 시스템 강제 종료로 최종 판단됨'
    )

def analyze_log(target_path):
    try:
        # 파일 열기 및 로그 읽기 
        with open(target_path, 'r', encoding='utf-8') as file:
            logs = file.readlines()

        # [수행과제] 원본 로그 전체 출력
        print(f'--- [전체 로그 출력: {len(logs)} lines] ---')
        for line in logs:
            print(line.strip())
        
        # [보너스 과제] 원본 로그 시간 역순 출력
        print(f'\n--- [시간 역순 출력: {len(logs)} lines] ---')
        for line in reversed(logs):
            print(line.strip())

        # 제너레이터 표현식을 활용하여 대용량 로그 처리에 유리한 방식으로 이상 징후 필터링
        incident_lines = [l for l in logs if any(k in l.lower() for k in INCIDENT_KEYWORDS)]
        
        '''
        incident_lines = []
        for l in logs:
            found = False
            for k in INCIDENT_KEYWORDS:
                if k in l.lower():
                    found = True
                    break
    
            if found:
                incident_lines.append(l)
        '''
        
        if not incident_lines:
            print('알림: 시스템 이상 징후가 발견되지 않았습니다.')
            return
        
        # 실행 환경에 구애받지 않도록 스크립트 위치 기준의 절대 경로 생성
        incident_path = target_path.replace(SOURCE_LOG, ANOMALY_LOG)
        report_path = target_path.replace(SOURCE_LOG, ANALYSIS_REPORT)

        # [보너스 과제] 이상 징후 데이터 보존: 별도 로그 파일로 추출
        with open(incident_path, 'w', encoding='utf-8') as f:
            f.writelines(incident_lines)

        # [수행과제] 사고원인 분석 및 보고서 작성: 가공된 데이터를 마크다운 규격에 맞게 포맷팅 
        formatted_logs = '\n'.join([f'- `{l.strip()}`' for l in incident_lines])
        
        report = REPORT_TEMPLATE.format(
            target_file = SOURCE_LOG,
            py_version = '3.9.6',
            total_count = len(logs),
            prob_count = len(incident_lines),
            log_list = formatted_logs,
            conclusion = get_incident_summary()
        )

        # 분석 보고서 저장 - utf-8 인코딩
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f'\n이상 징후 데이터 추출 완료: {ANOMALY_LOG}')
        print(f'기술 분석 보고서 업데이트 완료: {ANALYSIS_REPORT}')

    # [수행과제] 예외 발생 시 프로세스 중단을 방지하고 에러 원인을 터미널에 명시
    except FileNotFoundError:
        print(f'오류: 로그 파일 "{SOURCE_LOG}"을(를) 찾을 수 없습니다. 경로를 확인해주세요.')
        
    except PermissionError:
        print(f'오류: 로그 파일 "{SOURCE_LOG}"에 접근 권한이 없습니다. 권한 설정을 확인해주세요.')
    
    except UnicodeDecodeError:
        print(f'오류: 로그 파일 "{SOURCE_LOG}"의 인코딩이 올바르지 않습니다. UTF-8 인코딩을 사용해주세요.')

    except Exception as error:
        print(f'오류: {error}')

def main():
    
    # [수행과제] 설치 확인
    print('Hello Mars')
    print('--- Process Start ---')
    
    # 리뷰어의 실행 경로와 운영체제 상관 없이 경로설정 및 로그 분석 함수 호출
    absolute_log_path = __file__.replace('main.py', SOURCE_LOG)
    analyze_log(absolute_log_path)
    
    print('--- Process Terminated Successfully ---')

if __name__ == '__main__':
    main()