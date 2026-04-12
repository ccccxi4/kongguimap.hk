import requests
import json
import time
from math import radians, sin, cos, sqrt, atan2

API_KEY = "AIzaSyDhPLeG5lR8yHeyRNRp-2j-QY3OY1E2lEE"

# 港島其他區域待驗證餐廳（灣仔、上環、北角、筲箕灣等）
RESTAURANTS = [
  # ===== 灣仔 =====
  {"id":101,"name":"華星冰室 灣仔店","type":"茶餐廳","address":"克街6號廣生行大廈地下B1舖","lat":22.2775,"lng":114.1720,"price":45,"rating":4.3},
  {"id":102,"name":"一樂燒鵝 灣仔店","type":"燒臘","address":"軒尼詩道194-204號","lat":22.2780,"lng":114.1750,"price":50,"rating":4.4},
  {"id":103,"name":"金鳳茶餐廳","type":"茶餐廳","address":"春園街41號","lat":22.2760,"lng":114.1710,"price":40,"rating":4.0},
  {"id":104,"name":"麥奀雲吞麵世家 灣仔店","type":"雲吞麵","address":"莊士敦道45號","lat":22.2765,"lng":114.1700,"price":48,"rating":4.2},
  {"id":105,"name":"再興燒臘飯店","type":"燒臘","address":"軒尼詩道265-267號","lat":22.2785,"lng":114.1770,"price":42,"rating":4.1},
  {"id":106,"name":"檀島咖啡餅店 灣仔店","type":"茶餐廳","address":"軒尼詩道176-178號","lat":22.2778,"lng":114.1745,"price":45,"rating":4.0},
  {"id":107,"name":"靠得住 灣仔店","type":"粥粉麵","address":"莊士敦道142號","lat":22.2762,"lng":114.1705,"price":48,"rating":4.3},
  {"id":108,"name":"車仔麵之家","type":"粥粉麵","address":"灣仔道177-179號","lat":22.2770,"lng":114.1725,"price":38,"rating":3.9},
  
  # ===== 上環 =====
  {"id":109,"name":"瑞記咖啡","type":"茶餐廳","address":"上環市政大廈2樓","lat":22.2865,"lng":114.1505,"price":35,"rating":4.2},
  {"id":110,"name":"九記牛腩","type":"粥粉麵","address":"歌賦街21號","lat":22.2845,"lng":114.1520,"price":50,"rating":4.5},
  {"id":111,"name":"蘭芳園 上環店","type":"茶餐廳","address":"干諾道中168-200號","lat":22.2870,"lng":114.1510,"price":42,"rating":4.3},
  {"id":112,"name":"生記粥品專家 上環店","type":"粥品","address":"畢街7-9號","lat":22.2855,"lng":114.1515,"price":40,"rating":4.4},
  {"id":113,"name":"蓮香樓","type":"點心","address":"威靈頓街160-164號","lat":22.2840,"lng":114.1540,"price":48,"rating":4.1},
  {"id":114,"name":"麥奀雲吞麵世家 上環店","type":"雲吞麵","address":"威靈頓街77號","lat":22.2842,"lng":114.1535,"price":48,"rating":4.2},
  {"id":115,"name":"陳意齋","type":"茶餐廳","address":"皇后大道中176B號","lat":22.2850,"lng":114.1525,"price":40,"rating":4.0},
  {"id":116,"name":"德輔道西熟食中心","type":"快餐","address":"德輔道西246-248號","lat":22.2875,"lng":114.1470,"price":35,"rating":3.8},
  
  # ===== 北角 =====
  {"id":117,"name":"鳳城酒家 北角店","type":"點心","address":"英皇道395號僑冠大廈","lat":22.2905,"lng":114.2000,"price":48,"rating":4.2},
  {"id":118,"name":"東寶小館","type":"中菜","address":"渣華道99號渣華道市政大廈2樓","lat":22.2920,"lng":114.1980,"price":45,"rating":4.3},
  {"id":119,"name":"麥奀雲吞麵世家 北角店","type":"雲吞麵","address":"英皇道432號","lat":22.2910,"lng":114.2020,"price":48,"rating":4.1},
  {"id":120,"name":"德興茶餐廳","type":"茶餐廳","address":"北角道15號","lat":22.2900,"lng":114.1970,"price":38,"rating":3.9},
  {"id":121,"name":"大利茶餐廳","type":"茶餐廳","address":"春秧街48號","lat":22.2915,"lng":114.1990,"price":40,"rating":4.0},
  {"id":122,"name":"明苑粉麵茶餐廳","type":"粥粉麵","address":"書局街29號","lat":22.2925,"lng":114.2005,"price":35,"rating":3.8},
  {"id":123,"name":"新釗記","type":"粥粉麵","address":"七姊妹道118號","lat":22.2930,"lng":114.2010,"price":38,"rating":4.0},
  {"id":124,"name":"麥當勞 北角店","type":"快餐","address":"英皇道416-426號","lat":22.2918,"lng":114.2030,"price":35,"rating":3.5},
  
  # ===== 筲箕灣 =====
  {"id":125,"name":"王林記潮洲魚蛋粉","type":"粥粉麵","address":"筲箕灣東大街10號","lat":22.2785,"lng":114.2290,"price":40,"rating":4.4},
  {"id":126,"name":"筲箕灣東大街熟食中心","type":"快餐","address":"筲箕灣東大街","lat":22.2780,"lng":114.2285,"price":35,"rating":4.0},
  {"id":127,"name":"金華冰廳 筲箕灣店","type":"茶餐廳","address":"筲箕灣道57-87號","lat":22.2790,"lng":114.2300,"price":42,"rating":3.9},
  {"id":128,"name":"安利魚蛋粉麵","type":"粥粉麵","address":"筲箕灣東大街22號","lat":22.2782,"lng":114.2288,"price":38,"rating":4.1},
  {"id":129,"name":"德昌魚蛋粉","type":"粥粉麵","address":"筲箕灣道84號","lat":22.2788,"lng":114.2295,"price":40,"rating":4.2},
  {"id":130,"name":"太興燒味餐廳 筲箕灣店","type":"燒臘","address":"筲箕灣道111號","lat":22.2795,"lng":114.2310,"price":45,"rating":4.0},
  {"id":131,"name":"麥當勞 筲箕灣店","type":"快餐","address":"筲箕灣道57-87號太安樓","lat":22.2792,"lng":114.2305,"price":35,"rating":3.5},
  {"id":132,"name":"東大街小食","type":"小吃","address":"筲箕灣東大街30號","lat":22.2783,"lng":114.2292,"price":25,"rating":4.0},
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
                    "place_id": c.get("place_id")
                }
        return {"id": r["id"], "name": r["name"], "verified": False, "reason": "No match"}
    except Exception as e:
        return {"id": r["id"], "name": r["name"], "verified": False, "reason": str(e)}

print("开始验证餐厅数据...")
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

with open("verification_result.json", "w", encoding="utf-8") as f:
    json.dump({"verified": verified, "failed": failed}, f, ensure_ascii=False, indent=2)
print("\n结果已保存")
