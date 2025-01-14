from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

station_details = pd.read_csv('data_small/stations.txt', skiprows=17)
station_details = station_details[
    ['STAID', 'STANAME                                 ']]


@app.route('/')
def home():
    return render_template('home.html', data=station_details.to_html())


@app.route('/api/v1/<station>/<date>/')
def about(station, date):
    file_name = os.path.abspath(
        'data_small/TG_STAID' + str(station).zfill(6) + '.txt')
    df = pd.read_csv(file_name, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {'station': station,
            'date': date,
            'temperature': temperature}


@app.route('/api/v1/<station>/')
def all_data(station):
    file_name = os.path.abspath(
        'data_small/TG_STAID' + str(station).zfill(6) + '.txt')
    df = pd.read_csv(file_name, skiprows=20, parse_dates=["    DATE"])
    return df.to_dict(orient='records')


@app.route('/api/v1/yearly/<station>/<year>/')
def yearly(station, year):
    file_name = os.path.abspath(
        'data_small/TG_STAID' + str(station).zfill(6) + '.txt')
    df = pd.read_csv(file_name, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))]
    return result.to_dict(orient='records')


if __name__ == '__main__':
    app.run(debug=True)
