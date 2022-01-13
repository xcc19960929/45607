import os

proxy_host = 'http-dyn.abuyun.com'
proxy_port = '9020'
proxy_user = os.getenv('ABY_PROXY_USER', '')
proxy_pass = os.getenv('ABY_PROXY_PASS', '')
proxies = {
    'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
    'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
}