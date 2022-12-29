import os
import shutil
import zipfile
from io import BytesIO
import glob
import pandas as pd

from random import randint

import streamlit as st
from streamlit import session_state

from run import preprare_to_parse

upload_dir = "./uploaded_files"


def create_upload_dir():
    try:
        shutil.rmtree(upload_dir, ignore_errors=True)
        os.makedirs(upload_dir)
    except FileExistsError:
        os.makedirs(upload_dir, exist_ok=True)


def unpack_zip(bytes_data):
    zipfile.ZipFile(BytesIO(bytes_data)).extractall(upload_dir)


def dowloader_callback():
    pass
    # st.session_state['widget_key'] = str(randint(1000, 100000000))


def get_table_stats(report_name):
    df_report = pd.read_csv(report_name)
    df_to_show = df_report.head(5)
    stats_to_show = df_report['bdu'].value_counts().head(10)
    st.write('Отчет:')
    st.dataframe(df_to_show)
    st.write('Самые распространенные:')
    st.dataframe(stats_to_show)


if __name__ == "__main__":
    st.title('ScanOVAL Converter')

    st.subheader('Загрузите html файлы или zip архив с html файлами')

    if 'widget_key' not in session_state:
        session_state['widget_key'] = str(randint(1000, 100000000))

    uploaded_files = st.file_uploader("Upload", type=['html', 'zip'], accept_multiple_files=True, key=session_state['widget_key'])

    only_bdu = st.checkbox(label='only_bdu', value=False)
    add_date_time = st.checkbox(label='add_date_time', value=True)
    report_name = st.text_input(label="report name", value="report.csv")

    if uploaded_files is not None:
        create_upload_dir()
        for file in uploaded_files:
            file.seek(0)
        if len(uploaded_files) == 1 and uploaded_files[0].type == 'application/x-zip-compressed':
            bytes_data = uploaded_files[0].getvalue()
            unpack_zip(bytes_data)
            glob = glob.glob(upload_dir + '/*.html')
            preprare_to_parse(True, glob, only_bdu, report_name=report_name, add_date_time=add_date_time,
                              remove_orig_file=True)
            st.write('файл конвертирован')
            get_table_stats(report_name)

            with open(report_name, 'rb') as f:
                st.download_button('Download CSV', f, report_name)


        if len(uploaded_files) == 1 and uploaded_files[0].type == 'text/html':
            bytes_data = uploaded_files[0].getvalue()
            with open(os.path.join(upload_dir, uploaded_files[0].name), "wb") as f:
                f.write(bytes_data)

            glob = glob.glob(os.path.join(upload_dir, uploaded_files[0].name))
            # st.session_state['widget_key'] = str(randint(1000, 100000000))
            preprare_to_parse(False, glob, only_bdu, report_name="report.csv", add_date_time=add_date_time,
                              remove_orig_file=True)
            st.write('файл конвертирован')
            get_table_stats(report_name)
            with open(report_name, 'rb') as f:
                st.download_button('Download CSV', f, report_name)
                st.session_state['widget_key'] = str(randint(1000, 100000000))


        if len(uploaded_files) == 1 and (uploaded_files[0].type != 'text/html' and
                                         uploaded_files[0].type != 'application/x-zip-compressed'):
            st.write('Загружен не html file')
        if len(uploaded_files) > 1:
            for file in uploaded_files:
                if file.type != 'text/html':
                    st.write('Загружен не html file')
                else:
                    bytes_data = file.getvalue()
                    with open(os.path.join(upload_dir, file.name), "wb") as f:
                        f.write(bytes_data)
            glob = glob.glob(upload_dir + '/*.html')
            preprare_to_parse(True, glob, only_bdu, report_name=report_name, add_date_time=add_date_time,
                              remove_orig_file=True)
            st.write('файл конвертирован')
            get_table_stats(report_name)
            with open(report_name, 'rb') as f:
                st.download_button('Download CSV', f, report_name, on_click=dowloader_callback)

