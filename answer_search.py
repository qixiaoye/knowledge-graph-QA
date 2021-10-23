# 问题查询及返回
import json
import os
from py2neo import Graph


class AnswerSearcher:
    def __init__(self):
        # neo4j数据库连接
        self.graph = Graph('http://localhost:7474', auth=('neo4j', 'lsy-pass'))
        # 返回答案列举的最大个数
        self.num_limit = 30

    # 执行cypher查询，并返回相应结果
    def search_main(self, cql_s):
        final_answers = []
        for cql_ in cql_s:
            question_type = cql_['question_type']
            queries = cql_['cql']
            answers = []
            for query in queries:
                result = self.graph.run(query).data()  # 执行[‘sql’]中的查询语句得到查询结果
                answers += result
            final_answer = self.answer_prettify(question_type, answers)  # 根据问句类型，将查询结果和答案话术结合起来
            if final_answer:
                final_answers.append(final_answer)
        return final_answers  # 返回最终答案

    # 根据对应的qustion_type，调用相应的回复模板
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''

        # 属性词
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        property_path = os.path.join(cur_dir, 'wordList/data_property_list.txt')
        property_words = [i.strip() for i in open(property_path, encoding='utf-8') if i.strip()]

        # 知识点属于关系
        if question_type == 'point_belong_question':
            subject = answers[0]['m.name']
            desc = [answer['n.name'] for answer in answers]
            if len(desc) == 0:
                final_answer = '知识点{0}是独立知识点，不属于任何知识点或章节'.format(subject)
            else:
                final_answer = '知识点{0}属于：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        # 章节属于关系
        elif question_type == 'chapter_belong_question':
            subject = answers[0]['m.name']
            desc = [answer['n.name'] for answer in answers]
            if len(desc) == 0:
                final_answer = '章节{0}是独立章节，不属于任何课程'.format(subject)
            else:
                final_answer = '章节{0}属于：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        # 知识点包含关系
        elif question_type == 'point_contain_question':
            subject = answers[0]['n.name']
            desc = [answer['m.name'] for answer in answers]
            if len(desc) == 0:
                final_answer = '知识点{0}不包含其他知识点'.format(subject)
            else:
                final_answer = '知识点{0}包含：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        # 章节包含关系
        elif question_type == 'chapter_contain_question':
            subject = answers[0]['n.name']
            desc = [answer['m.name'] for answer in answers]
            if len(desc) == 0:
                final_answer = '章节{0}是空章节，不包含任何知识点'.format(subject)
            else:
                final_answer = '章节{0}包含：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        # 知识点前驱关系
        elif question_type == 'point_previous_question':
            subject = answers[0]['m.name']
            desc = [answer['n.name'] for answer in answers]
            if len(desc) == 0:
                final_answer = '进行{0}学习之前不需要学习任何知识点'.format(subject)
            else:
                final_answer = '进行{0}学习之前需要学习的知识点有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        # 章节前驱关系
        elif question_type == 'chapter_previous_question':
            subject = answers[0]['m.name']
            desc = [answer['n.name'] for answer in answers]
            if len(desc) == 0:
                final_answer = '进行{0}学习之前不需要先学习其他章节'.format(subject)
            else:
                final_answer = '进行{0}学习之前需要学习的章节有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        # 知识点后继关系
        elif question_type == 'point_next_question':
            subject = answers[0]['n.name']
            desc = [answer['m.name'] for answer in answers]
            if len(desc) == 0:
                final_answer = '进行{0}学习之后没有其他需要学习的知识点'.format(subject)
            else:
                final_answer = '进行{0}学习之后可以学习的知识点有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        # 章节后继关系
        elif question_type == 'chapter_next_question':
            subject = answers[0]['n.name']
            desc = [answer['m.name'] for answer in answers]
            if len(desc) == 0:
                final_answer = '进行{0}学习之后没有其他需要学习的章节'.format(subject)
            else:
                final_answer = '进行{0}学习之后可以学习的章节有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        # 知识点相关关系
        elif question_type == 'point_related_question':
            subject = answers[0]['m.name']
            desc = [answer['n.name'] for answer in answers]
            if len(desc) == 0:
                final_answer = '没有{0}相关的知识点'.format(subject)
            else:
                final_answer = '和{0}相关的知识点有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        # 知识点同义关系
        elif question_type == 'point_same_question':
            subject = answers[0]['m.name']
            desc = [answer['n.name'] for answer in answers]
            if len(desc) == 0:
                final_answer = '没有和{0}相同意义的知识点'.format(subject)
            else:
                final_answer = '和{0}表示相同概念的知识点有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        # 知识点属性关系
        elif question_type == 'point_property_question':
            subject = answers[0]['m.name']
            desc = []
            for pro in property_words:
                pro_type = 'm.' + pro
                if answers[0][pro_type] is not None:
                    desc.append('\n' + pro + ': ' + answers[0][pro_type])
            if len(desc) == 0:
                final_answer = '知识点{0}暂时没有属性'.format(subject)
            else:
                final_answer = '知识点{0}有以下这些属性：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        # 知识点属性关系（数据属性）
        else:
            subject = answers[0]['m.name']
            property_type = 'm.' + question_type
            desc = [answer[property_type] for answer in answers]
            if len(desc) == 0:
                final_answer = '知识点{0}没有{1}属性'.format(subject, question_type)
            else:
                final_answer = '知识点{0}的{1}属性是：{2}'.format(subject, question_type, '；'.join(list(set(desc))[:self.num_limit]))
        return final_answer


if __name__ == '__main__':

    from question_classifier import *
    from question_parser import *

    classifier = QuestionClassifier()
    parser = QuestionParser()
    searcher = AnswerSearcher()
    while 1:
        question = input('\n输入测试问句:')
        data = classifier.classify(question)
        print(data)
        sqls = parser.parser_main(data)
        print(sqls)
        ans = searcher.search_main(sqls)
        print(ans)
