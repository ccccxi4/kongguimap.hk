import requests
import json
import time
from math import radians, sin, cos, sqrt, atan2

API_KEY = "AIzaSyDhPLeG5lR8yHeyRNRp-2j-QY3OY1E2lEE"

# 深水埗、油麻地/佐敦區域待驗證餐廳
RESTAURANTS = [
  # ===== 深水埗 =====
  {"id":201,"name":"劉森記蝦籽麵","type":"粥粉麵","address":"深水埗桂林街48號","lat":22.3305,"lng":114.1620,"price":45,"rating":4.4},
  {"id":202,"name":"公和荳品廠","type":"小吃","address":"深水埗北河街118號","lat":22.3280,"lng":114.1605,"price":20,"rating":4.3},
  {"id":203,"name":"維記咖啡粉麵","type":"茶餐廳","address":"深水埗福華街62號","lat":22.3310,"lng":114.1630,"price":40,"rating":4.2},
  {"id":204,"name":"合益泰小食","type":"小吃","address":"深水埗桂林街121號","lat":22.3295,"lng":114.1615,"price":15,"rating":4.5},
  {"id":205,"name":"新香園堅記","type":"茶餐廳","address":"深水埗桂林街38號","lat":22.3300,"lng":114.1618,"price":38,"rating":4.3},
  {"id":206,"name":"文記車仔麵","type":"粥粉麵","address":"深水埗福榮街109號","lat":22.3315,"lng":114.1625,"price":40,"rating":4.4},
  {"id":207,"name":"增輝藝廚","type":"中菜","address":"深水埗石硤尾街31號","lat":22.3285,"lng":114.1595,"price":45,"rating":4.1},
  {"id":208,"name":"鴨寮街熟食中心","type":"快餐","address":"深水埗鴨寮街","lat":22.3290,"lng":114.1600,"price":35,"rating":4.0},
  {"id":209,"name":"麥當勞 深水埗店","type":"快餐","address":"深水埗欽州街37號","lat":22.3288,"lng":114.1598,"price":35,"rating":3.5},
  {"id":210,"name":"大家樂 深水埗店","type":"快餐","address":"深水埗長沙灣道264號","lat":22.3318,"lng":114.1635,"price":42,"rating":3.6},
  
  # ===== 油麻地 =====
  {"id":211,"name":"麥文記麵家","type":"雲吞麵","address":"油麻地白加士街51號","lat":22.3065,"lng":114.1710,"price":45,"rating":4.3},
  {"id":212,"name":"澳洲牛奶公司","type":"茶餐廳","address":"佐敦白加士街47號","lat":22.3060,"lng":114.1705,"price":35,"rating":4.2},
  {"id":213,"name":"義順牛奶公司","type":"茶餐廳","address":"油麻地庇利金街63號","lat":22.3070,"lng":114.1715,"price":35,"rating":4.0},
  {"id":214,"name":"美都餐室","type":"茶餐廳","address":"廟街63號","lat":22.3080,"lng":114.1700,"price":45,"rating":4.1},
  {"id":215,"name":"興記煲仔飯","type":"中菜","address":"油麻地廟街15號","lat":22.3090,"lng":114.1695,"price":50,"rating":4.3},
  {"id":216,"name":"佳佳甜品","type":"甜品","address":"佐敦寧波街29號","lat":22.3055,"lng":114.1700,"price":25,"rating":4.4},
  {"id":217,"name":"麥當勞 油麻地店","type":"快餐","address":"油麻地彌敦道473號","lat":22.3075,"lng":114.1718,"price":35,"rating":3.5},
  {"id":218,"name":"大快活 油麻地店","type":"快餐","address":"油麻地彌敦道480號","lat":22.3080,"lng":114.1720,"price":40,"rating":3.6},
  {"id":219,"name":"翠華餐廳 油麻地店","type":"茶餐廳","address":"油麻地碧街45號","lat":22.3068,"lng":114.1708,"price":48,"rating":3.9},
  {"id":220,"name":"富記粥品","type":"粥品","address":"油麻地廟街","lat":22.3085,"lng":114.1698,"price":40,"rating":4.2},
]

def calc_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))

def verify_restaurant(r):
    search_query = f"{r['name']} {r['address']} Hong Kong"
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": search_query,
        "inputtype": "textquery",
        "fields": "place_id,name,formatted_address,geometry,rating,business_status",
        "locationbias": f"point:{r['lat']},{r['lng']}",
        "key": API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("candidates"):
            c = data["candidates"][0]
            loc = c.get("geometry", {}).get("location", {})
            if loc:
                dist = calc_distance(r["lat"], r["lng"], loc["lat"], loc["lng"])
                return {
                    "id": r["id"], "name": r["name"], "verified": True,
                    "api_name": c.get("name"), "distance_m": round(dist, 1),
                    "status": c.get("business_status", "UNKNOWN"),
                    "place_id": c.get("place_id"),
                    "api_lat": loc["lat"], "api_lng": loc["lng"]
                }
        return {"id": r["id"], "name": r["name"], "verified": False, "reason": "No match"}
    except Exception as e:
        return {"id": r["id"], "name": r["name"], "verified": False, "reason": str(e)}

print("开始验证深水埗、油麻地区域餐厅数据...")
verified, failed = [], []

for r in RESTAURANTS:
    result = verify_restaurant(r)
    if result["verified"]:
        verified.append(result)
        icon = "✅" if result.get("status") == "OPERATIONAL" else "⚠️"
        print(f"{icon} {r['name']} - 偏差: {result.get('distance_m', 'N/A')}m")
    else:
        failed.append(result)
        print(f"❌ {r['name']} - {result.get('reason', 'Unknown')}")
    time.sleep(0.1)

print(f"\n=== 结果 ===")
print(f"✅ 通过: {len(verified)} | ❌ 失败: {len(failed)}")

if failed:
    print("\n失败列表:")
    for f in failed:
        print(f"  - {f['name']}")

with open("verification_result_ssp_yau.json", "w", encoding="utf-8") as f:
    json.dump({"verified": verified, "failed": failed}, f, ensure_ascii=False, indent=2)
print("\n结果已保存到 verification_result_ssp_yau.json")
