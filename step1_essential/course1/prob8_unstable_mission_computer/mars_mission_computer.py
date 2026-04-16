"""문제8 불안정한 미션 컴퓨터 상태 파악."""

import json
import os
import platform
from typing import Any

try:
    import psutil
except ImportError:
    psutil = None


class MissionComputer:
    """미션 컴퓨터의 시스템 정보와 실시간 부하를 확인한다."""

    def __init__(self) -> None:
        self.setting_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "setting.txt",
        )

    def _print_json(self, data: dict[str, Any]) -> None:
        print(json.dumps(data, ensure_ascii=False, indent=4))

    def _read_setting_items(self) -> set[str]:
        # [보너스 과제] setting.txt에 적힌 항목만 출력 대상으로 사용한다.
        if not os.path.exists(self.setting_path):
            return set()

        with open(self.setting_path, "r", encoding="utf-8") as file:
            return {
                line.strip()
                for line in file
                if line.strip() and not line.lstrip().startswith("#")
            }

    def _apply_setting(self, data: dict[str, Any]) -> dict[str, Any]:
        selected_items = self._read_setting_items()
        if not selected_items:
            return data
        return {key: value for key, value in data.items() if key in selected_items}

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

    def get_mission_computer_info(self) -> dict[str, Any]:
        # [수행과제] 미션 컴퓨터의 시스템 정보를 수집해 JSON으로 출력한다.
        try:
            info = {
                "운영체계": platform.system(),
                "운영체계 버전": platform.version(),
                "CPU의 타입": platform.processor() or platform.machine(),
                "CPU의 코어 수": os.cpu_count(),
                "메모리의 크기": self._get_memory_size(),
            }
        except Exception as error:  # pragma: no cover - 시스템 환경 의존
            info = {"error": f"시스템 정보를 가져오는 중 오류가 발생했습니다: {error}"}

        filtered_info = self._apply_setting(info)
        self._print_json(filtered_info)
        return filtered_info

    def get_mission_computer_load(self) -> dict[str, Any]:
        # [수행과제] CPU와 메모리의 실시간 사용량을 JSON으로 출력한다.
        try:
            load = {
                "CPU 실시간 사용량": self._get_cpu_usage(),
                "메모리 실시간 사용량": self._get_memory_usage(),
            }
        except Exception as error:  # pragma: no cover - 시스템 환경 의존
            load = {"error": f"시스템 부하를 가져오는 중 오류가 발생했습니다: {error}"}

        filtered_load = self._apply_setting(load)
        self._print_json(filtered_load)
        return filtered_load


if __name__ == "__main__":
    # [수행과제] MissionComputer 클래스를 runComputer 이름으로 인스턴스화한다.
    runComputer = MissionComputer()
    # [수행과제] 시스템 정보와 실시간 부하 정보를 차례대로 출력한다.
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
