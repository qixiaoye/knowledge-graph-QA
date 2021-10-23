from bs4 import BeautifulSoup
import os


def get_stripped_strings(bs):
    strings = ''
    for string in bs.stripped_strings:
        strings += string
    return strings


def get_strings(bs):
    strings = ''
    for string in bs.strings:
        strings += string
    return strings.strip()


def get_section_div_list(bs):
    section_list = []
    for div in bs.find_all('div'):
        # section div
        if div.attrs != {} and div.has_attr('class') and 'section' in div['class']:
            section_list.append(div)
    return section_list


def get_pure_txt(path):
    bs = BeautifulSoup(open(path), 'html.parser')
    section_list = get_section_div_list(bs)
    pure_txt = ''
    # 遍历section节点
    for section in section_list:
        for tag in section.children:
            if tag.name is not None:
                # section内的section，跳过
                if tag.attrs != {} and tag.has_attr('class') and 'section' in tag['class']:
                    continue
                # 代码，跳出
                if tag.name == 'pre':
                    continue
                # 代码实例，跳过
                if tag.attrs != {} and tag.has_attr('class') and 'highlight-default' in tag['class']:
                    continue
                # 无内容的标记，跳过
                if get_stripped_strings(tag) == '':
                    continue
                pure_txt += get_stripped_strings(tag) + '\n'
    return pure_txt


def loop_raw_html():
    # pure_txt = get_pure_txt('index.txt')
    # print(pure_txt)
    for root, dirs, files in os.walk('rawHTML'):
        for file in files:
            path = os.path.join(root, file)
            pure_txt = get_pure_txt(path)
            txt_path = 'pureTXT/' + file
            with open(txt_path, "w+") as f:
                f.write(pure_txt)
                print(txt_path, 'is ok!')
                f.close()


if __name__ == '__main__':
    loop_raw_html()
