import os
import wave
from datetime import datetime
import pyaudio


RECORDS_DIR = 'records'


class JavisAudioRecorder:

    def __init__(self) -> None:
        self.setup_directory()

    def setup_directory(self) -> None:
        try:
            if not os.path.exists(RECORDS_DIR):
                os.makedirs(RECORDS_DIR)
        except OSError as e:
            print(f'디렉토리 생성 오류: {e}')

    def get_formatted_time(self) -> str:
        return datetime.now().strftime('%Y%m%d-%H%M%S')

    def record_audio(self, duration: int) -> str:
        # [수행과제] 시스템의 마이크를 인식하여 음성을 녹음하고 '년월일-시간분초' 형태의 파일명으로 records 폴더에 저장한다.
        chunk = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 44100
        
        p = pyaudio.PyAudio()
        frames = []

        try:
            print(f'\n{duration}초 동안 녹음을 시작합니다...')
            stream = p.open(
                format=audio_format,
                channels=channels,
                rate=rate,
                input=True,
                frames_per_buffer=chunk
            )

            for _ in range(0, int(rate / chunk * duration)):
                data = stream.read(chunk)
                frames.append(data)

            print('녹음이 완료되었습니다.')

            stream.stop_stream()
            stream.close()
        except Exception as e:
            print(f'마이크 인식 및 녹음 중 오류 발생: {e}')
            p.terminate()
            return ''
        finally:
            p.terminate()

        filename = f'{self.get_formatted_time()}.wav'
        filepath = os.path.join(RECORDS_DIR, filename)

        try:
            wf = wave.open(filepath, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(audio_format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            return filepath
        except IOError as e:
            print(f'파일 저장 중 입출력 오류 발생: {e}')
            return ''

    def show_files_in_date_range(self, start_date: str, end_date: str) -> None:
        # [보너스과제] 특정 범위의 날짜를 입력받아 해당 기간 내에 기록된 녹음 파일 목록을 보여준다.
        print(f'\n--- {start_date} ~ {end_date} 녹음 파일 목록 ---')
        try:
            if not os.path.exists(RECORDS_DIR):
                print('저장된 파일이 존재하지 않습니다.')
                return

            files = os.listdir(RECORDS_DIR)
            if len(files) == 0:
                print('저장된 파일이 존재하지 않습니다.')
                return

            found = False
            for file in files:
                if not file.endswith('.wav'):
                    continue
                
                # 'YYYYMMDD-HHMMSS.wav' 형식에서 'YYYYMMDD' 부분만 추출
                file_date = file.split('-')[0]
                
                if start_date <= file_date <= end_date:
                    print(f'- {file}')
                    found = True
                    
            if not found:
                print('해당 기간에 일치하는 녹음 파일이 없습니다.')
        except OSError as e:
            print(f'파일 목록 읽기 오류: {e}')

    def run(self) -> None:
        
        while True:
            print('\n원하시는 기능을 선택해주세요.')
            print('1. 음성 녹음 (시간 지정)')
            print('2. 날짜 범위로 녹음 파일 검색')
            print('q. 프로그램 종료')
            choice = input('> ').strip()

            if choice.lower() == 'q':
                print('시스템을 종료합니다.')
                break
            
            elif choice == '1':
                print('몇 초 동안 녹음하시겠습니까? (숫자만 입력)')
                sec_input = input('> ').strip()
                
                if sec_input.isdigit() and int(sec_input) > 0:
                    duration = int(sec_input)
                    filepath = self.record_audio(duration)
                    if filepath != '':
                        print(f"\n성공: '{filepath}'에 녹음 파일이 저장되었습니다.")
                else:
                    print('경고: 0보다 큰 올바른 숫자를 입력해주세요.')
            
            elif choice == '2':
                print("검색할 시작 날짜를 입력하세요 (예: 20260501):")
                start = input('> ').strip()
                print("검색할 종료 날짜를 입력하세요 (예: 20260531):")
                end = input('> ').strip()
                
                if len(start) == 8 and len(end) == 8 and start.isdigit() and end.isdigit():
                    self.show_files_in_date_range(start, end)
                else:
                    print('경고: 날짜 형식이 올바르지 않습니다. (8자리 숫자)')
            else:
                print('잘못된 입력입니다. 다시 선택해주세요.')


def main() -> None:
    javis = JavisAudioRecorder()
    javis.run()


if __name__ == '__main__':
    main()