# Check bulk proxy with python

## How to use:
 - Clone repo and go in folder:
 - put proxy list on proxies.txt
 - run:
    ```
    python proxy_checker.py
    ```
- agruments:
  - -i or --input-file: Proxy file to check. Default is proxies.txt
  - -ob or --out-banned: File to write banned proxies to (banned)'). Default is banned.txt
  - -of or --out-good: File to write good proxies to (not banned)'). Default is good.txt
  - -ef or --error-file: File to store errored out proxies'). Default is error.txt
  - -t or --timeout: 'Timeout for requests to servers.'). Default is 5s

## Customize servers to check:
 - Replace server you need to work with in file servers.txt. One per line
 - 
## TODO: 
 - Using multi threads to run faster
 - Detect location and anonymity of proxy
 - Sort result by response, speed ...