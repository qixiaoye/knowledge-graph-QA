# 问句解析脚本

import os


class QuestionParser:

    # 构建实体节点
    # 从分类结果的{'args': {'break语句': ['知识点']}, 'question_types': ['point_belong_question']}中获取args
    # 返回{'知识点': ['break语句']}的形式
    def build_entity_dict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for a_type in types:
                if a_type not in entity_dict:
                    entity_dict[a_type] = [arg]
                else:
                    entity_dict[a_type].append(arg)
        return entity_dict

    # 解析主函数
    def parser_main(self, res_classify):
        args = res_classify['args']  # 从分类结果中获取args
        entity_dict = self.build_entity_dict(args)  # 返回形如{'实体类型':['领域词'],...}的entity_dict字典

        question_types = res_classify['question_types']  # 从分类结果中获取问句类型
        cql_s = []  # 转换为neo4j的Cypher语言，并组合
        for question_type in question_types:
            cql_ = {'question_type': question_type}
            if question_type == 'point_belong_question':  # 知识点属于关系
                cql = self.cql_transfer(question_type, entity_dict.get('知识点'))
            elif question_type == 'chapter_belong_question':  # 章节属于关系
                cql = self.cql_transfer(question_type, entity_dict.get('章节'))
            elif question_type == 'point_contain_question':  # 知识点包含关系
                cql = self.cql_transfer(question_type, entity_dict.get('知识点'))
            elif question_type == 'chapter_contain_question':  # 章节包含关系
                cql = self.cql_transfer(question_type, entity_dict.get('章节'))
            elif question_type == 'point_previous_question':  # 知识点前驱关系
                cql = self.cql_transfer(question_type, entity_dict.get('知识点'))
            elif question_type == 'chapter_previous_question':  # 章节前驱关系
                cql = self.cql_transfer(question_type, entity_dict.get('章节'))
            elif question_type == 'point_next_question':  # 知识点后继关系
                cql = self.cql_transfer(question_type, entity_dict.get('知识点'))
            elif question_type == 'chapter_next_question':  # 章节后继关系
                cql = self.cql_transfer(question_type, entity_dict.get('章节'))
            elif question_type == 'point_related_question':  # 知识点相关关系
                cql = self.cql_transfer(question_type, entity_dict.get('知识点'))
            elif question_type == 'point_same_question':  # 知识点同义关系
                cql = self.cql_transfer(question_type, entity_dict.get('知识点'))
            elif question_type == 'point_property_question':  # 知识点属性关系
                cql = self.cql_transfer(question_type, entity_dict.get('知识点'))
            else:    # 知识点属性关系(数据属性词库)
                cql = self.cql_transfer(question_type, entity_dict.get('知识点'))

            if cql:
                cql_['cql'] = cql
                cql_s.append(cql_)
        return cql_s

    # 将不同的问题类型，转换为Cypher查询语言并返回
    def cql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 属性词
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        property_path = os.path.join(cur_dir, 'wordList/data_property_list.txt')
        property_words = ['m.' + i.strip() for i in open(property_path, encoding='utf-8') if i.strip()]

        # 知识点属于关系
        if question_type == 'point_belong_question':
            cql1 = ["MATCH (m:知识点)-[r:属于]->(n:知识点) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            cql2 = ["MATCH (m:知识点)-[r:属于]->(n:章节) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            cql = cql1 + cql2
        # 章节属于关系
        elif question_type == 'chapter_belong_question':
            cql = ["MATCH (m:章节)-[r:属于]->(n:课程) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        # 知识点包含关系（x知识点 属于 知识点）
        elif question_type == 'point_contain_question':
            cql = ["MATCH (m:知识点)-[r:属于]->(n:知识点) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        # 章节包含关系
        elif question_type == 'chapter_contain_question':
            cql = ["MATCH (m:知识点)-[r:属于]->(n:章节) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        # 知识点前驱关系
        elif question_type == 'point_previous_question':
            cql = ["MATCH (m:知识点)-[r:前驱]->(n:知识点) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        # 章节前驱关系
        elif question_type == 'chapter_previous_question':
            cql = ["MATCH (m:章节)-[r:前驱]->(n:章节) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        # 知识点后继关系
        elif question_type == 'point_next_question':
            cql = ["MATCH (m:知识点)-[r:前驱]->(n:知识点) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        # 章节后继关系
        elif question_type == 'chapter_next_question':
            cql = ["MATCH (m:章节)-[r:前驱]->(n:章节) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        # 知识点相关关系
        elif question_type == 'point_related_question':
            cql = ["MATCH (m:知识点)-[r:相关]->(n:知识点) where m.name = '{0}' return m.name, r.name, n.name".format( i) for i in entities]
        # 知识点同义关系
        elif question_type == 'point_same_question':
            cql = ["MATCH (m:知识点)-[r:同义]->(n:知识点) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        # 知识点属性关系
        elif question_type == 'point_property_question':
            cql = ["MATCH (m:知识点) where m.name = '{0}' return m.name, {1}".format(i, ', '.join(property_words)) for i in entities]
        # 知识点属性关系（数据属性）
        else:
            cql = ["MATCH (m:知识点) where m.name = '{0}' return m.name, m.{1}".format(i, question_type) for i in entities]

        return cql


if __name__ == '__main__':

    from question_classifier import *

    handler = QuestionParser()
    QChandler = QuestionClassifier()
    while 1:
        question = input('\n输入测试问句:')
        data = QChandler.classify(question)
        print(data)
        sql = handler.parser_main(data)
        print(sql)
