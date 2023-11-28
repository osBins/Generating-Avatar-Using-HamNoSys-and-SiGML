from flask import Flask, render_template, request, send_from_directory, Response
import main
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # Ensure videos directory exists
        if not os.path.exists('videos'):
            os.makedirs('videos')

        # Save the uploaded file to /videos/
        uploaded_file.save(os.path.join('videos', uploaded_file.filename))
        main.convert(os.path.join('videos', uploaded_file.filename))

        with open(os.path.join('static', 'sigml', 'SiGML-output.sigml'), 'r') as f:
            sigml_text = f.read()

        # WRITE CORR. HAMNOSYS
        with open(os.path.join('static', 'sigml', 'hamnosys-generated'), 'r') as f:
            textarea_content = f.read()
    return render_template('index.html', filename=uploaded_file.filename, sigml=sigml_text, textarea_content=textarea_content.encode().decode('unicode_escape'))

@app.route('/videos/<filename>')
def send_file(filename):
    return send_from_directory('videos', filename)

@app.route('/static/js/cwasa.js')
def serve_cwasa_js():
    # Read the contents of 'SiGML-output.sigml' into a string
    with open('./static/sigml/SiGML-output.sigml', 'r') as file:
        new_sigml = file.read()

    # Open 'cwasa.js', read its content into a string, replace the SiGML part with the new SiGML content,
    with open('./static/js/cwasa.js', 'r') as file:
        cwasa_js = file.read()

    # Your original hardcoded SiGML string
    original_sigml = '''<?xml version="1.0" encoding="utf-8"?>
<sigml>
<hns_sign gloss="mug">
<hamnosys_nonmanual>
<hnm_mouthpicture picture="mVg"/>
</hamnosys_nonmanual>
<hamnosys_manual>
<hamfist/> <hamthumbacrossmod/>
<hamextfingerol/> <hampalml/>
<hamshoulders/>
<hamparbegin/> <hammoveu/> <hamarcu/>
<hamreplace/> <hamextfingerul/> <hampalmdl/>
<hamparend/>
</hamnosys_manual>
</hns_sign>
<hns_sign gloss="take">
<hamnosys_nonmanual>
<hnm_mouthpicture picture="te_Ik"/>
</hamnosys_nonmanual>
<hamnosys_manual>
<hamceeall/> <hamextfingerol/> <hampalml/>
<hamlrbeside/> <hamshoulders/> <hamarmextended/>
<hamreplace/> <hamextfingerl/> <hampalml/>
<hamchest/> <hamclose/>
</hamnosys_manual>
</hns_sign>
<hns_sign gloss="i">
<hamnosys_nonmanual>
<hnm_mouthpicture picture="a_I"/>
</hamnosys_nonmanual>
<hamnosys_manual>
<hamfinger2/> <hamthumbacrossmod/>
<hamextfingeril/> <hampalmr/>
<hamchest/> <hamtouch/>
</hamnosys_manual>
</hns_sign>
</sigml>'''

    # Replace the original SiGML string in cwasa_js with the new sigml
    cwasa_js = cwasa_js.replace(original_sigml, new_sigml)

    # Return the modified JavaScript code
    return Response(cwasa_js, mimetype="text/javascript")


if __name__ == "__main__":
    app.run(debug=True)
