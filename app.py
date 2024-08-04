from flask import Flask, render_template, request, jsonify
import pandas as pd
import random

app = Flask(__name__)

# Load and preprocess the Excel file
excel_file_path = "vocab.xlsx"
df = pd.read_excel(excel_file_path)
df_grouped = df.groupby('Word', as_index=False).agg({'Meaning': lambda x: ' | '.join(x)})

@app.route('/')
def index():
    return render_template('index.html', words=df_grouped.to_dict(orient='records'))

@app.route('/shuffle', methods=['POST'])
def shuffle_words():
    start = int(request.form.get('start'))
    end = int(request.form.get('end'))
    if start < 0 or end >= len(df_grouped) or start > end:
        return jsonify({'error': 'Invalid range'}), 400

    subset = df_grouped.iloc[start:end+1].copy()
    shuffled_subset = subset.sample(frac=1).reset_index(drop=True)
    return jsonify(shuffled_subset.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
