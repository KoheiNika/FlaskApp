import matplotlib.pyplot as plt
import pandas as pd
import os

from matplotlib import font_manager

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.db import get_db

bp = Blueprint('chart', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    db_cursor = db.cursor(buffered=True, dictionary=True)

    db_cursor.execute('DROP TABLE IF EXISTS urltable')
    db.commit()

    # create table, which convert item_name to data_url
    db_cursor.execute('CREATE TABLE IF NOT EXISTS urltable ('
        ' item TEXT NOT NULL,'
        ' url TEXT NOT NULL'
    ')')
    db.commit()

    # insert into table
    # current dir is templates?
    dir_path = os.path.dirname(__file__)
    sample_df = pd.read_csv(dir_path + '\DataBase\品目区分.csv')
    sample_df = sample_df.drop('Unnamed: 0', axis=1)
    sample_series = sample_df['0']
    item_list = sample_series.values.tolist()
    for i in range(len(item_list)):
        path = dir_path + "\\DataBase\\" + item_list[i] + '.csv'
        db_cursor.execute('INSERT IGNORE INTO urltable (item, url)'
            ' VALUES (%s, %s)',
            (item_list[i], path)
            )
        db.commit()

    current_item = 'ボタンから選択してください'
    #return render_template('graph/index.html', items=item_list, current_item=current_item, path=None) # path=Noneでurl_forがエラー
    return redirect(url_for('chart.csv_plot', item=item_list[0]))

@bp.route('/<item>/graph', methods=('GET', 'POST'))
def csv_plot(item):

    dir_path = os.path.dirname(__file__)
    sample_df = pd.read_csv(dir_path + '\DataBase\品目区分.csv')
    sample_df = sample_df.drop('Unnamed: 0', axis=1)
    sample_series = sample_df['0']
    item_list = sample_series.values.tolist()

    abs_path = dir_path + '\\static\\' + item + '.png'
    img_path = item + '.png'

    if os.path.exists(abs_path):
        return render_template('graph/index.html', items=item_list, current_item=item, path=img_path)
    else:
        db = get_db()
        db_cursor = db.cursor(buffered=True, dictionary=True)

        db_cursor.execute('SELECT url FROM urltable WHERE item = %s', (item,))
        dict = db_cursor.fetchone()
        path = dict['url']
        df = pd.read_csv(path)

        font_prop = font_manager.FontProperties(fname=dir_path + "\msgothic.ttc")
        fig, ax = plt.subplots()
        ax2 = ax.twinx()
        columns = df.columns
        index = df[columns[0]]
        ax.set_xticklabels(index, rotation=45, fontdict={"fontproperties": font_prop, "fontsize": 5})
        ax.plot(index, df[columns[1]], marker='o', color="blue", label="関東全体の支出")
        ax2.plot(index, df[columns[2]], marker='x', color="green", label="東京都内感染者数")
        ax2.plot(index, df[columns[3]], marker='^', color="red", label="神奈川県内感染者数")
        ax.set_ylabel("支出", fontdict={"fontproperties": font_prop})
        ax2.set_ylabel("感染者数", fontdict={"fontproperties": font_prop})
        h, l = ax.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax.legend(h+h2, l+l2, prop=font_prop)
        ax.set_title(item, fontdict={"fontproperties": font_prop})
        plt.savefig(abs_path)
        plt.close('all')

        return render_template('graph/index.html', items=item_list, current_item=item, path=img_path)
