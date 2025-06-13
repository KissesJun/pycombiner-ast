import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import defaultdict

visited = set()
site_map = defaultdict(set)

def crawl(url, base_url, depth=1):
    if depth == 0 or url in visited:
        return
    visited.add(url)
    print(f"Crawling: {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Response status: {response.status_code}")
        if not response.ok:
            print(f"Failed to get {url}: {response.status_code}")
            return
        
        print(f"Response content length: {len(response.text)}")
        soup = BeautifulSoup(response.text, 'html.parser')
        links_found = 0
        
        print("Found links:")
        for a_tag in soup.find_all('a', href=True):
            print(f"  Raw href: {a_tag['href']}")
            # if links_found >= 10:  # 增加每个页面处理的链接数
            #     break
            link = urljoin(base_url, a_tag['href'])
            parsed = urlparse(link)
            print(f"  Parsed link: {link}")
            print(f"  Parsed path: {parsed.path}")
            
            if base_url in link:
                path = parsed.path.strip('/')
                if path:
                    print(f"  Processing path: {path}")
                    parts = path.split('/')
                    if len(parts) > 0:
                        # 处理语言目录
                        # if parts[0] in ['zh', 'en', 'jp']:
                        #     # 将语言目录作为根目录
                        #     if len(parts) > 1:
                        #         site_map[parts[0]].add('/'.join(parts[1:]))
                        #     else:
                        #         site_map[parts[0]].add('index')
                        # else:
                        # 处理其他路径
                        parent = '/'.join(parts[:-1])
                        site_map[parent].add(parts[-1])
                        print(f"  Added to site_map: parent='{parent}', item='{parts[-1]}'")
                # links_found += 1
                crawl(link, base_url, depth - 1)
    except Exception as e:
        print(f"Failed to crawl {url}: {str(e)}")
        import traceback
        print(traceback.format_exc())

def print_tree(directory, prefix='', is_last=True):
    if not directory:
        return
    
    contents = sorted(site_map[directory])
    print(f"Directory '{directory}' has contents: {contents}")
    
    connector = '└── ' if is_last else '├── '
    print(f"{prefix}{connector}{directory.split('/')[-1]}/")
    
    for i, item in enumerate(contents):
        is_last_item = i == len(contents) - 1
        new_prefix = prefix + ('    ' if is_last else '│   ')
        new_dir = f"{directory}/{item}" if directory else item
        
        if item in site_map:
            print_tree(new_dir, new_prefix, is_last_item)
        else:
            connector = '└── ' if is_last_item else '├── '
            print(f"{new_prefix}{connector}{item}")

def write_tree_to_file():
    print("\nWriting to file...")
    with open('site_structure.txt', 'w', encoding='utf-8') as f:
        def print_to_file(directory, prefix='', is_last=True):
            if not directory and directory != '':
                return
            
            contents = sorted(site_map[directory])
            connector = '└── ' if is_last else '├── '
            f.write(f"{prefix}{connector}{directory.split('/')[-1]}/\n")
            
            for i, item in enumerate(contents):
                is_last_item = i == len(contents) - 1
                new_prefix = prefix + ('    ' if is_last else '│   ')
                new_dir = f"{directory}/{item}" if directory else item
                
                if item in site_map:
                    print_to_file(new_dir, new_prefix, is_last_item)
                else:
                    connector = '└── ' if is_last_item else '├── '
                    f.write(f"{new_prefix}{connector}{item}\n")
        
        print_to_file('')
    print("File writing completed")

# 使用一个测试网站
start_url = 'https://www.proface-sys.com/'
print("Starting crawl from:", start_url)
crawl(start_url, start_url)
print("\nCrawling completed. Found paths:")
print_tree('')

write_tree_to_file()
print("\nDone")






