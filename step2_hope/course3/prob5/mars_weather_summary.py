import csv
import pymysql


# [보너스과제] 데이터베이스 연결 및 쿼리 실행을 쉽게 처리하기 위한 클래스 구현
class MySQLHelper:

    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            charset='utf8mb4'
        )
        self.cursor = self.connection.cursor()

    def execute_insert(self, query, args=None):
        if self.cursor is None:
            self.connect()
        self.cursor.execute(query, args)
        self.connection.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


# [수행과제] CSV 파일을 읽고 Python을 통해 MySQL 테이블에 INSERT 쿼리를 반복 실행하는 로직
def process_mars_weather_data(csv_file_path, db_config):
    db_helper = MySQLHelper(
        host=db_config.get('DB_HOST', '127.0.0.1'),
        user=db_config.get('DB_USER', 'root'),
        password=db_config.get('DB_PASSWORD', ''),
        database=db_config.get('DB_NAME', '')
    )

    try:
        db_helper.connect()

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)

            insert_query = (
                'INSERT INTO mars_weather (mars_date, temp, storm) '
                'VALUES (%s, %s, %s)'
            )

            for row in csv_reader:
                if len(row) >= 4:
                    mars_date = row[1]
                    temp = int(float(row[2]))  # 소수점 데이터 처리 에러 해결
                    storm = int(row[3])
                    
                    db_helper.execute_insert(insert_query, (mars_date, temp, storm))

        print('화성 날씨 데이터가 성공적으로 백업되었습니다.')

    except Exception as e:
        print(f'데이터 처리 중 오류가 발생했습니다: {e}')
        
    finally:
        db_helper.close()


def load_env(filepath='.env'):
    env_vars = {}
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        print('.env 파일을 찾을 수 없습니다.')
    
    return env_vars


if __name__ == '__main__':
    config = load_env('.env')
    
    if config:
        data_file = 'mars_weathers_data.csv'
        process_mars_weather_data(data_file, config)