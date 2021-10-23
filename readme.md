## Python语言课程知识图谱构建流程

### 课程语料获取

使用Scrapy爬取菜鸟教程的Python课程（https://www.runoob.com/python3）

```
    scrapy startproject runoob
    cd runoob
    scrapy genspider -t crawl python_tutorial runoob.com
    scrapy list
    scrapy crawl python_tutorial
```