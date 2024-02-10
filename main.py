from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


def search_db(database_path, table_name, column_name, search_value):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    query = f"SELECT * FROM {table_name} WHERE {column_name} = ?"

    cursor.execute(query, (search_value,))

    row = cursor.fetchone()

    connection.close()

    return row


@app.route('/search/v1', methods=['GET'])
def search_api():
    search_value = request.args.get('search_value')
    if not search_value:
        return jsonify({'error': 'Missing search_value parameter'}), 400

    # Assuming fixed database path, table name, and column name for simplicity
    database_path = 'v1.db'
    table_name = 'COURSELIST'
    column_name = 'COURSEABRV'

    row = search_db(database_path, table_name, column_name, search_value)

    if row:
        # Assuming you know the structure of your row, for example:
        # (COURSEABRV, COURSEFULLNAME, COURSEID, SUBJECTCODE)
        row_dict = {
            'COURSEABRV': row[0],
            'COURSEFULLNAME': row[1],
            'COURSEID': row[2],
            'SUBJECTCODE': row[3],
            # TODO: Note this is static, and needs to be updated
            'TERM': '1244'
        }
        return jsonify(row_dict)
    else:
        return jsonify({'message': 'No matching row found.'}), 404


@app.route('/term', methods=['GET'])
def term_api():
    dict = {
        'TERM': '1244'
    }
    return jsonify(dict)


if __name__ == "__main__":
    app.run(debug=False)
