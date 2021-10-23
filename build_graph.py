# 将实体和三元组导入neo4j，构建知识库
# Cypher语句清空所有数据：match (n) detach delete n

from py2neo import Graph, Node


class KnowledgeGraph:
    def __init__(self):
        # neo4j数据库连接
        self.graph = Graph('http://1.117.28.192:7474', auth=('neo4j', 'lsy-pass'))
        # 实例文件
        self.course_list = []
        self.chapter_list = []
        self.point_list = []
        self.turtle_list = []
        # 关系文件
        self.data_property_list = []  # 数据属性
        self.object_property_list = []  # 对象属性

    # 读取数据文件
    def read_nodes(self):
        # 课程实例
        with open('wordList/course_list.txt', "r") as f:
            self.course_list = f.read().split('\n')
        # 章节实例
        with open('wordList/chapter_list.txt', "r") as f:
            self.chapter_list = f.read().split('\n')
        # 知识点实例
        with open('wordList/point_list.txt', "r") as f:
            self.point_list = f.read().split('\n')
        # 数据属性关系
        with open('wordList/data_property_list.txt', "r") as f:
            self.data_property_list = f.read().split('\n')
        # 对象属性关系
        with open('wordList/object_property_list.txt', "r") as f:
            self.object_property_list = f.read().split('\n')
        # 三元组实例
        with open('wordList/turtle_list.txt', "r") as f:
            self.turtle_list = f.read().split('\n')

    # 创建普通实体节点
    def create_node(self, label, nodes):
        count = 0
        # 对每一个节点，调用py2neo库中Graph类的create函数，在neo4j中创建label为实体类别，name为具体实体名称的节点
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.graph.create(node)
            count += 1
            print(label, count, node_name, len(nodes))

    # 创建普通实体节点模块
    def create_graph_nodes(self):
        self.create_node('课程', self.course_list)
        self.create_node('章节', self.chapter_list)
        self.create_node('知识点', self.point_list)

    # 根据名字判断并获取节点
    def get_node_label(self, content):
        if content in self.course_list:
            return '课程'
        elif content in self.chapter_list:
            return '章节'
        elif content in self.point_list:
            return '知识点'
        else:
            return None

    # 创建实体关系边(object_property)
    def create_graph_relations(self):
        for turtle in self.turtle_list:
            content_list = turtle.split(' ; ')
            start_node_label = self.get_node_label(content_list[0])
            end_node_label = self.get_node_label(content_list[2])
            if start_node_label is not None and end_node_label is not None:
                # 调用py2neo库中Graph类的run函数，使用Cypher语言直接执行Neo4j CQL语句，对每一对实体关系在neo4j里创建边
                query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    start_node_label, end_node_label, content_list[0], content_list[2], content_list[1],
                    content_list[1])
                try:
                    self.graph.run(query)
                    print(content_list[0], content_list[1], content_list[2])
                except Exception as e:
                    print(e)

    # 为有多个属性的实体添加属性
    def add_node_property(self):
        for turtle in self.turtle_list:
            content_list = turtle.split(' ; ')
            start_node_label = self.get_node_label(content_list[0])
            end_node_label = self.get_node_label(content_list[2])
            if start_node_label is not None and end_node_label is None:
                # 使用Cypher语言直接执行Neo4j CQL语句，添加属性
                query = "match(p {name: '%s'}) set p.%s='%s'" % (content_list[0], content_list[1], content_list[2])
                try:
                    self.graph.run(query)
                    print(content_list[0], content_list[1], content_list[2])
                except Exception as e:
                    print(e)

    def build_graph_main(self):
        self.read_nodes()
        self.create_graph_nodes()
        self.create_graph_relations()
        self.add_node_property()


if __name__ == '__main__':
    handler = KnowledgeGraph()
    handler.build_graph_main()
