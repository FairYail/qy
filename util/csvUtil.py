import csv


def read_csv_file():
    """
    读取CSV文件，返回一个列表，其中每个元素是一个字典对象，表示一行数据
    :param file_path: CSV文件的路径
    :return: 包含所有数据的列表
    """
    # with open("/home/dev/qy/util/dtl.csv", encoding="utf-8") as csv_file:
    with open("/Users/zhuchen/Desktop/qy/util/dtl.csv", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        data = []
        for row in csv_reader:
            data.append(row)
        return data
