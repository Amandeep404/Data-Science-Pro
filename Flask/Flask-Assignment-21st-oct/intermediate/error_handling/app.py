from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get input values from the form
        num1 = float(request.form.get('num1'))
        num2 = float(request.form.get('num2'))

        # Perform the calculation (for example, addition)
        result = num1 + num2

        # Return the result as JSON
        return jsonify({'result': result})

    except Exception as e:
        # Log other exceptions for debugging purposes
        app.logger.error(str(e))
        # Return an internal server error response
        return jsonify({'error': 'Internal Server Error'}), 500
     

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)  
