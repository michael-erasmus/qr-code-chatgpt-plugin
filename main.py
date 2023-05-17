import json

import quart
import quart_cors
from quart import request, jsonify

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

@app.route('/create-qr-code', methods=['GET'])
async def create_qr_code():
    data = request.args.get('data', '')
    size = request.args.get('size', '100x100')
    alt = request.args.get('alt', '')
    title = request.args.get('title', '')

    img_src = f"https://api.qrserver.com/v1/create-qr-code/?data={data}&size={size}"

    img_tag = f'<img src="{img_src}" alt="{alt}" title="{title}" />'

    return jsonify({'img_tag': img_tag})

@app.get("/qr-logo.png")
async def plugin_logo():
    filename = 'qr-logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
