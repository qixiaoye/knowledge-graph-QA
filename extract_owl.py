import rdflib

# 需要获取的词表
class_list = []  # 类
data_property_list = []  # 数据属性
object_property_list = []  # 对象属性
point_list = []  # 知识点实例
chapter_list = []  # 章节实例
course_list = []  # 课程实例
# 三元组存储
turtle_list = []


def save_word_list(a_type, word):
    if a_type == 'owl:Class':
        class_list.append(word)
    elif a_type == 'owl:DatatypeProperty':
        data_property_list.append(word)
    elif a_type == 'owl:ObjectProperty':
        object_property_list.append(word)
    elif a_type == ':知识点,':
        point_list.append(word)
    elif a_type == ':章节,':
        chapter_list.append(word)
    elif a_type == ':课程,':
        course_list.append(word)


def save_turtle_list(a_subject, a_property, a_object):
    turtle = a_subject + ' ; ' + a_property + " ; " + a_object
    turtle_list.append(turtle)


def export_word_list(path='wordList'):
    with open(path + '/class_list.txt', "w+") as f:
        data = '\n'.join(list(class_list))
        f.write(data)
        f.close()
    with open(path + '/data_property_list.txt', "w+") as f:
        data = '\n'.join(list(data_property_list))
        f.write(data)
        f.close()
    with open(path + '/object_property_list.txt', "w+") as f:
        data = '\n'.join(list(object_property_list))
        f.write(data)
        f.close()
    with open(path + '/point_list.txt', "w+") as f:
        data = '\n'.join(list(point_list))
        f.write(data)
        f.close()
    with open(path + '/chapter_list.txt', "w+") as f:
        data = '\n'.join(list(chapter_list))
        f.write(data)
        f.close()
    with open(path + '/course_list.txt', "w+") as f:
        data = '\n'.join(list(course_list))
        f.write(data)
        f.close()
    with open(path + '/turtle_list.txt', "w+") as f:
        data = '\n'.join(list(reversed(turtle_list)))
        f.write(data)
        f.close()


def extract_owl():
    # 引入RDF的主要接口Graph
    g = rdflib.Graph()

    # 解析对应的OWL文件
    g.parse("Python编程课程本体.owl")

    # 循环Graph中的三元组
    for subj, pred, obj in g:
        # 检查Graph中是否至少有一个三元组
        if (subj, pred, obj) not in g:
            raise Exception("It better be!")

    # 自带的三元组形式化
    result = g.serialize(format="turtle").decode("utf-8")

    # 按照每个概念/实例主体分割为列表
    result_list = result.split('\n\n')

    # 循环处理
    # 其中第一行是OWL本体文件的描述，第二行是本体的URL索引，不处理
    for result_index in range(len(result_list)):
        if result_index == 0 or result_index == 1:
            continue
        if len(result_list[result_index]) == 0:
            continue
        temp_list = result_list[result_index].split('\n')
        # print(temp_list)
        a_subject = ''  # 主语
        for temp_index in range(len(temp_list)):
            # 第一行，获取三元组的主语，和所属词表
            if temp_index == 0:
                first_list = temp_list[temp_index].split(' ')
                a_subject = first_list[0].lstrip(':')
                a_type = first_list[2]
                save_word_list(a_type, a_subject)
            else:
                if len(temp_list) == 2:
                    other_list = temp_list[temp_index].strip().split(' ')
                    if 'rdfs:subClassOf' in other_list:
                        save_turtle_list(a_subject, 'subClassOf', other_list[1].lstrip(':'))
                    elif 'rdfs:subPropertyOf' in other_list or 'owl:NamedIndividual' in other_list:
                        # 关系之间的关系不存入三元组，实例和概念的关系已存入词表，此处不做讨论
                        continue
                else:
                    if temp_index >= 2:
                        line = temp_list[temp_index].strip().lstrip(':')
                        a_property = ''
                        a_object = ''
                        flag = False
                        start_index = 0
                        end_str = ''
                        for line_index in range(len(line)):
                            if flag is False and line[line_index] != ' ':
                                a_property += line[line_index]
                            elif flag is False and line[line_index] == ' ':
                                flag = True
                                start_index = line_index + 1
                            elif flag is True and start_index == line_index:
                                if line[line_index] == '"':
                                    end_str = '"'
                                elif line[line_index] == ':':
                                    end_str = ' '
                            elif flag is True and line[line_index] != end_str:
                                a_object += line[line_index]
                            elif flag is True and line[line_index] == end_str:
                                break
                        save_turtle_list(a_subject, a_property, a_object)

    # 处理词表中隐含的三元组关系
    for a_point in point_list:
        save_turtle_list(a_point, 'type', '知识点')
    for a_chapter in chapter_list:
        save_turtle_list(a_chapter, 'type', '章节')
    for a_course in course_list:
        save_turtle_list(a_course, 'type', '课程')


if __name__ == '__main__':
    extract_owl()
    export_word_list()
