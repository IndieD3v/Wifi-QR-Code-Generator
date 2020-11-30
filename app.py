from base64 import b64encode
from io import BytesIO

from wifi_qrcode_generator import wifi_qrcode
from flask import Flask, abort, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
  return render_template("Pages/index.html")


@app.route('/result', methods=["POST"])
def result():
  if 'ssid' in request.form and 'password' in request.form and 'encryption' in request.form:
    ssid = request.form.get("ssid")
    password = request.form.get("password")
    encryption = request.form.get("encryption")
  else:
    abort(404)
  hidden = request.form.get("hidden", default=False)
  if hidden == "on":
    hidden = True

  qr_code = wifi_qrcode(
      ssid, hidden, encryption, password
  )

  output = BytesIO()
  qr_code.save(output, "PNG")
  image = output.getvalue()
  output.close()
  image = str(b64encode(image))[2:-1]
  return render_template("Pages/result.min.html", image=image)


@app.route("/sitemap.xml")
def sitemap():
  return render_template("sitemap.xml")


@app.route("/google5c02155bdaa39045.html")
def google_verification():
  return render_template("google5c02155bdaa39045.html")


if __name__ == '__main__':
  app.env = "development"
  app.run(debug=True)
