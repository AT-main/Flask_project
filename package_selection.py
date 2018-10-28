from flask import Flask, render_template, request, jsonify, make_response
import sqlite3, datetime
app = Flask(__name__)

def log_report(*args, **kwargs):
    if kwargs.get('value', 0):
        with open('logfile.txt','w') as f:
            f.write('Last run: ' + str (datetime.datetime.now()) +'\n\n')
        return
    
    with open('logfile.txt', 'a', encoding='utf8') as log_file:
        count = 1
        for key, value in kwargs['report_dict'].items():
            if type(value) == float:
                txt = '{0:^6} >> {1:^8.2f}|'.format(key, value)
            
            else: txt = '{0:^6} >> {1:^8}|'.format(key, value)
            
            count += 1
            if  not (count % 4): txt += '\n\n'
            log_file.write(txt)
            

@app.route('/package-form/')
def select_package():

    resp = make_response(render_template('package-form.html')) # this line was added only to test make_response functionality
    # resp.set_cookie('UserID', 'No users yet') # cookies can be set using make_response
    return resp

@app.route('/recommend-package', methods = ['POST', 'GET'])
def recommed_package():
    
    if request.method == 'POST':
        form_result = request.form
        
        print (form_result)
        
        db_connect = sqlite3.connect('cities.db')
        cursor = db_connect.cursor()

        cursor.execute('SELECT * FROM Cities WHERE City=?',(form_result['city'],))
        city = cursor.fetchone()

        # for c in city:
        k5 = city[3]
        k6 = city[4]
        _city = city[2]
        print(_city)

        # city.close()

        Ans5 = int(form_result['Ans5'])
        Ans5_list = [0, 1, 1.3, 1.6, 2, 0.8]
        k1 = Ans5_list[Ans5]


        Ans7 = int(form_result['Ans7'])
        if Ans7 == 4: n =0
        else: n = Ans7

        Ans8 = int(form_result['Ans8'])
        if Ans8 == 1 : k2 = 1
        else: k2 = 0.93

        Ans9 = int(form_result['Ans9'])
        if Ans9 == 1 : k3 = 1
        else: k3 = 1.15

        k4 = 1 + (0.02 * k5)
        k7 = 1 + (0.00014 * k6) 

        Area = abs(int(form_result['area']))

        P = int(Area * k1 * k2 * k3 * k4 * 120)
        Q = P + int(n * 12023)
        R = P + int(n * 8516)
        S = P + int(n * 6777)

        if P <= 12000: 
            B = 1.5
        else: 
            B = 0.000122 * P

        c_dict = {'CP36': 36, 'CP45': 45, 'CP65': 65, 'CP85': 85, 'CP125': 125, 'CP160': 160, 'CP200': 200}
        f_dict = {'28000': 27.5, '32000': 31.5, '36000': 35.5, '39000': 38, '45000': 44.5, '50000': 49, '54000': 53}
        h_dict = {'18': 15, '24': 20, '28': 23.5, '32': 27, '36': 30.5, '40': 33.5}
        
        if S > 200000:
            C = ''
            D = 0
        else:
            for key, value in c_dict.items():
                if S <= value * 1000: 
                    C = key
                    D = value * 1000
                    break
        if S > 53000: G = ''
        else:
            for key, value in f_dict.items():
                if S <= value * 1000: 
                    G = key
                    break

        E = 0.000128 * k7 * Q
        
        if R > 53000: F = 0
        else:
            for key, value in f_dict.items():
                if R <= value * 1000: 
                    F = key
                    break
        
        F1 = 0.000119 * k7 * Q
        
        if P > 33500: H = ''
        else:
            for key, value in h_dict.items():
                if P <= value * 1000: 
                    H = key
                    break
        
        if R > 200000: 
            I = ''
            O = 0
        else:
            for key, value in c_dict.items():
                if R <= value * 1000: 
                    I = key
                    O = value * 1000
                    break
        
        J = 0.000128 * k7 * R

        K = 0.000128 * k7 * S

        if Q > 53000: L = ''
        else:
            for key, value in f_dict.items():
                if Q <= value * 1000: 
                    L = key
                    break
        
        if P > 53000: M = ''
        else:
            for key, value in f_dict.items():
                if P <= value * 1000: 
                    M = key
                    break

        Q1 = 0.000119 * k7 * R

        T = 0.000119 * k7 * S

        if P > 200000:
            U = ''
            V = 0
            Z1 = ''
        else:
            for key, value in c_dict.items():
                if P <= value * 1000: 
                    U = key
                    V = value * 1000
                    Z1 = key + '-S'
                    break
        
        W = 0.000122 * P

        X = 0.000128 * k7 * P

        Y1 = k7 * S

        Y2 = k7 * R 

        Y3 = k7 * P

        Z = 0.000119 * k7 * P
    
        Ans1 = int(form_result['Ans1'])
        Ans3 = int(form_result['Ans3'])
        Ans4 = int(form_result['Ans4'])
        Ans7 = int(form_result['Ans7'])

        combi = [Ans4, Ans1, Ans3, Ans7]
        print('combination is', combi)
        
        cursor.execute('SELECT * FROM Combinations WHERE combi=?',(str(combi),))
        combination = cursor.fetchone()
        
        parts = []
        parts.append(eval(combination[2]))
        parts.append(eval(combination[3]))
        parts.append(eval(combination[4]))

        report_list = [ 'Area', '_city',  
                        'Ans1', 'Ans3', 'Ans4', 'Ans5', 'Ans7', 'Ans8', 'Ans9',
                        'k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7',
                        'P', 'Q', 'R', 'S',
                        'B', 'C', 'D', 'E', 'F', 'F1', 'G', 'H', 'I',
                        'J', 'K', 'L', 'M', 'O', 'Q1', 'T', 'U', 'V',
                        'W', 'X', 'Y1', 'Y2', 'Y3', 'Z', 'Z1']

        log_report(value = 'erase')

        report_dict = {}
        for param in report_list:
            report_dict[param] = eval(param)
        
        log_report(report_dict = report_dict)
####################################################################################################
#                                for loops                                                         #
####################################################################################################
        result = []
        for part in parts:
            temp = {}
            print('>>>>> This part includes: ', part, ' <<<<<')
            for text_id in part:
                print('text_id is:', text_id)
                # db_connect = sqlite3.connect('cities.db')
                cursor = db_connect.cursor()
                cursor.execute('SELECT * FROM OutputTexts WHERE id=?',(text_id,))
                text = cursor.fetchone()
                cursor.close()

                content = text[1]
                condition = eval(text[2])
                params = eval(text[3])

                if not (condition):
                    print('condition for text', text_id,':<<' , text[2], '>> is not met')
                    continue

                output_text = content
                for item in params:
                    if type(eval(item)) == str:
                        output_text = output_text.replace(item, eval(item)) +'\n\n\n'
                    else:
                        output_text = output_text.replace(item, str(int(float(eval(item))))) +'\n\n\n'
                
                temp[text_id] =(output_text)
            
            result.append(temp)

        print('number of texts', len(result))
        

        return render_template('recommend-package.html', result = result)
    else:
        return ("{'value':'تهران'}, {'value':'ورامین'},{'value':'کن'}")
    """
----------------------------------------------------------------------------------------------------------------------------    
    """
##############################################################################################################################
@app.route('/states/')
def return_states():
    
    db_connect = sqlite3.connect('cities.db')
    cursor = db_connect.cursor()
    
    cursor.execute('SELECT * FROM States')
    states = cursor.fetchall()
    cursor.close()
    # for state in states:
    #     print(state[0])
    
    stateArray = []
    for state in states:
        stateObj = {}
        stateObj['id'] = state[0]
        stateObj['name'] = state[1]
        stateArray.append(stateObj)

    states_json = jsonify({'states' : stateArray})

    return states_json

@app.route('/cities/<province>/')
def return_cities(province):
    print ('>>> {} <<<'.format(province))
    db_connect = sqlite3.connect('cities.db')
    cursor = db_connect.cursor()
    
    cursor.execute('SELECT * FROM States WHERE id=?',(province,))
    state = cursor.fetchone()[1]

    cursor.execute('SELECT * FROM Cities WHERE State=? ORDER BY Id',(state,))
    cities = cursor.fetchall()
    cursor.close()

    cityArray = []
    for city in cities:
        cityObj = {}
        cityObj['id'] = city[0]
        cityObj['name'] = city[2]
        cityArray.append(cityObj)
    
    cities_json = jsonify({'cities' : cityArray})
    
    return cities_json
    
app.add_url_rule('/','package-form', select_package )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

