import requests
import json
import time
from math import radians, sin, cos, sqrt, atan2

API_KEY = "AIzaSyDhPLeG5lR8yHeyRNRp-2j-QY3OY1E2lEE"

RESTAURANTS = [
  {"id":301,"name":"蘭芳園 尖沙咀店","type":"茶餐廳","address":"尖沙咀重慶大廈地庫","lat":22.2990,"lng":114.1720,"price":42,"rating":4.0},
  {"id":302,"name":"澳門茶餐廳","type":"茶餐廳","address":"尖沙咀樂道40號","lat":22.2980,"lng":114.1715,"price":45,"rating":4.1},
  {"id":303,"name":"池記雲吞麵","type":"雲吞麵","address":"尖沙咀樂道52號","lat":22.2975,"lng":114.1710,"price":48,"rating":4.2},
  {"id":304,"name":"麥當勞 尖沙咀店","type":"快餐","address":"尖沙咀北京道65號","lat":22.2985,"lng":114.1718,"price":35,"rating":3.5},
  {"id":305,"name":"大家樂 尖沙咀店","type":"快餐","address":"尖沙咀彌敦道36號","lat":22.2990,"lng":114.1722,"price":42,"rating":3.6},
  {"id":306,"name":"華嫂冰室 尖沙咀店","type":"茶餐廳","address":"尖沙咀棉登徑8號","lat":22.2982,"lng":114.1730,"price":45,"rating":4.3},
  {"id":307,"name":"星座冰室","type":"茶餐廳","address":"尖沙咀金馬倫道16號","lat":22.2998,"lng":114.1735,"price":40,"rating":4.0},
  {"id":308,"name":"金華冰廳 太子店","type":"茶餐廳","address":"太子弼街47號","lat":22.3250,"lng":114.1685,"price":42,"rating":3.9},
  {"id":309,"name":"一點心 太子店","type":"點心","address":"太子通菜街209A","lat":22.3255,"lng":114.1690,"price":48,"rating":4.3},
  {"id":310,"name":"麥當勞 太子店","type":"快餐","address":"太子彌敦道750號","lat":22.3245,"lng":114.1680,"price":35,"rating":3.5},
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

print("验证尖沙咀、太子區域餐厅...")
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

with open("verification_result_tst.json", "w", encoding="utf-8") as f:
    json.dump({"verified": verified, "failed": failed}, f, ensure_ascii=False, indent=2)
print("结果已保存")
