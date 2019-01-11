import argparse
import requests


def main():
    global args
    args = None
    log('Booting up.')
    log('Mass Proxy Checker by ducla: v1.0.0')
    parser = argparse.ArgumentParser(description='Check some proxies')
    parser.add_argument('-i', '--input-file',
                        default='proxies.txt', help='Proxy file to check.')
    parser.add_argument('-ob', '--out-banned', default='banned.txt',
                        help='File to write banned proxies to (banned)')
    parser.add_argument('-of', '--out-good', default='good.txt',
                        help='File to write good proxies to (not banned)')
    parser.add_argument('-ef', '--error-file', default='error.txt',
                        help='File to store errored out proxies')
    parser.add_argument('-t', '--timeout', default=5,
                        help='Timeout for requests to servers.')
    args = parser.parse_args()

    servers = []
    with open('servers.txt', 'r') as sv:
        servers = sv.read().split('\n')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

    with open(args.input_file, 'r+') as f, open(args.out_banned, 'w+') as banned, open(args.out_good, 'w+') as good, open(args.error_file, 'w+') as error:
        proxies = f.read().splitlines()
        for p in proxies:
            # TODO: Use multithreading to make it go ZOOM ZOOM
            log('Attempting to check proxy {}...'.format(p))
            pr = {
                'http': p,
                'https': p
            }
            flag = check_proxy(p, pr, servers, headers)

            if flag == 0:
                good.write('{}\n'.format(p))
            elif flag == 1:
                banned.write('{}\n'.format(p))
            else:
                error.write('{}\n'.format(p))

        f.close()
        good.close()
        banned.close()
        error.close()


def log(message, char='+'):
    print('[{}] {}'.format(char, message))


def verbose_log(message, char='+'):
    print('--> [{}] {}'.format(char, message))

# TODO: Multi thread to faster check


def check_proxy(p, proxy, servers, header):
    for server in servers:
        flag = -1
        try:
            verbose_log(
                'Sending HTTP request to {}, watiting for response...'.format(server))
            r = requests.get(server, proxies=proxy, timeout=float(
                args.timeout), headers=header)
            verbose_log('Received response from {} : {}'.format(
                server, r.status_code))
            if r.status_code == 200 or r.status_code == 301:
                flag = 0
                verbose_log('{}, 200 OK, proxy is not banned on: {}.'.format(
                    p, server))
            if r.status_code == 403:
                verbose_log(
                    '{}, 403 Forbidden, proxy is banned on : {}.'.format(p, server))
                flag = 1
        except requests.exceptions.Timeout:
            verbose_log('{}, Timed out after {} seconds.'.format(
                p, args.timeout))
        except requests.exceptions.RequestException as e:
            verbose_log('{pr}, Unable to connect to the proxy {pr}, or timed out. Make sure to add https://, and the port.'.format(
                pr=p))
            log('requestsexception: ' + str(e), '!')
        if flag != 0:
            break
    return flag


if __name__ == '__main__':
    main()
