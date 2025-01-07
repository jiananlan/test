import browser_cookie3

# 获取 Chrome 或 Firefox 的 Cookies
cookies = browser_cookie3.firefox() # 或 browser_cookie3.firefox()

# 将 Cookies 保存为 Netscape 格式的文件
with open('cookies.txt', 'w') as f:
    for cookie in cookies:
        f.write(f"{cookie.domain}   TRUE   {cookie.path}   {cookie.secure}   {cookie.expires}   {cookie.name}   {cookie.value}\n")
with open('cookies.txt', 'r') as f:
    print(f.readlines())
