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

headers_get = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

@app.route("/estado", methods=["GET"])
def estado():
    res = requests.get(
        f"{SUPABASE_URL}/rest/v1/producao?data_fim=is.null&select=operador,op,produto,tipo,hora_inicio,data_inicio",
        headers=headers_get
    )
    registros = res.json()

    estado = {}
    for r in registros:
        # Horario local salvo sem fuso — envia sem Z para o browser tratar como local
        inicio_iso = f"{r['data_inicio']}T{r['hora_inicio']}"
        estado[r["operador"]] = {
            "op": r["op"],
            "produto": r["produto"],
            "tipo": r["tipo"],
            "inicio": inicio_iso
        }

    return jsonify(estado)

@app.route("/", methods=["POST"])
def salvar():
    data = request.json

    if data["acao"] == "iniciar":
        # Horario local enviado pelo frontend (ex: "2024-04-20T17:50:00")
        inicio = datetime.fromisoformat(data["inicio"])
        payload = {
            "operador": data["operador"],
            "op": data["op"],
            "produto": data["produto"],
            "tipo": data["tipo"],
            "data_inicio": inicio.date().isoformat(),
            "hora_inicio": inicio.strftime("%H:%M:%S")
        }

        res = requests.post(
            f"{SUPABASE_URL}/rest/v1/producao",
            json=payload,
            headers=headers
        )
        print(res.text)

    elif data["acao"] == "concluir":
        # Hora local do servidor — ajustada para horario de Brasilia
        from datetime import timezone, timedelta
        agora = datetime.now(timezone(timedelta(hours=-3)))
        res = requests.patch(
            f"{SUPABASE_URL}/rest/v1/producao?operador=eq.{data['operador']}&data_fim=is.null",
            json={
                "data_fim": agora.date().isoformat(),
                "hora_fim": agora.strftime("%H:%M:%S")
            },
            headers=headers
        )
        print(res.text)

    return jsonify({"ok": True})

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
