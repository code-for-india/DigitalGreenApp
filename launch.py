from flask import Flask, render_template, request, Response, url_for
from flaskext.mysql import MySQL
import MySQLdb
import json
import plivo
import plivoxml

auth_id = 'MANJVHMTE4ODRHODA3ND'
auth_token = 'NGNiNjg5N2RlYzEwNmZjNTFhNzQ2NWFkNDY4OWE4'
 
app = Flask(__name__)

@app.route('/')
def HomePage():
    return render_template('index.html')

@app.route('/list')
def ViewList():
    db=MySQLdb.connect("216.12.194.50","purvotar_root", "root1", "purvotar_cfi")
    cur = db.cursor()
    query = "SELECT * FROM farmersdata"
    cur.execute(query)
    data = cur.fetchall()
    db.close()
    
    html = "<html><style>"
    html += "#hor-minimalist-b{ font-family: 'Lucida Sans Unicode', 'Lucida Grande', Sans-Serif;font-size: 12px;background: #fff;margin: 45px;border-collapse: collapse;text-align: left;}"
    html+="#hor-minimalist-b th{font-size: 16px;font-weight: normal;color: #039;padding: 16px 10px;border-bottom: 2px solid #6678b1;}"
    html+="#hor-minimalist-b td{border-bottom: 1px solid #ccc;color: #669;font-size:12px;padding: 12px 10px;}"
    html+="#hor-minimalist-b tbody tr:hover td{color: #009;}</style>"

    html += "<body><table width='800' id='hor-minimalist-b'><tr><th>Farmer ID</th><th>Farmer Name</th><th>Village Name</th><th>Phone Number</th><th>Block Name</th><th>Interested</th><th>Adopted</th><th> Call Now</th></tr>"
    for row in data:
        html += '<tr>'
        for ele in row:
            col = '<td>'+str(ele)+'</td>'
            html += col
        par = "/call?key="+str(row[3])
        html+="<td><a href='"+par+"'>Call</a></td></tr>"
    html += '</table></body></html>'
    return html

@app.route('/populate', methods=['POST'])
def addEntry():
    '''
    name = request.form['name']
    village = request.form['vilname']
    phno = request.form['phno']
    block = request.form['blockname']
    '''
    a = request.form['name']
    b = request.form['vilname']
    c = request.form['phno']
    d = request.form['blockname']
    video_id = request.form['videoID']
    video_titles = request.form['videoTitles']

    db=MySQLdb.connect("216.12.194.50","purvotar_root", "root1", "purvotar_cfi")
    cur = db.cursor()
    sql = "INSERT INTO farmersdata(farmerid,name,villagename,phone,blockname) VALUES (null,'"+str(a)+"','"+str(b)+"','"+str(c)+"','"+str(d)+"')"
    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print "Problem inserting a row"
    db.close()
    return "<html><head><meta http-equiv='refresh' content='2;URL=\"http://fathomless-inlet-8852.herokuapp.com/\"'></head><body><center><h2>New entry added</h2></center></body></html>"

@app.route('/call',methods=['GET'])
def make_call():
    p = plivo.RestAPI(auth_id,auth_token)
    params = {'from':'919242733911', 'to':request.args.get('key', '') , 'answer_url' : 'http://fathomless-inlet-8852.herokuapp.com/answer'}
    response = p.make_call(params)
    return "<html><head><meta http-equiv='refresh' content='2;URL=\"http://fathomless-inlet-8852.herokuapp.com/list\"'></head><body><center><h2>Call is being made. Please wait while we connect you to the farmer</h2></center></body></html>"
    db.commit()

@app.route('/answer', methods=['GET','POST'])
def ivr():
    '''
    text = 'Hello, you have recently watched S R I technique videos'
    response = plivoxml.Response()
    params = {'loop':1,'language':"en-US", 'voice':'WOMAN'}
    response.addSpeak(text,**params)
    return Response(str(response), mimetype='text/xml')
    '''
    response = plivoxml.Response()
    if request.method == 'GET':
        getdigits_action_url = url_for('ivr', _external=True)
        getDigits = plivoxml.GetDigits(action=getdigits_action_url, method='POST',timeout=7, numDigits=1, retries=1)
        getDigits.addSpeak("Welcome to the Plivo IVR Demo App. Press 1 to hear a random joke. Press 2 to listen to a song.")
        response.add(getDigits)
        response.addSpeak("Sorry, I didn't catch that. Please hangup and try again later.")
        return Response(str(response), mimetype='text/xml')
    elif request.method == 'POST':
        digit = request.form.get('Digits')
        if digit == "1":
            # Fetch a random joke using the Reddit API.
            print "Got the digit one"    
        elif digit == "2":
            # Listen to a song
            print "Got the digit two"
        else:
            response.addSpeak("Sorry, it's wrong input.")
        
        return Response(str(response), mimetype='text/xml')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print port
    app.run(host='0.0.0.0',port=port)
