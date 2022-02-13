import urllib3


def cookies_to_header(cookies):
    return {
        'Cookie': ';'.join(map(lambda cookie: f'{cookie["name"]}={cookie["value"]}', cookies))
    }


def download_file(url, path, cookies):
    headers = cookies_to_header(cookies)
    http = urllib3.PoolManager()
    r = http.request('GET', url, headers=headers, preload_content=False)
    with open(path, 'wb') as out:
        while True:
            data = r.read(2**16)
            if not data:
                break
            out.write(data)
    r.release_conn()
