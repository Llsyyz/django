import pandas as pd
import os
from ..public import file_write

def order_combine(dingdan_dir, xiangmufenleibiao, dingdan_to_path, project):
    def sort(df, xiangmufenleibiao):
        dy_store_df = pd.read_excel(xiangmufenleibiao, engine='calamine', sheet_name='抖音项目')
        zb_store_df = pd.read_excel(xiangmufenleibiao, engine='calamine', sheet_name='直播项目')

        patterns = '|'.join(dy_store_df['店铺id'].astype(str))
        print(patterns)
        mask = df['店铺id'].str.contains(patterns, regex=True, na=False)
        dy_df = df[mask]

        patterns = '|'.join(zb_store_df['店铺id'].astype(str))
        print(patterns)
        mask = df['店铺id'].str.contains(patterns, regex=True, na=False)
        zb_df = df[mask]
        return dy_df, zb_df

    df_result = pd.DataFrame()
    for root, dirs, files in os.walk(dingdan_dir):
        for file in files:
            print(os.path.join(root, file))
            path = os.path.join(root, file)
            parts = path.split('\\')
            dir_name = parts[-2]
            parts = dir_name.split('-')
            df = pd.read_csv(str(path))
            df['店铺名称'] = str(parts[0])
            df['店铺id'] = str(parts[1])
            tmp = df.pop('店铺id')
            df.insert(0, '店铺id', tmp)
            tmp = df.pop('店铺名称')
            df.insert(0, '店铺名称', tmp)
            df_result = df_result._append(df, ignore_index=True)

    count = 0
    for column in df_result.columns:
        count = count + 1
        if column in ['店铺名称', '店铺id', '主订单编号', '子订单编号', '支付方式', '选购商品', '商品ID', '商家编码',
                      '订单提交时间', '支付完成时间', '订单完成时间', '旗帜颜色', '商家备注', '商家优惠', '订单状态',
                      '售后状态', '发货时间', '快递信息', '达人ID', '达人昵称', '流量来源', '广告渠道', '流量类型',
                      '流量体裁', '流量渠道', '取消原因', '平台优惠', '达人优惠']:
            count = count - 1
            df_result[column] = df_result[column].astype(str).replace("'", "", regex=True).replace('\t', '', regex=True).replace('None', '', regex=True).replace('nan', '')
        if column in ['商品金额', '订单应付金额', '运费', '优惠总金额', '平台实际承担优惠金额', '商家实际承担优惠金额',
                      '达人实际承担优惠金额']:
            count = count - 1
            df_result[column] = df_result[column].astype(str).replace(",", "", regex=True)
            df_result[column] = df_result[column].astype(float).replace('nan', '')
        if column in ['商品数量']:
            count = count - 1
            df_result[column] = df_result[column].astype(int)
    if count != 0:
        raise "初始化存在未处理的列"

    dy_df, zb_df = sort(df_result, xiangmufenleibiao)

    if project == '抖音':
        with pd.ExcelWriter(dingdan_to_path) as writer:
            file_write.FileProcessor(df=dy_df, writer=writer).write_file()
    if project == '直播':
        with pd.ExcelWriter(dingdan_to_path) as writer:
            file_write.FileProcessor(df=zb_df, writer=writer).write_file()
