import csv
import importlib.util
import os
import wave
from datetime import datetime

import speech_recognition as sr


RECORDS_DIR = 'records'
OUTPUTS_DIR = 'outputs'
LANGUAGE = 'ko-KR'
PREVIOUS_PROJECT_DIR_NAME = 'prob7_need_jarvis'
RECORDER_FILE_NAME = 'javis_recorder.py'
RECORDER_MODULE_NAME = 'javis_recorder'


class Javis:

    def __init__(self) -> None:
        self.recorder = self.load_recorder_class()()
        self.setup_directory()

    def setup_directory(self) -> None:
        try:
            os.makedirs(OUTPUTS_DIR, exist_ok=True)
        except OSError as error:
            print(f'디렉토리 생성 오류: {error}')

    def load_recorder_class(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        course2_dir = os.path.dirname(base_dir)
        recorder_path = os.path.join(
            course2_dir,
            PREVIOUS_PROJECT_DIR_NAME,
            RECORDER_FILE_NAME,
        )

        spec = importlib.util.spec_from_file_location(
            RECORDER_MODULE_NAME,
            recorder_path,
        )

        if spec is None or spec.loader is None:
            raise ImportError(f'모듈 정보를 불러올 수 없습니다: {recorder_path}')

        recorder_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(recorder_module)

        return recorder_module.JavisAudioRecorder

    def get_files_by_extension(
        self,
        directory: str,
        extension: str,
    ) -> list[str]:
        try:
            if not os.path.exists(directory):
                return []

            return sorted(
                file_name
                for file_name in os.listdir(directory)
                if file_name.endswith(extension)
            )
        except OSError as error:
            print(f'파일 목록 읽기 오류: {error}')
            return []

    def get_record_files(self) -> list[str]:
        return self.get_files_by_extension(RECORDS_DIR, '.wav')

    def get_csv_files(self) -> list[str]:
        return self.get_files_by_extension(OUTPUTS_DIR, '.csv')

    def select_record_file(self) -> str:
        record_files = self.get_record_files()

        if not record_files:
            print('records 폴더에 녹음 파일이 없습니다.')
            return ''

        print('\n--- 녹음 파일 목록 ---')

        for index, file_name in enumerate(record_files, start=1):
            print(f'{index}. {file_name}')

        selected_input = input('STT 변환할 녹음 파일 번호를 선택하세요.\n> ').strip()

        if not selected_input.isdigit():
            print('경고: 숫자를 입력해주세요.')
            return ''

        selected_index = int(selected_input)

        if not 1 <= selected_index <= len(record_files):
            print('경고: 목록에 있는 번호를 입력해주세요.')
            return ''

        return record_files[selected_index - 1]

    def format_seconds(self, seconds: float) -> str:
        total_milliseconds = int(seconds * 1000)
        milliseconds = total_milliseconds % 1000
        total_seconds = total_milliseconds // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return f'{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}'

    def get_audio_duration(self, audio_path: str) -> str:
        try:
            with wave.open(audio_path, 'rb') as wave_file:
                frame_count = wave_file.getnframes()
                frame_rate = wave_file.getframerate()

                return self.format_seconds(frame_count / frame_rate)
        except wave.Error as error:
            print(f'음성 파일 길이 확인 오류: {error}')
            return ''

    def convert_audio_to_text(self, audio_path: str) -> str:
        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        return recognizer.recognize_google(audio_data, language=LANGUAGE)

    def save_text_to_csv(
        self,
        csv_path: str,
        audio_file: str,
        audio_path: str,
        transcript: str,
    ) -> None:
        fieldnames = [
            'audio_file',
            'segment_start',
            'segment_end',
            'transcript',
            'language',
            'created_at',
        ]

        row = {
            'audio_file': audio_file,
            'segment_start': '00:00:00.000',
            'segment_end': self.get_audio_duration(audio_path),
            'transcript': transcript,
            'language': LANGUAGE,
            'created_at': datetime.now().isoformat(timespec='seconds'),
        }

        with open(csv_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(row)

    # [수행과제] 문제 7에서 녹음된 음성 파일 목록을 불러와 선택한 파일의 텍스트를 추출하고 outputs 폴더에 CSV로 저장한다.
    def convert_record_to_csv(self) -> None:
        file_name = self.select_record_file()

        if file_name == '':
            return

        audio_path = os.path.join(RECORDS_DIR, file_name)
        csv_name = f'{os.path.splitext(file_name)[0]}.csv'
        csv_path = os.path.join(OUTPUTS_DIR, csv_name)

        try:
            transcript = self.convert_audio_to_text(audio_path)
        except sr.UnknownValueError:
            transcript = '음성을 인식하지 못했습니다.'
        except sr.RequestError as error:
            transcript = f'STT 요청 중 오류가 발생했습니다: {error}'

        self.save_text_to_csv(csv_path, file_name, audio_path, transcript)
        print(f'{file_name} -> {csv_path}')

    def search_text_in_csv(self, keyword: str) -> None:
        csv_files = self.get_csv_files()

        if not csv_files:
            print('검색할 CSV 파일이 없습니다.')
            return

        found = False

        for file_name in csv_files:
            csv_path = os.path.join(OUTPUTS_DIR, file_name)

            try:
                with open(
                    csv_path,
                    'r',
                    encoding='utf-8-sig',
                    newline='',
                ) as csv_file:
                    reader = csv.DictReader(csv_file)

                    for row in reader:
                        segment_start = row.get('segment_start', '')
                        segment_end = row.get('segment_end', '')
                        transcript = row.get('transcript', '')

                        if keyword in transcript:
                            print(
                                f'[{file_name}] '
                                f'{segment_start} ~ {segment_end}: '
                                f'{transcript}'
                            )
                            found = True
            except OSError as error:
                print(f'CSV 파일 읽기 오류: {error}')

        if not found:
            print('검색 결과가 없습니다.')

    # [보너스과제] 특정 키워드를 입력하면 저장된 CSV 파일 안에서 내용을 찾아 출력한다.
    def search_csv_by_keyword(self) -> None:
        keyword = input('검색할 키워드를 입력하세요: ').strip()

        if keyword == '':
            print('검색어가 입력되지 않았습니다.')
            return

        self.search_text_in_csv(keyword)

    def record_audio(self) -> None:
        second_input = input('몇 초 동안 녹음하시겠습니까?\n> ').strip()

        if not second_input.isdigit() or int(second_input) <= 0:
            print('경고: 0보다 큰 올바른 숫자를 입력해주세요.')
            return

        file_path = self.recorder.record_audio(int(second_input))

        if file_path != '':
            print(f'\n성공: {file_path}에 녹음 파일이 저장되었습니다.')

    def is_valid_date(self, date_text: str) -> bool:
        return len(date_text) == 8 and date_text.isdigit()

    def search_record_by_date(self) -> None:
        start_date = input('검색할 시작 날짜를 입력하세요. 예: 20260501\n> ').strip()
        end_date = input('검색할 종료 날짜를 입력하세요. 예: 20260531\n> ').strip()

        if self.is_valid_date(start_date) and self.is_valid_date(end_date):
            self.recorder.show_files_in_date_range(start_date, end_date)
            return

        print('경고: 날짜 형식이 올바르지 않습니다.')

    def run(self) -> None:
        menu_actions = {
            '1': self.record_audio,
            '2': self.search_record_by_date,
            '3': self.convert_record_to_csv,
            '4': self.search_csv_by_keyword,
        }

        while True:
            print('\n기능을 선택해주세요.')
            print('1. 음성 녹음')
            print('2. 날짜 범위로 녹음 파일 검색')
            print('3. 녹음 파일 STT 변환 후 CSV 저장')
            print('4. CSV 파일 키워드 검색')
            print('q. 프로그램 종료')

            choice = input('> ').strip().lower()

            if choice == 'q':
                print('시스템을 종료합니다.')
                break

            action = menu_actions.get(choice)

            if action is None:
                print('잘못된 입력입니다. 다시 선택해주세요.')
                continue

            action()


def main() -> None:
    javis = Javis()
    javis.run()


if __name__ == '__main__':
    main()