from ltp import LTP
import os


def loop_pure_txt():
    ltp = LTP()
    ltp.init_dict(path="it_dict.txt", max_window=4)  # 添加自定义的IT词库
    for root, dirs, files in os.walk('pureTXT'):
        for file in files:
            path = os.path.join(root, file)
            with open(path, "r") as f:  # 打开文件
                contents = f.read()
                sentences = ltp.sent_split([contents])  # 分句处理
                segments, hidden = ltp.seg(sentences)  # 分词处理
                print(segments)
                segment_txt = ''
                for segs in segments:
                    for seg in segs:
                        segment_txt += seg + "\n"
            segment_path = 'segmentTXT/' + file
            with open(segment_path, "w+") as f:
                f.write(segment_txt)
                f.close()


if __name__ == '__main__':
    loop_pure_txt()
