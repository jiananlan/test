import browser_cookie3

# 获取 Chrome 或 Firefox 的 Cookies
cookies = browser_cookie3.chrome()  # 或 browser_cookie3.firefox()

# 将 Cookies 保存为 Netscape 格式的文件
with open('cookies.txt', 'w') as f:
    for cookie in cookies:
        f.write(f".{cookie.domain}\tTRUE\t{cookie.path}\t{cookie.secure}\t{cookie.expires}\t{cookie.name}\t{cookie.value}\n")
