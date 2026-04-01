# DummySensor.py
# 문제6 미션 컴퓨터 리턴즈 
# Python Version: 3.9.6

import random 
import datetime 

# 각 센서별 생성 범위(min, max), 소수점 표기 자리수(decimal), 출력 단위(unit)를 정의합니다.
SENSOR_CONFIG: dict = {
    'mars_base_internal_temperature': {'min': 18.0, 'max': 30.0, 'decimal': 0, 'unit': '°C'},
    'mars_base_external_temperature': {'min': 0.0, 'max': 21.0, 'decimal': 0, 'unit': '°C'},
    'mars_base_internal_humidity': {'min': 50.0, 'max': 60.0, 'decimal': 0, 'unit': '%'},
    'mars_base_external_illuminance': {'min': 500.0, 'max': 715.0, 'decimal': 0, 'unit': 'W/m²'},
    'mars_base_internal_co2': {'min': 0.02, 'max': 0.1, 'decimal': 2, 'unit': '%'},
    'mars_base_internal_oxygen': {'min': 4.0, 'max': 7.0, 'decimal': 0, 'unit': '%'}
}

class FileLogger:
    """센서 측정 데이터를 로컬 파일에 기록하는 파일 입출력 전담 클래스입니다."""
    
    def save_sensor_data(self, data: dict) -> None:
        """전달받은 측정 데이터를 현재 시간과 함께 로그 파일에 추가(Append)합니다. """
        now: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        sensor_values: list = [f"[{now}] {key}: {value}{SENSOR_CONFIG[key]['unit']}" for key, value in data.items()]
        log_message: str = '\n'.join(sensor_values) + '\n'
        
        # 현재 스크립트 파일과 동일한 경로에 로그 파일을 생성하거나 덧붙입니다.
        absolute_log_path: str = __file__.replace('mars_mission_computer.py', 'sensor_record.log')
        
        try:
            with open(absolute_log_path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_message)
        except IOError as e:
            print(f'Error: log 파일 저장 실패 -> {e}')
        except Exception as e:
            print(f'Error: log 파일 기록 중 오류 -> {e}')


class DummySensor:
    """[수행과제] 더미 센서에 해당하는 클래스입니다."""
    
    def __init__(self) -> None:
        """DummySensor 객체를(env_values) 초기화하고, 센서 데이터를 SENSOR_CONFIG를 기반으로 0으로 기본 설정합니다."""
        self.env_values: dict = {key: 0.0 for key in SENSOR_CONFIG}
        self.logger: FileLogger = FileLogger()
    
    def set_env(self) -> None:
        """SENSOR_CONFIG에 정의된 각 센서의 범위와 소수점 규칙에 따라 무작위 데이터를 생성하여 env_values를 갱신합니다."""
        for key, config in SENSOR_CONFIG.items():
            min_val: float = config['min']
            max_val: float = config['max']
            decimals: int = config['decimal']
            
            val: float = round(random.uniform(min_val, max_val), decimals)
            
            # 소수점 표기가 불필요한 데이터는 명시적으로 정수형(int)으로 변환합니다.
            self.env_values[key] = int(val) if decimals == 0 else val
    
    def get_env(self) -> dict:
        """측정 데이터를 sensor_record.log에 기록한 후 env_values를 반환합니다."""
        self.logger.save_sensor_data(self.env_values)
        return self.env_values
        

if __name__ == '__main__':
    
    # [수행과제] 센서 인스턴스(ds) 생성 및 랜덤 데이터 생성 
    ds = DummySensor()
    ds.set_env()
    
    # [수행 + 보너스과제] 측정된 데이터 획득 및 로그 기록 수행
    current_data: dict = ds.get_env()
    
    # [수행과제] 콘솔 결과 출력
    print(f'--- 센서 측정 결과 {len(current_data)}lines. ---')
    for key, value in current_data.items():
        unit: str = SENSOR_CONFIG[key]['unit']
        print(f'{key}: {value}{unit}')