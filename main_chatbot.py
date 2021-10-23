# 智能问答程序脚本

from question_classifier import *
from question_parser import *
from answer_search import *


# 本项目的问答系统完全基于规则匹配实现，通过关键词匹配，对问句进行分类，
# 然后使用cypher的match去匹配查找neo4j，根据返回数据组装问句回答，最后返回结果。

class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()  # 定义了QuestionClassifier类型的成员变量classifier
        self.parser = QuestionParser()  # 定义了QuestionParser类型的成员变量parser
        self.searcher = AnswerSearcher()  # 定义了AnswerSearcher类型的成员变量searcher

    # 传入问题sent
    def chat_main(self, sent):
        res_classify = self.classifier.classify(sent)  # 进行问句分类
        if not res_classify:
            return '抱歉，小助手暂时无法回答您的问题，请咨询老师。'  # 如果没有对应的分类结果，则输出模板句式

        res_cql = self.parser.parser_main(res_classify)  # 进行问句解析

        final_answers = self.searcher.search_main(res_cql)  # 查找对应的答案
        if not final_answers:
            return '抱歉，该问题无法在知识库中找到答案，请等待知识库的补充和完善。'  # 如果没有答案，则输出模板句式
        else:
            return '\n'.join(final_answers)


if __name__ == '__main__':
    print('\n欢迎来到智能问答服务，服务正在初始化，请等待。\n')
    handler = ChatBotGraph()
    print('\n初始化已完成，请输入你的问题。\n')
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('小助手:', answer, '\n')
