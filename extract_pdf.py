import pdfplumber


class PdfExtractor:
    def __init__(self):
        self.texts = []
        self.data = ''

    # 提取pdf文件内容
    def extractor_main(self, path):
        with pdfplumber.open(path) as pdf:  # 获取pdfplumber.PDF类的实例
            # 分页读取文字
            for index in range(len(pdf.pages)):  # 遍历pdfplumber.Page实例的列表，每个实例代表PDF每页的信息
                page = pdf.pages[index]  # 当前页的Page实例
                text = page.extract_text()  # 提取页面的所有字符
                if text is not None:
                    self.texts.append(text.replace(' ', '').replace('\n', '').replace('\r', ''))  # 去除空格和换行符
            # 整合
            self.data = '\n'.join(list(self.texts))


if __name__ == '__main__':
    extractor = PdfExtractor()
    extractor.extractor_main('Python编程：从入门到实践.pdf')
    # 导出
    with open('Python编程：从入门到实践.txt', "w+") as f:
        f.write(extractor.data)
        f.close()
