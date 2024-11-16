from scholarly import scholarly
def extract_authors_info(paper):
    """
    从论文信息中提取作者姓名和 Google Scholar ID
    :param paper: dict, 包含论文详细信息的字典
    :return: list, 包含作者信息的字典列表 [{name: author_name, scholar_id: author_id}, ...]
    """
    # 检查输入数据是否包含作者和作者 ID
    authors = paper.get("bib", {}).get("author", [])
    author_ids = paper.get("author_id", [])
    
    # 如果作者或作者 ID 缺失，返回错误信息
    if not authors or not author_ids:
        return "Mismatch between authors and author IDs. Please verify the input data."
    
    # 如果作者数量与 author_id 数量不一致，返回错误信息
    if len(authors) != len(author_ids):
        return "Mismatch between authors and author IDs. Please verify the input data."
    
    # 构造作者信息
    authors_info = [
        {"name": author, "google_scholar_id": scholar_id}
        for author, scholar_id in zip(authors, author_ids)
    ]
    
    return authors_info



def get_paper_authors_scholar_ids(paper_title):
    """
    根据论文标题查询论文作者的 Google Scholar ID
    :param paper_title: str, 论文标题
    :return: list, 包含每位作者的姓名和 scholar_id 的字典列表
    """
    try:
        from scholarly import ProxyGenerator

        # 创建 ProxyGenerator 对象
        pg = ProxyGenerator()
        pg.SingleProxy(http="http://172.67.141.14:80")

        # 将代理传递给 scholarly
        scholarly.use_proxy(pg)

        # scholarly.use_proxy("http://104.25.158.117:80")
        # 查询论文信息
        search_query = scholarly.search_pubs(paper_title)
        # print("search_query:", search_query)

        print("search_query type:", type(search_query))  # 打印返回类型
        for result in search_query:
            print("Search result:", result)

        paper = next(search_query, None)  # 获取第一篇匹配的论文
        if not paper:
            return f"No results found for the paper title: {paper_title}"
        
        # 打印论文标题
        print(f"Paper Title: {paper['bib']['title']}")
        
        return extract_authors_info(paper=paper) # return a list[dict]
    except Exception as e:
        return f"Error occurred: {e}"

# 测试函数
if __name__ == "__main__":
    paper_title = "Unpacking how decentralized autonomous organizations (daos) work in practice"
    authors_scholar_infos = get_paper_authors_scholar_ids(paper_title)
    print(authors_scholar_infos)
    if not isinstance(authors_scholar_infos, list):
        print(authors_scholar_infos)
    else:
        for author_info_dict in authors_scholar_infos:
            print(f"Author: {author_info_dict['name']}, Scholar ID: {author_info_dict['google_scholar_id']}")






