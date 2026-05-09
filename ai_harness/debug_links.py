import re
with open('test_ddg.html', 'r', encoding='utf-16') as f:
    content = f.read()
    title = re.search(r'<title>(.*?)</title>', content)
    print(f"Title: {title.group(1) if title else 'N/A'}")
    if "verification" in content.lower() or "captcha" in content.lower():
        print("Captcha detected")
    print(f"Content length: {len(content)}")
    print(content[:1000])
