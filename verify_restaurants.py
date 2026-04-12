import requests
import json
import time
from math import radians, sin, cos, sqrt, atan2

API_KEY = "AIzaSyDhPLeG5lR8yHeyRNRp-2j-QY3OY1E2lEE"

RESTAURANTS = [
  {"id":1,"name":"Yee Kee Restaurant 怡記餐廳","type":"茶餐廳","address":"士美菲路12S-12T號","lat":22.2804602,"lng":114.1293146,"price":40,"rating":4.2},
  {"id":2,"name":"Ho Ho Restaurant 好好餐廳","type":"茶餐廳","address":"卑路乍街136-142號","lat":22.2821097,"lng":114.1269981,"price":42,"rating":3.9},
  {"id":3,"name":"Sing Kee Restaurant 勝記餐廳","type":"茶餐廳","address":"士美菲路12號","lat":22.2816977,"lng":114.1285481,"price":38,"rating":3.7},
  {"id":4,"name":"Sun Hing Restaurant 新興食家","type":"茶餐廳","address":"士美菲路8號","lat":22.2829508,"lng":114.1282447,"price":45,"rating":4.3},
  {"id":5,"name":"McDonald's 麥當勞 (士美菲路)","type":"快餐","address":"士美菲路12F號宏光閣地下","lat":22.2821823,"lng":114.1284249,"price":35,"rating":3.4},
  {"id":6,"name":"McDonald's 麥當勞 (卑路乍街)","type":"快餐","address":"卑路乍街8號The Westwood","lat":22.2856032,"lng":114.1329466,"price":35,"rating":3.4},
  {"id":7,"name":"Pici","type":"意大利菜","address":"加多近街45-55號翰宇大廈地下5-9號舖","lat":22.2817380,"lng":114.1264158,"price":50,"rating":4.8},
  {"id":8,"name":"Thairos Thai Food","type":"泰國菜","address":"厚和街6-18號","lat":22.2827905,"lng":114.1277828,"price":45,"rating":4.4},
  {"id":9,"name":"BRESOLA","type":"西餐","address":"吉席街78-86號裕安大廈地下","lat":22.2830246,"lng":114.1269493,"price":50,"rating":4.6},
  {"id":10,"name":"Twelve Flavors 十二味","type":"中菜","address":"卑路乍街13號珍珠閣地下2-4號舖","lat":22.2843917,"lng":114.1312318,"price":50,"rating":4.8},
  {"id":51,"name":"康記粉麵","type":"粥粉麵","address":"皇后大道西425號","lat":22.2861562,"lng":114.1360696,"price":38,"rating":4.2},
  {"id":52,"name":"Junels Restobar","type":"菲律賓菜","address":"安寧里7號地下1G","lat":22.2867036,"lng":114.1386439,"price":45,"rating":4.4},
  {"id":53,"name":"Happiness Single Coffee","type":"咖啡廳","address":"英華台1-6號華輝閣","lat":22.2847881,"lng":114.1424969,"price":40,"rating":4.6},
  {"id":54,"name":"Kam Cheung Spare Ribs Noodle 金祥排骨麵","type":"粥粉麵","address":"德輔道西316號地下C舖","lat":22.2871675,"lng":114.1387987,"price":42,"rating":4.3},
  {"id":55,"name":"Hong Lok Restaurant 康樂餐廳","type":"茶餐廳","address":"第一街102號地下","lat":22.2865097,"lng":114.1406645,"price":40,"rating":4.0},
  {"id":56,"name":"Hainan (First Street)","type":"海南雞","address":"第一街55B地下","lat":22.2865948,"lng":114.1424513,"price":45,"rating":4.4},
  {"id":57,"name":"Chiuchownese Noodle Shop 潮州麵店","type":"粥粉麵","address":"正街6-14號","lat":22.2882634,"lng":114.1422643,"price":38,"rating":4.2},
  {"id":58,"name":"Luen Wah Cafe 聯華茶餐廳","type":"茶餐廳","address":"正街28號","lat":22.2873957,"lng":114.1422143,"price":40,"rating":3.7},
  {"id":59,"name":"Po Kee BBQ Restaurant 寶記燒臘","type":"燒臘","address":"皇后大道西425號","lat":22.2860481,"lng":114.1362712,"price":42,"rating":4.0},
  {"id":60,"name":"Modern Fast Food 現代快餐","type":"快餐","address":"干諾道西168號","lat":22.2878983,"lng":114.1385611,"price":35,"rating":4.0},
  {"id":61,"name":"Chung Kee Congee 忠記粥品","type":"粥粉麵","address":"軒尼詩道432-436號地下7鋪","lat":22.2792783,"lng":114.1815653,"price":35,"rating":3.8},
  {"id":62,"name":"Chiu Hing Restaurant 超興粉麵","type":"粥粉麵","address":"謝斐道481號","lat":22.2811251,"lng":114.1825737,"price":38,"rating":3.6},
  {"id":63,"name":"Wing Kee Noodle 榮記粉麵","type":"粥粉麵","address":"糖街15-23號銅鑼灣中心地下1-2號","lat":22.2800381,"lng":114.1867358,"price":40,"rating":3.9},
  {"id":64,"name":"肥仔記麵家 (銅鑼灣)","type":"粥粉麵","address":"福興里40號地舖","lat":22.2793448,"lng":114.1849976,"price":38,"rating":3.4},
  {"id":65,"name":"Cafe de Coral 大家樂 (銅鑼灣)","type":"快餐","address":"軒尼詩道489號","lat":22.2797994,"lng":114.1829961,"price":42,"rating":3.6},
  {"id":66,"name":"Habibs Middle Eastern","type":"中東菜","address":"電氣道83號地下","lat":22.2848458,"lng":114.1914735,"price":48,"rating":4.3},
  {"id":67,"name":"Angus Cafe Angus茶餐廳","type":"茶餐廳","address":"宏安道14-28號","lat":22.2882304,"lng":114.1918253,"price":45,"rating":4.2},
  {"id":68,"name":"Dragon City Cafe 龍城茶餐廳","type":"茶餐廳","address":"謝斐道500號偉安商業大廈地下","lat":22.2809290,"lng":114.1831586,"price":40,"rating":3.5},
  {"id":69,"name":"McDonald's 麥當勞 (怡和街)","type":"快餐","address":"怡和街46-54號","lat":22.2795320,"lng":114.1859030,"price":35,"rating":3.7},
  {"id":70,"name":"Bánh Mì Kitchen","type":"越南菜","address":"利源東街22號","lat":22.2828079,"lng":114.1563254,"price":45,"rating":4.1},
  {"id":71,"name":"New Forest Restaurant 新森林","type":"茶餐廳","address":"威靈頓街99號威華商業中心","lat":22.2838663,"lng":114.1540003,"price":42,"rating":3.7},
  {"id":72,"name":"Wang Fu 王府餃子","type":"餃子","address":"威靈頓街168號","lat":22.2844975,"lng":114.1533121,"price":48,"rating":4.2},
  {"id":73,"name":"Tsim Chai Kee Noodle 沾仔記 (威靈頓街)","type":"雲吞麵","address":"威靈頓街98號地下B舖","lat":22.2829758,"lng":114.1544256,"price":40,"rating":4.0},
  {"id":74,"name":"To Good (Central)","type":"茶餐廳","address":"吉士笠街4號","lat":22.2846228,"lng":114.1539539,"price":42,"rating":4.1},
  {"id":75,"name":"Tsim Chai Kee Noodle 沾仔記 (皇后大道中)","type":"雲吞麵","address":"皇后大道中153號","lat":22.2846853,"lng":114.1537465,"price":40,"rating":4.0},
  {"id":76,"name":"Home.dumpling","type":"餃子","address":"利源東街25號地下","lat":22.2826374,"lng":114.1561985,"price":45,"rating":4.5},
  {"id":77,"name":"Sing Heung Yuen 勝香園","type":"茶餐廳","address":"美輪街2號","lat":22.2840960,"lng":114.1525891,"price":40,"rating":4.0},
  {"id":78,"name":"Tim Ho Wan (Central) 添好運","type":"點心","address":"香港站1樓12A-12B舖","lat":22.2845094,"lng":114.1581426,"price":50,"rating":4.5},
  {"id":79,"name":"Samdor Noodle 三多麵店","type":"粉麵","address":"砵典乍街28號","lat":22.2831673,"lng":114.1557471,"price":38,"rating":4.2},
  {"id":80,"name":"Small Rainy Day 小雨天","type":"台灣菜","address":"史釗域道74-78號2樓205A室","lat":22.2834264,"lng":114.1544905,"price":45,"rating":3.4},
  {"id":81,"name":"Nam Kee Spring Roll Noodle 南記粉麵","type":"粉麵","address":"砵典乍街行人電梯地下","lat":22.2831051,"lng":114.1548233,"price":40,"rating":3.8},
  {"id":82,"name":"27 Kebab House","type":"中東菜","address":"荷李活道27號","lat":22.2822235,"lng":114.1538585,"price":42,"rating":4.2},
  {"id":83,"name":"Yoshinoya 吉野家 (中環)","type":"快餐","address":"干諾道中15-18號大廈地下","lat":22.2830243,"lng":114.1576832,"price":38,"rating":3.6},
  {"id":84,"name":"One Dim Sum 一點心 (太子)","type":"點心","address":"通菜街209A地下","lat":22.3254818,"lng":114.1691477,"price":48,"rating":4.3},
  {"id":85,"name":"Mui Kee Congee 妹記生滾粥品","type":"粥品","address":"花園街123A號市政大廈3樓11-12號","lat":22.3208729,"lng":114.1706581,"price":40,"rating":4.2},
  {"id":86,"name":"Kam Wah Cafe 金華冰廳","type":"茶餐廳","address":"弼街45-47號","lat":22.3222738,"lng":114.1697189,"price":42,"rating":3.7},
  {"id":87,"name":"Eastern Delights 東方小祇園","type":"素食","address":"深水埗街10號","lat":22.3184657,"lng":114.1666938,"price":40,"rating":4.6},
  {"id":88,"name":"Malay Restaurant 馬來餐廳","type":"馬來西亞菜","address":"白布街16號7號舖","lat":22.3177568,"lng":114.1706008,"price":45,"rating":4.2},
  {"id":89,"name":"Fairwood 大快活 (旺角)","type":"快餐","address":"旺角道25號","lat":22.3203645,"lng":114.1671890,"price":40,"rating":3.7},
  {"id":90,"name":"Sai Kee Congee Shop 西記粥店","type":"粥品","address":"旺角道25號","lat":22.3203645,"lng":114.1671890,"price":35,"rating":3.5},
  {"id":91,"name":"Yet Shin Eatery 日新美食","type":"茶餐廳","address":"花園街123A號市政大廈3樓5號","lat":22.3208713,"lng":114.1705767,"price":38,"rating":3.9},
  {"id":92,"name":"Wing Yuen Noodle 永園麵家","type":"粉麵","address":"通菜街69號地下","lat":22.3187294,"lng":114.1705514,"price":36,"rating":4.2},
  {"id":93,"name":"Tim Ho Wan 添好運 (奧運)","type":"點心","address":"海庭道18號奧海城2期G72A-C舖","lat":22.3170282,"lng":114.1627279,"price":48,"rating":4.3},
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
