import requests
import time
import random

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

def main():
    count = 1
    file = open('urls.txt', 'r')
    try:
        text_lines = file.readlines()
        print(type(text_lines))
    except:
        print('Error!')
    finally:
        file.close()
    with open('./ok_urls_1.txt', 'w+') as f:
        for line in text_lines[4140:]:
            time.sleep(1)
            line = line.strip()
            print('正在请求第{}个页面:{}'.format(count, line))
            response = requests.get(line, headers = headers)
            if response.status_code == 200:
                print('200!')
                f.write(line)
                f.write('\n')
            else:
                print('404！')
            count += 1
    
if __name__ == "__main__":
    main()
    print('Over!')