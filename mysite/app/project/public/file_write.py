import time
import numpy as np
from abc import abstractmethod, ABC


def decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f'{func.__name__} start in {start}')
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} executed in {round(end - start, 2)} seconds')
        return result
    return wrapper


# ABC 定义基类, 不可被实例化
class ProcessStrategy(ABC):
    @abstractmethod
    def process_file(self, file_path):
        pass


class ExcelProcessStrategy(ProcessStrategy):
    def process_file(self, file_path):
        pass

    @decorator
    def write_file(self, writer, df, chunk_size: int):
        num_parts = int(np.ceil(df.shape[0] / chunk_size))
        for i in range(num_parts):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size
            df_part = df.iloc[start_idx:end_idx]
            sheet_name_tmp = 'Sheet' + '_' + str(i) + '_' + str(start_idx) + '_' + str(end_idx)
            df_part.to_excel(writer, sheet_name=sheet_name_tmp, index=False)

            workbook = writer.book
            cell_format = workbook.add_format({'font_name': '等线', 'font_size': 10})
            worksheet = writer.sheets[sheet_name_tmp]
            worksheet.set_column('A:CZ', None, cell_format)  # 应用格式到A和B列

    @decorator
    def write_file_without_format(self, writer, df, chunk_size: int):
        num_parts = int(np.ceil(df.shape[0] / chunk_size))
        for i in range(num_parts):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size
            df_part = df.iloc[start_idx:end_idx]
            sheet_name_tmp = 'Sheet' + '_' + str(i) + '_' + str(start_idx) + '_' + str(end_idx)
            df_part.to_excel(writer, sheet_name=sheet_name_tmp, index=False)

class ParquetProcessStrategy(ProcessStrategy):
    def process_file(self, file_path):
        pass

    @decorator
    def write_file(self, file_path, df):
        df.to_parquet(file_path, engine='pyarrow')


class FileProcessor:
    def __init__(self, df, writer=None):
        self.chunk_size = 1000000
        self.writer = writer
        self.df = df

    def write_file(self):
        ExcelProcessStrategy().write_file(writer=self.writer, df=self.df, chunk_size=self.chunk_size)
    def write_file_without_format(self):
        ExcelProcessStrategy().write_file_without_format(writer=self.writer, df=self.df, chunk_size=self.chunk_size)

