import os


from flask import Flask, request, redirect, render_template, session, url_for, g, jsonify

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='devIAm')  # Needed for session tracking
  # Note flask does CLIENT session data storage!  Watch data sizes!


@app.route('/', methods=['GET','POST'])
def calculate():
  t = {'a': 0, 'b': 0, 'c': 0}   # josh
  if request.method == 'POST':
    t['a'] = request.form['a']
    t['b'] = request.form['b']
  elif 'a' in request.args:
    t['a'] = request.args.get('a')
    t['b'] = request.args.get('b') 
  t['c'] = int(t['a']) * int(t['b'])

  # Update the number of visits
  # session is a dict which persists.  Stored in client cookie (no local storage)
  if 'times' not in session:
    session['times'] = 0
  session['times'] += 1

  return render_template('index.html', t = t, times = session['times']) # Send t to the template

@app.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('calculate'))  # Calculate is the fn name above!



@app.route('/windchill', methods=['GET','POST'])
def windChill():
  temp = ""
  speed = ""
  chill = None
  tempUnit = None

  if request.method == 'POST':
    # when method is post and a json body is sent, respond with a json object
    if request.headers['Content-type'] == 'application/json':
      calcData = request.get_json()
      temp = float(calcData.get("temp"))
      tempUnit = str(calcData.get("tempUnit"))
      speed = float(calcData.get("speed"))
      speedUnit = str(calcData.get("speedUnit"))
      if speedUnit == "kmh":
        speed = kmhToMph(speed)
      if tempUnit == "c":
        chill = toCelsius(calcWindChill(toFahrenheit(temp), speed))
      else:
        chill = calcWindChill(temp, speed)
      return jsonify(tempUnit=tempUnit, chill = chill)

    temp = float(request.form["temp"])
    tempUnit = str(request.form["tempUnit"])
    speed = float(request.form["speed"])
    speedUnit = str(request.form["speedUnit"])

    if speedUnit == "kmh":
      speed = kmhToMph(speed)

    if tempUnit == "c":
      chill = toCelsius(calcWindChill(toFahrenheit(temp), speed))
    else:
      chill = calcWindChill(temp, speed)
    # if (isC):
    #   chill = toCelsius(calcWindChill(toFahrenheit(float(temp)), float(speed)))
    # else:
    #   chill = calcWindChill(float(temp), float(speed))

  return render_template('windchill.html', temp = temp, speed = speed, chill = chill, tempUnit = tempUnit)


def kmhToMph(kmh):
  return kmh / 1.609

def mphToKmh(mph):
  return mph * 1.60934

def toFahrenheit(celsius):
  return 32 + (celsius * 9.0 / 5.0)

def toCelsius(fahrenheit):
  return (fahrenheit - 32) * 5.0 / 9.0

def calcWindChill(T, Wind):
  return (35.74 + (0.6215 * T) - (35.75 * Wind**0.16) + (0.4275 * T * Wind**0.16))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Enable on all devices so Docker works!