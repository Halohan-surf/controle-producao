from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

SUPABASE_URL = "COLE_SUA_URL_AQUI"
SUPABASE_KEY = "COLE_SUA_API_KEY_AQUI"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
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

        requests.post(f"{SUPABASE_URL}/rest/v1/producao", json=payload, headers=headers)

    elif data["acao"] == "concluir":
        # Atualiza o último registro sem fim
        requests.patch(
            f"{SUPABASE_URL}/rest/v1/producao?operador=eq.{data['operador']}&data_fim=is.null",
            json={
                "data_fim": agora.date().isoformat(),
                "hora_fim": agora.time().isoformat()
            },
            headers=headers
        )

    return jsonify({"ok": True})

app.run(host="0.0.0.0", port=5000)