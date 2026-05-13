PASSWD_PATH = '../prob1_password_xxxxxx/password.txt'
RESULT_PATH = 'result.txt'

KEYWORD_DICTIONARY = [
    'the',
    'password',
    'mars',
    'emergency',
    'oxygen',
    'science',
    'computer',
    'mission'
]


# [수행과제] pass.txt 파일을 읽어온다.
def read_password_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print('password.txt 파일을 찾을 수 없습니다.')
    except OSError:
        print('password.txt 파일을 읽는 중 오류가 발생했습니다.')

    return ''


# [보너스과제] 사전에 있는 단어가 해독 결과에 있는지 확인한다.
def has_keyword(decoded_text: str, keyword_dictionary: list) -> bool:
    lower_text = decoded_text.lower()

    for keyword in keyword_dictionary:
        if keyword.lower() in lower_text:
            return True

    return False


# [수행과제] 카이사르 암호를 해독하는 함수를 만든다.
def caesar_cipher_decode(target_text: str) -> dict:
    decoded_dict = {}

    for shift in range(26):
        decoded_text = ''

        for char in target_text:
            if 'a' <= char <= 'z':
                decoded_text += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                decoded_text += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decoded_text += char

        decoded_dict[shift] = decoded_text
        print(str(shift) + ': ' + decoded_text)

        # [보너스과제] 사전 단어가 발견되면 반복을 멈춘다.
        if has_keyword(decoded_text, KEYWORD_DICTIONARY):
            print('사전에 있는 단어를 발견했습니다.')
            break

    return decoded_dict


# [수행과제] 확인한 번호의 해독 결과를 result.txt 파일에 저장한다.
def save_result_file(file_path: str, decoded_text: str) -> bool:
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(decoded_text)
        return True
    except OSError:
        print('result.txt 파일을 저장하는 중 오류가 발생했습니다.')

    return False


def main() -> None:
    password_text = read_password_file(PASSWD_PATH)

    if not password_text:
        return

    # [수행과제] 해독 결과를 순서대로 출력한다.
    decoded_results = caesar_cipher_decode(password_text)

    found_number = max(decoded_results)

    # [수행과제] 확인한 번호의 해독 결과를 result.txt 파일에 저장한다.
    is_saved = save_result_file(
        RESULT_PATH,
        decoded_results[found_number]
    )

    if is_saved:
        print('result.txt 파일에 저장되었습니다.')


if __name__ == '__main__':
    main()