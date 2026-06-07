from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime, timedelta
import os
from zoneinfo import ZoneInfo

PERTH_TZ = ZoneInfo("Australia/Perth")

app = Flask(__name__)

TRANS_PERTH_BASE = "https://www.transperth.wa.gov.au/API/SilverRailRestService/SilverRailService"


HEADERS = {
    'Accept-Charset': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en,en-AU;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'ModuleId': '5310',
    'Origin': 'https://www.transperth.wa.gov.au',
    'Referer': 'https://www.transperth.wa.gov.au/Journey-Planner/Stops-Near-You',
    'RequestVerificationToken': 'ASkCqaFEItbfbf0p0ACZi1_0FXEB4KlOFujkk50UwowkGLrrKXm7Qy9g7hsrCwBn2z1n5A2',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TabId': '141',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Cookie': 'dnn_IsMobile=False; language=en-AU; .ASPXANONYMOUS=8xUsfMcU6gxuncn9k4JgAjmeCG-PLfVqb9JJE4RWI2zI-bzBqLOXKJHMJk39WTNaMGM5xOEW5jciTJGOFHIbfwepiTvMH4q4cfLk8cW22tiAHVGf0; ASP.NET_SessionId=euohfm5blhus5fzwkmnorysz; __RequestVerificationToken=DUcUy1ltMWBnUHmIXWpXb1mHgBgPuXBGR0YKFSqQ2JsYXhoX1L-YBWiCljPawlL-GT0fPg2; TS01a3c144=0169f4a7f2ee180e014c1bf98f383e30d43ff588ef2df2f5142e888e3218f742df8ef7ebd1435b70bfc6ed089ef4a49d04812b9183; _gcl_au=1.1.1258687187.1780819914; _ga=GA1.1.862622410.1780819914; _tt_enable_cookie=1; _ttp=01KTGJ6VS2YY8WTTVWC4VHV2HW_.tt.3; ttcsid=1780819914531::MQhMEaHWN8Sic41XXyhG.1.1780819924537.0::1.-3120.0::0.0.0.0::0.0.0; ttcsid_CNBBHLJC77U3KI9K5FD0=1780819914531::WSLF4ZXMfj-bhRUEqENI.1.1780819924540.1; TScdcd7383027=08eb9c7649ab20008c74f4adb2b71c019332feb72b8449c4051691b9e866533d05741f0ae08536330849f05abc11300043e7f13128770bc823de6d33469f6fb19a41ba8b61c31f26616ad7ad083621a059d690cab6e169406e007dd33a5a1b15; _ga_K2FCMWJJX5=GS2.1.s1780819914$o1$g1$t1780819964$j10$l0$h0'
}

@app.route("/")
def index():
    return render_template("index.html", now=datetime.now(PERTH_TZ).replace(tzinfo=None))


@app.route("/nearby")
def nearby():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Missing lat/lon"}), 400

    url = f"{TRANS_PERTH_BASE}/GetNearbyStopsAsync"
    payload = {
        "GeoCoordinate": f"{lat},{lon}",
        "ReturnPolylineInformation": "false",
        "MaximumDistanceInMetres": "600",
        "MaximumStopsToReturn": "12",
    }

    resp = requests.post(url, data=payload, headers=HEADERS)
    return jsonify(resp.json())


@app.route("/nextbuses")
def nextbuses():
    stop = request.args.get("stop")
    if not stop:
        return jsonify([])

    now = datetime.now(PERTH_TZ).replace(tzinfo=None)

    url = f"{TRANS_PERTH_BASE}/GetStopTimetableAsync"

    payload = {
        'StopNumber': stop,
        'SearchDate': now.strftime('%Y-%m-%d'),
        'SearchTime': now.strftime('%H:%M'),
        'IsRealTimeChecked': 'true',
        'ReturnNoteCodes': 'DV,LM,CM,TC,BG,FG,LK',
        'MaxTripCount': '5'
    }

    try:
        resp = requests.post(url, headers=HEADERS, data=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get("result") != "success":
            print(f"[DEBUG] Stop {stop} -> API failure")
            return jsonify([])

        trips_out = []

        for trip in data.get("trips", []):
            try:
                # --- Values returned by API ---
                display_route = str(trip.get("DisplayRouteCode") or "")
                display_title = str(trip.get("DisplayTripTitle") or "")
                est_arrival = str(trip.get("RealTimeInfo", {}).get("EstimatedArrivalTime") or "")

                countdown = ""

                # --- Countdown calculation (same logic as home()) ---
                if est_arrival:
                    fmt = "%H:%M:%S" if len(est_arrival.split(":")) == 3 else "%H:%M"
                    arrival_dt = datetime.strptime(est_arrival, fmt)

                    # interpret this naive time as Perth local time
                    arrival_dt = arrival_dt.replace(
                        year=now.year, month=now.month, day=now.day
                    )

                    if arrival_dt < now:
                        arrival_dt += timedelta(days=1)

                    seconds_until = int((arrival_dt - now).total_seconds())

                    if seconds_until <= 0:
                        countdown = "departed"
                    else:
                        minutes = round(seconds_until / 60)
                        countdown = f"in {minutes} min"

                # --- Append output ---
                trips_out.append({
                    "DisplayRouteCode": display_route,
                    "DisplayTripTitle": display_title,
                    "ArriveTime": est_arrival,
                    "Countdown": countdown
                })

            except Exception as e:
                print(f"[WARN] Trip parse failed at stop {stop}: {e}")
                continue

        print(f"[DEBUG] Stop {stop} -> {len(trips_out)} trips returned")
        return jsonify(trips_out)

    except Exception as e:
        print(f"[ERROR] Failed to fetch stop {stop}: {e}")
        return jsonify([])
    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)