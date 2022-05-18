from argparse import ArgumentParser
import glob
import os
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

class ReportParser:
  is_dir = False
  glob_ = None
  def __init__(self, is_dir, glob):
    self.is_dir = is_dir
    self.glob_ = glob
    self.saved_file_path = None
    self.encoding = "utf-8"

  def parse_files(self):
    if self.is_dir:
      self.parse_multiple_files()
    else:
      df = self.parse_one_file(self.glob_[0])
      file_path_save = str(self.glob_[0].split('.')[0]) + ".csv"
      self.save_csv_to_disk(df, file_path_save)
    print('parsing completed')


  def print_file_list(self):
    print('file will be parsed:')
    for file_name in self.glob_ :
      print(file_name)

  def parse_multiple_files(self):
    df_list = []
    for file_name in self.glob_:
      df = self.parse_one_file(file_name)
      df_list.append(df)
    df_concated = pd.concat(df_list, axis=0)

    self.saved_file_path = f'Report_ {datetime.now().strftime("%d %m %Y %H-%M-%S")}.csv'
    self.save_csv_to_disk(df_concated ,self.saved_file_path)

  def parse_one_file(self, file_name):
    html_doc = open(file_name, encoding='utf-8')
    soup = BeautifulSoup (html_doc, "lxml")
    table = soup.find("table", {'class':'vulnerabilitiesTbl'}) 
    rows = table.findAll(lambda tag: tag.name=='tr')

    df = pd.DataFrame()
    row_list = []

    current_number = 0
    row_dict = {}
    for idx, row in enumerate(rows):
      if idx==0:
          continue
      if not row.has_attr('calss'):
        current_number += 1

        bdu = row.find("td", {'class':'bdu'}).text

        risk = row.find("td", {'class':'risk riskTextColor'}).text

        desc = row.find("td", {'class':'desc'}).text


        row_dict['bdu'] = bdu
        row_dict['risk'] = risk
        row_dict['desc'] = desc
      if row.has_attr('calss'):
        filelist_prods = row.find("td", {'class':'fileslist prods'}).text

        file_list_desc = row.find("td", {'class':'desc fileslist'}).text


        row_dict['filelist_prods'] = filelist_prods
        row_dict['file_list_desc'] = file_list_desc

        row_list.append(row_dict)
        row_dict = {}

    df = df.append(row_list)
    return df

  def save_csv_to_disk(self, df, file_name):
    df.to_csv(file_name, encoding="utf-8")

  def fix_multiple_bdu_rows(self, file_name, remove_orig_file=True, only_bdu=True):
    df = pd.read_csv(self.saved_file_path, encoding="utf-8")

    df_idxs = df[df['bdu'].str.len() > 14]['bdu'].index
    bdu_series1 = df[df['bdu'].str.len() > 14]['bdu'].str[:14]
    bdu_series2 = df[df['bdu'].str.len() > 14]['bdu'].str[14:]

    for idx in df_idxs:
      df.loc[idx, 'bdu'] = bdu_series1[idx]

    df_n = df.iloc[df_idxs].copy()

    for idx in df_idxs:
      df_n.loc[idx, 'bdu'] = bdu_series2[idx]

    df = df.append(df_n)
    df = df.drop(df.columns[0],axis=1)

    if only_bdu:
      df = df[['bdu']]

    df.to_csv(file_name, encoding="utf-8", index=False)

    if remove_orig_file:
      os.remove(self.saved_file_path)


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument('file')
  res = parser.parse_args()

  IS_DIR = False
  if os.path.isdir(res.file):
    IS_DIR = True
    glob = glob.glob(res.file + '/*.html')
  else:
    glob = glob.glob(res.file)


  if len(glob) == 0:
    raise ValueError('Incorrect file name or no html file in directory.')

  reportParser = ReportParser(IS_DIR, glob)
  reportParser.print_file_list()
  reportParser.parse_files()
  reportParser.fix_multiple_bdu_rows("report.csv")