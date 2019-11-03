from flask import Flask, jsonify
import requests

app = Flask(__name__, static_url_path='/static')

def get_url(**kwargs):
    url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?'
    params = []
    for k, v in kwargs.items():
        if type(v) == list:
            v = '&'.join(v)
        params.append('$' + k + '=' + v)
    return (url + '&'.join(params)).replace(' ', '%20')


@app.route('/get_count_by_borough/<string:borough>', methods=['GET'])
def get_count_by_borough(borough):
    data = requests.get(
        get_url(
            select='count(tree_id) as cnt',
            where=f'lower(boroname)=lower("{borough}")'
        )
    ).json()
    return jsonify(data[0])


@app.route('/get_count_spc_by_borough/<string:borough>', methods=['GET'])
def get_count_spc_by_borough(borough):
    data = requests.get(
        get_url(
            select='spc_common, count(tree_id) as cnt',
            where=f'lower(boroname)=lower("{borough}")',
            group='spc_common',
            order='spc_common',
        )
    ).json()
    return jsonify(data)


@app.route('/get_all_by_borough/<string:borough>', methods=['GET'])
def get_all_by_borough(borough):
    data = requests.get(
        get_url(
            select='*',
            where=f'lower(boroname)=lower("{borough}")'
        )
    ).json()
    return jsonify(data)


@app.route('/complex/<string:word>')
def return_complex(word):
    return jsonify({'complex': word})


if __name__ == '__main__':
    app.run(debug=True)
