# mars_mission_computer.py
# 문제8 불안정한 미션 컴퓨터 상태 파악
# Python Version: 3.9.6

import json
import os
import platform
import threading
import time

try:
    import psutil
except ImportError:
    psutil = None


SENSOR_CONFIG = {
    "mars_base_internal_temperature": {"min": 18.0, "max": 30.0, "decimal": 0},
    "mars_base_external_temperature": {"min": 0.0, "max": 21.0, "decimal": 0},
    "mars_base_internal_humidity": {"min": 50.0, "max": 60.0, "decimal": 0},
    "mars_base_external_illuminance": {"min": 500.0, "max": 715.0, "decimal": 0},
    "mars_base_internal_co2": {"min": 0.02, "max": 0.1, "decimal": 2},
    "mars_base_internal_oxygen": {"min": 4.0, "max": 7.0, "decimal": 0},
}


class DummySensor:
    """센서 데이터 생성 클래스"""

    def __init__(self) -> None:
        self.env_values = {key: 0.0 for key in SENSOR_CONFIG}
        self.seed = int(time.time() * 1000)

    def _get_random(self, min_val: float, max_val: float) -> float:
        self.seed = (1103515245 * self.seed + 12345) % 2147483648
        return min_val + (self.seed / 2147483647) * (max_val - min_val)

    def set_env(self) -> None:
        for key, config in SENSOR_CONFIG.items():
            value = round(
                self._get_random(config["min"], config["max"]),
                config["decimal"],
            )
            self.env_values[key] = int(value) if config["decimal"] == 0 else value

    def get_env(self) -> dict:
        return self.env_values


class MissionComputer:
    """[수행과제] 문제 7 기반으로 시스템 상태 확인 기능을 확장한다."""

    def __init__(self, sensor: DummySensor) -> None:
        self.sensor = sensor
        self.env_values = {}
        self.is_running = False
        self.show_avg = False
        self.setting_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "setting.txt",
        )
        self._reset_history()

    def _reset_history(self) -> None:
        self.history = {key: [] for key in SENSOR_CONFIG}
        self.count = 0

    def _to_json(self, data: dict) -> str:
        return json.dumps(data, ensure_ascii=False, indent=4)

    def _calculate_average(self) -> dict:
        if self.count == 0:
            return {key: 0.0 for key in SENSOR_CONFIG}

        average_data = {}
        for key, values in self.history.items():
            average_data[key] = round(
                sum(values) / self.count,
                SENSOR_CONFIG[key]["decimal"],
            )
        return average_data

    def _read_setting_items(self) -> set:
        # [보너스 과제] setting.txt에 적힌 항목만 출력 대상으로 반영한다.
        if not os.path.exists(self.setting_path):
            return set()

        with open(self.setting_path, "r", encoding="utf-8") as file:
            return {
                line.strip()
                for line in file
                if line.strip() and not line.lstrip().startswith("#")
            }

    def _apply_setting(self, data: dict) -> dict:
        selected_items = self._read_setting_items()
        if not selected_items:
            return data
        return {key: value for key, value in data.items() if key in selected_items}

    def _key_listener(self) -> None:
        while self.is_running:
            try:
                command = input().strip().lower()
                if command == "q":
                    self.is_running = False
                elif command == "e":
                    self.show_avg = True
            except EOFError:
                pass

    def _get_memory_size(self) -> str:
        if psutil is None:
            return "확인 불가"
        total_memory = psutil.virtual_memory().total
        return f"{total_memory / (1024 ** 3):.2f}GB"

    def _get_cpu_usage(self) -> str:
        if psutil is None:
            return "확인 불가"
        return f"{psutil.cpu_percent(interval=1):.1f}%"

    def _get_memory_usage(self) -> str:
        if psutil is None:
            return "확인 불가"
        return f"{psutil.virtual_memory().percent:.1f}%"

    def get_mission_computer_info(self) -> dict:
        # [수행과제] 시스템 정보를 수집해 JSON 형식으로 출력한다.
        try:
            info = {
                "운영체계": platform.system(),
                "운영체계 버전": platform.version(),
                "CPU의 타입": platform.processor() or platform.machine(),
                "CPU의 코어 수": os.cpu_count(),
                "메모리의 크기": self._get_memory_size(),
            }
        except Exception as error:
            info = {"error": f"시스템 정보를 가져오는 중 오류가 발생했습니다: {error}"}

        filtered_info = self._apply_setting(info)
        print(self._to_json(filtered_info))
        return filtered_info

    def get_mission_computer_load(self) -> dict:
        # [수행과제] CPU와 메모리 사용량을 JSON 형식으로 출력한다.
        try:
            load = {
                "CPU 실시간 사용량": self._get_cpu_usage(),
                "메모리 실시간 사용량": self._get_memory_usage(),
            }
        except Exception as error:
            load = {"error": f"시스템 부하를 가져오는 중 오류가 발생했습니다: {error}"}

        filtered_load = self._apply_setting(load)
        print(self._to_json(filtered_load))
        return filtered_load

    def get_sensor_data(self) -> None:
        # [수행과제] 문제 7의 센서 모니터링 기능을 그대로 이어받아 사용한다.
        self.is_running = True
        listener = threading.Thread(target=self._key_listener, daemon=True)
        listener.start()

        while self.is_running:
            self.sensor.set_env()
            self.env_values = self.sensor.get_env()
            print(self._to_json(self.env_values))

            for key, value in self.env_values.items():
                self.history[key].append(value)

            self.count += 1

            if self.show_avg or self.count >= 60:
                print("[Average Data]")
                print(self._to_json(self._calculate_average()))
                if self.count >= 60:
                    self._reset_history()
                self.show_avg = False

            for _ in range(50):
                if not self.is_running:
                    break
                time.sleep(0.1)

        print("System stopped....")


if __name__ == "__main__":
    # [수행과제] DummySensor 객체와 MissionComputer 객체를 생성한다.
    ds = DummySensor()
    runComputer = MissionComputer(ds)
    # [수행과제] 시스템 정보와 실시간 부하 정보를 차례대로 확인한다.
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
