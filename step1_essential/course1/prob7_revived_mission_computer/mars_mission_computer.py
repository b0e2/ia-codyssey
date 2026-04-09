# mars_mission_computer.py
# 문제7 살아난 미션 컴퓨터
# Python Version: 3.9.6

import time
import threading

# 센서명 : {각 센서별 생성 범위(min, max), 소수점 표기 자리수(decimal), 출력 단위(unit)를 정의합니다.}
SENSOR_CONFIG: dict = {
    'mars_base_internal_temperature': {'min': 18.0, 'max': 30.0, 'decimal': 0},
    'mars_base_external_temperature': {'min': 0.0, 'max': 21.0, 'decimal': 0},
    'mars_base_internal_humidity': {'min': 50.0, 'max': 60.0, 'decimal': 0},
    'mars_base_external_illuminance': {'min': 500.0, 'max': 715.0, 'decimal': 0},
    'mars_base_internal_co2': {'min': 0.02, 'max': 0.1, 'decimal': 2},
    'mars_base_internal_oxygen': {'min': 4.0, 'max': 7.0, 'decimal': 0}
}

class DummySensor:
    '''센서 데이터 생성 클래스'''
    def __init__(self) -> None:
        self.env_values: dict = {key: 0.0 for key in SENSOR_CONFIG}
        self.seed: int = int(time.time() * 1000)

    def _get_random(self, min_val: float, max_val: float) -> float:
        self.seed = (1103515245 * self.seed + 12345) % 2147483648
        return min_val + (self.seed / 2147483647) * (max_val - min_val)

    def set_env(self) -> None:
        for key, config in SENSOR_CONFIG.items():
            val: float = round(self._get_random(config['min'], config['max']), config['decimal'])
            self.env_values[key] = int(val) if config['decimal'] == 0 else val

    def get_env(self) -> dict:
        return self.env_values

class MissionComputer:
    '''[수행과제] 미션 컴퓨터에 해당하는 클래스'''
    def __init__(self, sensor: DummySensor) -> None:
        self.sensor: DummySensor = sensor
        self.env_values: dict = {}
        self.is_running: bool = False
        self.show_avg: bool = False
        self._reset_history()

    # 평균 측정 데이터 초기화 
    def _reset_history(self) -> None:
        self.history: dict = {key: [] for key in SENSOR_CONFIG}
        self.count: int = 0

    # json format return 
    def _to_json(self, data: dict) -> str:
        '''[수행과제] '''
        lines: list = ['{']
        lines.extend([f'    "{k}": {v},' for k, v in data.items()])
        if len(lines) > 1:
            lines[-1] = lines[-1].rstrip(',')
        lines.append('}')
        return "\n".join(lines)

    # 평균 값 함수
    def _calculate_average(self) -> dict:
        if self.count == 0:
            return {key: 0.0 for key in SENSOR_CONFIG}
        return {
            key: round(sum(self.history[key]) / self.count, SENSOR_CONFIG[key]['decimal'])
            for key in SENSOR_CONFIG
        }

    # 사용자 입력을 기다리는 백그라운드 스레드
    def _key_listener(self) -> None:
        '''[보너스 과제] 특정 키 입력시 출력 중단 및 메시지 출력'''
        while self.is_running:
            try:
                cmd: str = input().strip().lower()
                if cmd == 'q':
                    self.is_running = False
                elif cmd == 'e':
                    self.show_avg = True
            except EOFError:
                pass

    def get_sensor_data(self) -> None:
        '''[수행과제] 센서 데이터 가져온 뒤 env_values 담고 json 형태로 5초 마다 출력'''
        self.is_running = True
        
        # 키 입력을 감지하는 스레드 실행
        listener: threading.Thread = threading.Thread(target=self._key_listener, daemon=True)
        listener.start()

        while self.is_running:
            self.sensor.set_env()
            # [수행과제] env_values 구현
            self.env_values = self.sensor.get_env()
            
            print(self._to_json(self.env_values))
            
            for key, val in self.env_values.items():
                self.history[key].append(val)
            
            self.count += 1
            
            # 5분에 한번씩 각 환경값에 대한 5분 평균 값 출력 (5초 * 60회 = 300초 = 5분)
            if self.show_avg or self.count >= 60:
                print('\n[Average Data]')
                print(self._to_json(self._calculate_average()))
                if self.count >= 60:
                    self._reset_history()
                self.show_avg = False
                
            for _ in range(50):
                if not self.is_running: 
                    break
                time.sleep(0.1)
                
        print('\nSystem stopped....')

if __name__ == '__main__':
    # [수행과제] DummySensor() - ds 객체 인스터스화 
    ds = DummySensor()
    # [수행과제] MissionComputer() - RunComputer 객체 인스턴스화 
    RunComputer = MissionComputer(ds)
    # [수행과제] get_sensor_data() 메소드를 호출해서 지속적으로 환경에 대한 값을 출력
    RunComputer.get_sensor_data()