from hybrider import hybrid_search

queries=['流式','助手协作模式里验收类检查由谁跑','流式 reasoning','postgresql']
results=hybrid_search(queries)

if __name__ == "__main__":
    print(results)