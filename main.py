import sys
import requests

from bs4 import BeautifulSoup
from clint.textui import progress


def getChaptersList(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    with requests.Session() as request:
        response = request.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")
        seasons = soup.find_all('div', {'class': 'tvseason'})

        for season in seasons:
            title = season.find('strong').text.strip()
            links = season.find_all('a')
            for link in links:
                try:
                    if 'episode' in link['href']:
                        print("%s %s, %s" % (title, link.text.strip(), link['href'].strip()))
                except KeyError:
                    pass


def getVideoID(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    with requests.Session() as request:
        response = request.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")
        iframe = soup.find('iframe')

    return iframe['src'].split('/')[-1]


def getVideoSource(video_id):
    headers = {
        'authority': 'pvip.nl',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://pvip.nl',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://pvip.nl/v/%s' % video_id,
        'accept-language': 'es-419,es;q=0.9,en;q=0.8,gl;q=0.7,la;q=0.6',
        'cookie': '_ym_uid=1608942855461123898; _ym_d=1608942855; __cfduid=d6ea87f3cd3af769d01ae3138eb5861571609291009',
    }

    data = {
      'r': '',
      'd': 'pvip.nl'
    }

    response = requests.post('https://pvip.nl/api/source/%s' % video_id, headers=headers, data=data)
    response = response.json()

    if not response['data'] == 'Video not found or has been removed':
        for file in response['data']:
            if file['label'] == '720p':
                response = requests.get(file['file'], headers=headers, allow_redirects=False)
                video_source = response.headers['Location']
                print(' > %s' % video_source)
                return video_source

    else:
        print(video_source['data'])
        return False



def downloadVideo(video_source, output_name):
    headers = {
        'authority': 'pvip.nl',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://pvip.nl',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://pvip.nl/v/%s' % video_id,
        'accept-language': 'es-419,es;q=0.9,en;q=0.8,gl;q=0.7,la;q=0.6',
        'cookie': '_ym_uid=1608942855461123898; _ym_d=1608942855; __cfduid=d6ea87f3cd3af769d01ae3138eb5861571609291009',
    }

    response = requests.get(video_source, headers=headers, stream=True)

    with open("%s.mp4" % output_name, 'wb') as video:
        total_length = int(response.headers.get('content-length'))

        for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
            if chunk:
                video.write(chunk)


if __name__ == '__main__':
    if sys.argv[1] == 'scrap':
        getChaptersList(sys.argv[2])

    elif sys.argv[1] == 'download':
        list_file = open(sys.argv[2], 'r')
        list = list_file.read().strip()

        for line in list.split('\n'):
            print(line)
            title, url = line.split(',')

            video_id = getVideoID(url.strip())
            video_source = getVideoSource(video_id)

            if video_source:
                downloadVideo(video_source, title)
