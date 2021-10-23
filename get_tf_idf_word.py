import os
import math
import operator


# 获取停用词表
def get_stop_word(path):
    stop_word_list = []
    for i in read_file(path):
        out_stop_word = str(i).replace('\n', '')
        stop_word_list.append(out_stop_word)
    return stop_word_list


# 遍历文件夹中的所有文件，返回文件list
def get_files(dir_path):
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            path = os.path.join(root, file)
            file_list.append(path)
    return file_list


# 建立语料库(所有文章合并起来的wordlist)
def build_corpus(file_list, stop_word_list):
    corpus_list = []
    for file in file_list:
        clean_word_list = get_clean_word_list(read_file(str(file)), stop_word_list)
        corpus_list.append(clean_word_list)
    return corpus_list


# 读取txt文件，并返回list(词表)
def read_file(path):
    f = open(path, encoding="utf8")
    data = []
    for line in f.readlines():
        data.append(line.strip())
    return data


# 去除文章中的停用词
def get_clean_word_list(file_word_list, stop_word_list):
    clean_word_list = []
    for word in file_word_list:
        if str(word) in stop_word_list:
            continue
        else:
            clean_word_list.append(str(word))
    return clean_word_list


# 统计词频，并返回字典
def get_frequency_word(word_list):
    frequency_word = {}
    for word in word_list:
        if str(word) in frequency_word:
            count = frequency_word[str(word)]
            frequency_word[str(word)] = count + 1
        else:
            frequency_word[str(word)] = 1
    return frequency_word


# 查出包含该词的文档数
def get_word_in_file_count(clean_word, corpus_list):
    count = 0  # 计数器
    for i in corpus_list:
        for j in i:
            if clean_word in set(j):  # 只要文档出现该词，这计数器加1，所以这里用集合
                count = count + 1
            else:
                continue
    return count


# 计算TF-IDF,并返回字典
def tf_idf(clean_word_list, file_list, corpus_list):
    # clean_word_list 去除停用词后的词表
    # file_list 文档集合
    # corpus_list 文档集合词汇
    out_dict = {}
    frequency_word = get_frequency_word(clean_word_list)  # 统计词频，并返回字典
    for clean_word in set(clean_word_list):
        # 计算TF
        tf = frequency_word[str(clean_word)] / len(clean_word_list)
        # 计算IDF
        idf = math.log(len(file_list) / (get_word_in_file_count(str(clean_word), corpus_list) + 1))
        # 计算TF-IDF
        tfidf = tf * idf
        out_dict[str(clean_word)] = tfidf
    order_dict = sorted(out_dict.items(), key=operator.itemgetter(1), reverse=True)  # 给字典排序
    return order_dict


# 写入预处理，将list转为string
def before_write_file(lis):
    out_all = ''
    for i in lis:
        ech = str(i).replace("('", '').replace("',", '\t').replace(')', '')
        out_all = out_all + '\t' + ech + '\n'
    return out_all


def loop_segment_txt():
    stop_word_path = r'hit_stopwords.txt'  # 停用词表路径
    stop_word_list = get_stop_word(stop_word_path)  # 获取停用词表列表

    dir_path = r'segmentTXT'
    file_list = get_files(dir_path)  # 获取文件列表

    corpus_list = build_corpus(file_list, stop_word_list)  # 建立语料库

    for file in file_list:
        # 获取每一篇已经去除停用的词表
        clean_word_list = get_clean_word_list(read_file(str(file)), stop_word_list)
        # print(read_file(str(file)))
        # print(clean_word_list)
        # 计算TF-IDF
        tf_idf_dict = tf_idf(clean_word_list, file_list, corpus_list)
        # 存储TF-IDF值
        file_name = str(file).split('/')[1]
        tfidf_word_path = 'tfidfWord/' + file_name
        with open(tfidf_word_path, "w+") as f:
            f.write(before_write_file(tf_idf_dict))
            print(file_name + ' is ok!')
            f.close()


if __name__ == '__main__':
    loop_segment_txt()
