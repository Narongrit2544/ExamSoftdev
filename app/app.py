from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "ExamSoftdev Success!!!!!"

@app.route('/is_prime/<number>',methods=['GET'])
def show_number(number):
    # แปลงค่าจาก string เป็น int
    number = int(number)

    if number <= 1:
        return 'False'
    
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return 'False'
    
    return 'True'

if __name__ == '__main__':
    app.run(debug=True)
