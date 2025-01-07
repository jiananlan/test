import browser_cookie3
import time

# 获取 Firefox 的 Cookies
cookies = browser_cookie3.firefox()  # 获取 Firefox 浏览器的 Cookies

# 将 Cookies 保存为 Netscape 格式的文件
with open('cookies.txt', 'w') as f:
    f.write("# Netscape HTTP Cookie File\n")
    for cookie in cookies:
        # 确保域名以 . 开头
        domain = f".{cookie.domain}" if not cookie.domain.startswith('.') else cookie.domain
        
        # 确保 secure 字段是 'TRUE' 或 'FALSE'
        secure = 'TRUE' if cookie.secure else 'FALSE'
        
        # 如果没有过期时间，则用 None 或 0 来代替（确保格式正确）
        expires = cookie.expires if cookie.expires else 0

        # 确保 cookie 路径为 '/' 或其他有效路径
        path = cookie.path if cookie.path else '/'
        
        # 确保 cookie 名称和值不是 None 或空值
        name = cookie.name if cookie.name else ''
        value = cookie.value if cookie.value else ''
        
        # 确保 name 和 value 的长度是有效的，避免空值
        if not name or not value:
            continue  # 跳过无效的 Cookie
        
        # 将每条 cookie 按照 Netscape 格式写入文件
        f.write(f"{domain}    TRUE    {path}    {secure}    {expires}    {name}    {value}\n")
