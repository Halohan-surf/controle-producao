from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

SUPABASE_URL = "https://smanlyoipirfhcvutlqg.supabase.co"
SUPABASE_KEY = "sb_publishable_nO9vSD_XchdmUFcQwZMEfQ_1DCLIyTw"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

@app.route("/", methods=["POST"])
def salvar():
    data = request.json
    agora = datetime.now()

    if data["acao"] == "iniciar":
        payload = {
            "operador": data["operador"],
            "op": data["op"],
            "produto": data["produto"],
            "tipo": data["tipo"],
            "data_inicio": agora.date().isoformat(),
            "hora_inicio": agora.time().isoformat()
        }

        res = requests.post(
            f"{SUPABASE_URL}/rest/v1/producao",
            json=payload,
            headers=headers
        )
        print(res.text)

    elif data["acao"] == "concluir":
        res = requests.patch(
            f"{SUPABASE_URL}/rest/v1/producao?operador=eq.{data['operador']}&data_fim=is.null",
            json={
                "data_fim": agora.date().isoformat(),
                "hora_fim": agora.time().isoformat()
            },
            headers=headers
        )
        print(res.text)

    return jsonify({"ok": True})

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
