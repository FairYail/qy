import csv


def read_csv_file():
    """
    读取CSV文件，返回一个列表，其中每个元素是一个字典对象，表示一行数据
    :param file_path: CSV文件的路径
    :return: 包含所有数据的列表
    """
    with open("./dtl.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        data = []
        for row in csv_reader:
            data.append(dict(zip(headers, row)))
        return data
