import os


from flask import Flask, request, redirect, render_template, session, url_for, g

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
  chill = ""
  isF = True
  isC = False

  if request.method == 'POST':
    temp = request.form['temp']
    speed = request.form['speed']
    isF = request.form.get('unitF')
    isC = request.form.get('unitC')
    if (isC):
      chill = toCelsius(calcWindChill(toFahrenheit(float(temp)), float(speed)))
    else:
      chill = calcWindChill(float(temp), float(speed))

  return render_template('windchill.html', temp = temp, speed = speed, chill = chill, isF = isF, isC = isC)


def mphToMetersPerSec(mph):
  return 0.44704 * mph

def mpsToMph(mps): 
  return 2.23694 * mps

def ktsToMph(kts):
  return 1.1507794 * kts

def toFahrenheit(celsius):
  return 32 + (celsius * 9.0 / 5.0)

def toCelsius(fahrenheit):
  return (fahrenheit - 32) * 5.0 / 9.0

def calcWindChill(T, Wind):
  return (35.74 + (0.6215 * T) - (35.75 *   Wind**0.16) + (0.4275 * T * Wind**0.16))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Enable on all devices so Docker works!