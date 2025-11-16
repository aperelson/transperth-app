from flask import Flask, render_template, jsonify, request
import requests
import urllib.parse
from datetime import datetime

app = Flask(__name__)

TRANS_PERTH_BASE = "https://www.transperth.wa.gov.au/API/SilverRailRestService/SilverRailService"

@app.route("/")
def index():
    return render_template("index.html", now=datetime.now())

@app.route("/nearby")
def nearby():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Missing lat/lon"}), 400

    url = f"{TRANS_PERTH_BASE}/GetNearbyStops"
    payload = {
        "GeoCoordinate": f"{lat},{lon}",
        "ReturnPolylineInformation": "false",
        "MaximumDistanceInMetres": "500",
        "MaximumStopsToReturn": "8",
    }
    headers = {
        'Accept-Charset': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-AU;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'ModuleId': '5310',
        'Origin': 'https://www.transperth.wa.gov.au',
        'Referer': 'https://www.transperth.wa.gov.au/Journey-Planner/Stops-Near-You',
        'RequestVerificationToken': 'oDKoc33Ff4f48zYdDnDY3mfxEhdIH5b5JRUYjSUv55YXhJ3pytlpXN62r2GNirgRcxbqdw2',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TabId': '141',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Cookie': 'dnn_IsMobile=False; language=en-AU; .ASPXANONYMOUS=TRcrP5IMWa-ReSKSqZ9vKWye6U_xznDh1LaBCqc7m3Bqpel6_WZH0b4VEz4MSvAARHtdS5dAyBX7Ux3XbONqRjChfPrmBUPpr0wvJo0g6t4HWRcu0; Analytics_VisitorId=bdee5299-8878-4d18-8738-ffae3a524773; ASP.NET_SessionId=cp2tvdgcdbti3ryaphkzqegf; __RequestVerificationToken=xEZmGAlGgXuE_ZHELSfsWFpbs-Do0L5i03NFp40gnH27HLkagbC5x5SwhUI6LngO1x35RQ2; _gcl_au=1.1.1819698543.1751687118; _ga=GA1.1.468980649.1751687119; _tt_enable_cookie=1; _ttp=01JZCB0G989GVFNAP0QED3DGQP_.tt.3; .DOTNETNUKE=23D9D97F85F750F82C747D5C61B056DF47F40C010BF6080973C53F392B9AD57FB1B549789A1158AB682838CE5200088B084750ECAB631AC25A4EB268A2BA12251B3ED905EC9159C39C020A8CEBC00FBF8F241290625F4C66688FED0EFEDD9E7197495AE7C0806D0565D0A010E2F057AB1D2D03D00DDB055342BAA0A7; LastPageId=0:267; TS01a3c144=0169f4a7f2c972d28caba2cf0726d4a9f21e2968fc3cbaadf24ea8fc4fd08cfb218b6116a6fea678dd4776fb7e04c38ab33bfcdd57; Analytics=SessionId=a671f38b-1f69-4e5a-a030-2e132ccf8d1a&TabId=141&ContentItemId=-1; _ga_K2FCMWJJX5=GS2.1.s1751687118$o1$g1$t1751690541$j3$l0$h0; ttcsid_CNBBHLJC77U3KI9K5FD0=1751687119145::4S74n5hAHVdc0_m24_DM.1.1751690541241; ttcsid=1751687119145::ojc2hSve6MIOxRyNxGHo.1.1751690541241; TScdcd7383027=08eb9c7649ab2000ef56bd4b034b292f824f794585f3e3259d0c4a3279202424a65a4f517ca4a17f08b2eef3ca113000d792813533c1af21ff837d43dc67a24e9452b9a15fa0542be839a224735698e39bf45617902618acfdf785b1d2d2c735'
    }

    resp = requests.post(url, data=payload, headers=headers)
    return jsonify(resp.json())

@app.route("/nextbuses")
def nextbuses():
    stop = request.args.get("stop")
    if not stop:
        return jsonify([])

    url = f"{TRANS_PERTH_BASE}/GetStopTimetable"
    now = datetime.now()
    
    payload = {
        'StopNumber': stop,
        'SearchDate': now.strftime('%Y-%m-%d'),
        'SearchTime': now.strftime('%H:%M'),
        'IsRealTimeChecked': 'true',
        'ReturnNoteCodes': 'DV,LM,CM,TC,BG,FG,LK',
        'MaxTripCount': '3'
    }

    payload_encoded = urllib.parse.urlencode(payload)

    headers = {
        'Accept-Charset': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-AU;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'ModuleId': '5310',
        'Origin': 'https://www.transperth.wa.gov.au',
        'Referer': 'https://www.transperth.wa.gov.au/Journey-Planner/Stops-Near-You',
        'RequestVerificationToken': 'oDKoc33Ff4f48zYdDnDY3mfxEhdIH5b5JRUYjSUv55YXhJ3pytlpXN62r2GNirgRcxbqdw2',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TabId': '141',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Cookie': 'dnn_IsMobile=False; language=en-AU; .ASPXANONYMOUS=TRcrP5IMWa-ReSKSqZ9vKWye6U_xznDh1LaBCqc7m3Bqpel6_WZH0b4VEz4MSvAARHtdS5dAyBX7Ux3XbONqRjChfPrmBUPpr0wvJo0g6t4HWRcu0; Analytics_VisitorId=bdee5299-8878-4d18-8738-ffae3a524773; ASP.NET_SessionId=cp2tvdgcdbti3ryaphkzqegf; __RequestVerificationToken=xEZmGAlGgXuE_ZHELSfsWFpbs-Do0L5i03NFp40gnH27HLkagbC5x5SwhUI6LngO1x35RQ2; _gcl_au=1.1.1819698543.1751687118; _ga=GA1.1.468980649.1751687119; _tt_enable_cookie=1; _ttp=01JZCB0G989GVFNAP0QED3DGQP_.tt.3; .DOTNETNUKE=23D9D97F85F750F82C747D5C61B056DF47F40C010BF6080973C53F392B9AD57FB1B549789A1158AB682838CE5200088B084750ECAB631AC25A4EB268A2BA12251B3ED905EC9159C39C020A8CEBC00FBF8F241290625F4C66688FED0EFEDD9E7197495AE7C0806D0565D0A010E2F057AB1D2D03D00DDB055342BAA0A7; LastPageId=0:267; TS01a3c144=0169f4a7f2c972d28caba2cf0726d4a9f21e2968fc3cbaadf24ea8fc4fd08cfb218b6116a6fea678dd4776fb7e04c38ab33bfcdd57; Analytics=SessionId=a671f38b-1f69-4e5a-a030-2e132ccf8d1a&TabId=141&ContentItemId=-1; _ga_K2FCMWJJX5=GS2.1.s1751687118$o1$g1$t1751690541$j3$l0$h0; ttcsid_CNBBHLJC77U3KI9K5FD0=1751687119145::4S74n5hAHVdc0_m24_DM.1.1751690541241; ttcsid=1751687119145::ojc2hSve6MIOxRyNxGHo.1.1751690541241; TScdcd7383027=08eb9c7649ab2000ef56bd4b034b292f824f794585f3e3259d0c4a3279202424a65a4f517ca4a17f08b2eef3ca113000d792813533c1af21ff837d43dc67a24e9452b9a15fa0542be839a224735698e39bf45617902618acfdf785b1d2d2c735'
    }

    try:
        resp = requests.post(url, data=payload_encoded, headers=headers)

        print(f"[DEBUG] Stop {stop} -> {resp.status_code}")
        print(f"[DEBUG] Response text: {resp.text[:300]}")

        data = resp.json()
        return jsonify(data.get("Trips", []))
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
