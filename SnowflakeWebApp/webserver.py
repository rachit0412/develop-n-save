# Import Packages
from flask import Flask, render_template, request
import pandas as pd
from Snowflakeconnection import sfconnect

# Flask Web Application
app = Flask("my website")


@app.route('/')
def homepage():
    cur = cnx.cursor().execute("select color_name,count(*) from colors group by color_name "
                               "having count(*)>1 "
                               "order by count(*) desc; ")
    rows = pd.DataFrame(cur.fetchall(), columns=['Color name', 'votes'])
    # test dataframe as html
    dfhtml = rows.to_html(index=False)
    return render_template('index.html', dfhtml=dfhtml)


@app.route('/submit')
def submitpage():
    return render_template('submit.html')


@app.route('/thanks4submit', methods=["post"])
def thanks4submit():
    colorname = request.form.get("cname")
    username = request.form.get("uname")
    cnx.cursor().execute("INSERT INTO COLORS(COLOR_UID, COLOR_NAME) " + "SELECT color_uid_seq.nextval, '" + colorname
                         + "'")
    return render_template('thanks4submit.html', colorname=colorname, username=username)


@app.route('/coolcharts')
def coolcharts():
    cur = cnx.cursor().execute("select color_name,count(*) from colors group by color_name order by count(*) desc;")
    data4charts = pd.DataFrame(cur.fetchall(), columns=['Color', 'votes'])
# data4charts.to_csv('datacharts.csv', index=False)
    data4chartsjson = data4charts.to_json(orient='records')
    return render_template('coolcharts.html', data4chartsjson=data4chartsjson)


# Snowflake

cnx = sfconnect()

app.run()
