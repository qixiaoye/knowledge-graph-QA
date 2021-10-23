# 问句类型分类脚本

import os
import ahocorasick


class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 实例词
        self.course_list_path = os.path.join(cur_dir, 'wordList/course_list.txt')
        self.chapter_list_path = os.path.join(cur_dir, 'wordList/chapter_list.txt')
        self.point_list_path = os.path.join(cur_dir, 'wordList/point_list.txt')
        self.course_words = [i.strip() for i in open(self.course_list_path, encoding='utf-8') if i.strip()]
        self.chapter_words = [i.strip() for i in open(self.chapter_list_path, encoding='utf-8') if i.strip()]
        self.point_words = [i.strip() for i in open(self.point_list_path, encoding='utf-8') if i.strip()]
        # 领域词
        self.region_words = set(self.chapter_words + self.course_words + self.point_words)

        # 构造领域AC树
        self.region_tree = self.build_actree(list(self.region_words))

        # 否定词
        self.deny_path = os.path.join(cur_dir, 'wordList/deny.txt')
        self.deny_words = [i.strip() for i in open(self.deny_path, encoding='utf-8') if i.strip()]

        # 属性词
        self.property_path = os.path.join(cur_dir, 'wordList/data_property_list.txt')
        self.property_words = [i.strip() for i in open(self.property_path, encoding='utf-8') if i.strip()]

        # 构建{实例词：实例词对应的概念}形式的词典
        self.word_type_dict = self.build_word_type_dict()

        # 问句疑问词，对象属性：前驱 \ 后继 \ 同义 \ 属于 \ 包含 \ 相关 \ 其他
        self.belong_question_words = ['属于什么', '属于']
        self.contain_question_words = ['包含什么', '包含', '有什么', '有哪些']
        self.previous_question_words = ['之前', '先学习', '需要先学习', '学习前']
        self.next_question_words = ['之后', '然后学习', '可以学习', '还要学习', '学习后']
        self.related_question_words = ['相关', '关联']
        self.same_question_words = ['相同', '一样', '相似', '类似']
        self.property_question_words = ['是什么', '什么是', '如何', '怎么样', '怎样']

        return

    # 分类主函数，输入自然问句
    def classify(self, question):
        data = {}
        # 获取问句中包含的领域词及其所在领域，并收集问句当中所涉及到的实体类型
        point_dict = self.check_point(question)
        data['args'] = point_dict

        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in point_dict.values():
            types += type_

        question_types = []

        # 基于问句疑问词进行分类，判断问句属于哪种类型

        # 属于
        if self.check_words(self.belong_question_words, question) and ('知识点' in types):
            question_type = 'point_belong_question'  # 知识点属于关系
            question_types.append(question_type)

        if self.check_words(self.belong_question_words, question) and ('章节' in types):
            question_type = 'chapter_belong_question'  # 章节属于关系
            question_types.append(question_type)

        # 包含
        if self.check_words(self.contain_question_words, question) and ('知识点' in types):
            question_type = 'point_contain_question'  # 知识点包含关系
            question_types.append(question_type)

        if self.check_words(self.contain_question_words, question) and ('章节' in types):
            question_type = 'chapter_contain_question'  # 章节包含关系
            question_types.append(question_type)

        # 前驱
        if self.check_words(self.previous_question_words, question) and ('知识点' in types):
            question_type = 'point_previous_question'  # 知识点前驱关系
            question_types.append(question_type)

        if self.check_words(self.previous_question_words, question) and ('章节' in types):
            question_type = 'chapter_previous_question'  # 章节前驱关系
            question_types.append(question_type)

        # 后继
        if self.check_words(self.next_question_words, question) and ('知识点' in types):
            question_type = 'point_next_question'  # 知识点后继关系
            question_types.append(question_type)

        if self.check_words(self.next_question_words, question) and ('章节' in types):
            question_type = 'chapter_next_question'  # 章节后继关系
            question_types.append(question_type)

        # 相关
        if self.check_words(self.related_question_words, question) and ('知识点' in types):
            question_type = 'point_related_question'  # 知识点相关关系
            question_types.append(question_type)

        # 同义
        if self.check_words(self.same_question_words, question) and ('知识点' in types):
            question_type = 'point_same_question'  # 知识点同义关系
            question_types.append(question_type)

        # 属性
        if self.check_words(self.property_question_words, question) and ('知识点' in types):
            question_type = 'point_property_question'  # 知识点属性关系
            question_types.append(question_type)

        if self.check_words(self.property_words, question) and ('知识点' in types):
            question_type = self.get_words(self.property_words, question)  # 知识点属性关系
            question_types.append(question_type)

        # 将多个分类结果进行合并处理，组装成一个问句类型字典
        data['question_types'] = question_types

        return data

    # 根据7类实体构造 { 特征词：特征词对应实体类型 } 形式的词典
    def build_word_type_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.course_words:
                wd_dict[wd].append('课程')
            if wd in self.chapter_words:
                wd_dict[wd].append('章节')
            if wd in self.point_words:
                wd_dict[wd].append('知识点')
        return wd_dict

    # 构造actree，加速过滤
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()  # 通过ahocorasick库（字符串匹配算法），初始化trie树（字符串索引的词典）
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))  # 向trie树中添加单词
        actree.make_automaton()  # 将trie树转化为Aho-Corasick自动机（在Trie树上实现KMP，可以完成多模式串的匹配），在一次运行中找到给定集合所有字符串
        return actree

    # 问句过滤
    def check_point(self, question):
        region_wds = []
        # ahocorasick库的iter()函数匹配问题，将有重复字符串的领域词去除短的，取最长的领域词返回
        # 过滤问句中含有的领域词，返回{问句中的领域词：词所对应的实体类型}
        for i in self.region_tree.iter(question):
            wd = i[1][1]  # 匹配到的词
            region_wds.append(wd)

        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)  # stop_wds取重复的短的词

        final_wds = [i for i in region_wds if i not in stop_wds]  # final_wds取长词
        final_dict = {i: self.word_type_dict.get(i) for i in final_wds}  # 获取词和词所对应的实体类型
        return final_dict

    # 检查问句中是否含有某词
    def check_words(self, words, sent):
        for wd in words:
            if wd in sent:
                return True
        return False

    # 获取该词
    def get_words(self, words, sent):
        for wd in words:
            if wd in sent:
                return wd
        return None


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        a_question = input('\n输入测试问句:')
        a_data = handler.classify(a_question)
        print('问句类型解析结果:')
        print(repr(a_data))
