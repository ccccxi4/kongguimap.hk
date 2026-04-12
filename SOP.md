# 港版窮鬼地圖 SOP（標準作業程序）

> 專屬於 kongguimap.hk 的開發、維護與運營指南

---

## 一、項目概述

**項目名稱**：港版窮鬼地圖  
**網址**：https://kongguimap.hk（Cloudflare Pages）  
**GitHub**：https://github.com/ccccxi4/kongguimap.hk  
**核心定位**：香港平價美食（≤$50）地圖，覆蓋多區真實餐廳

**技術棧**：
- 前端：HTML5 + CSS3 + Vanilla JavaScript
- 地圖：Leaflet.js + OpenStreetMap
- 部署：GitHub + Cloudflare Pages
- 數據驗證：Google Places API

---

## 二、數據收集與驗證 SOP

### 2.1 新增餐廳流程

```
收集餐廳資訊 → Google Places API 驗證 → 修正位置偏差 → 寫入數據 → 測試顯示
```

### 2.2 Google Places API 驗證腳本

**驗證項目**：
1. 餐廳名稱是否真實存在
2. 地址是否正確
3. 經緯度偏差（>100米需修正）
4. 營業狀態（是否已結業）

**驗證標準**：
| 偏差距離 | 處理方式 |
|---------|---------|
| < 100米 | 接受，可選微調 |
| 100-500米 | 必須修正為 API 返回位置 |
| > 500米 | 重新核實，可能地址錯誤 |
| 搜尋不到 | 刪除或標記待核實 |

**Python 驗證腳本**：`verify_restaurants.py`
```python
# 核心邏輯
1. 讀取餐廳列表
2. 調用 Google Places API (findplacefromtext)
3. 計算位置偏差 (Haversine formula)
4. 輸出驗證報告 (verification_result.json)
```

### 2.3 數據格式規範

```javascript
{
  id: 唯一編號（遞增）,
  name: '餐廳名稱（中英文）',
  type: '類型（見分類表）',
  address: '詳細地址',
  lat: 緯度（API驗證後）,
  lng: 經度（API驗證後）,
  price: 平均消費（HKD）,
  rating: Google評分（可選）
}
```

**餐廳類型分類**：
- 茶餐廳、粥粉麵、快餐、點心、燒臘
- 雲吞麵、餃子、越南菜、泰國菜、日本菜
- 台灣菜、中東菜、西餐、咖啡廳、素食、其他

---

## 三、開發與部署 SOP

### 3.1 本地開發流程

```bash
# 1. 進入項目目錄
cd /Users/ccccxi4l/WorkBuddy/[timestamp]/hk-cheap-map

# 2. 啟動本地服務器（可選）
python3 -m http.server 8080
# 或
npx serve .

# 3. 瀏覽器訪問 http://localhost:8080
```

### 3.2 Git 工作流程

```bash
# 修改後提交
git add .
git commit -m "描述更新內容"
git push origin main
```

**提交信息規範**：
- `更新餐廳數據：新增/刪除/修正 XX 間餐廳`
- `優化功能：XX 功能改進`
- `修復問題：修正 XX Bug`

### 3.3 Cloudflare Pages 部署

**自動部署**：
- GitHub push 後自動觸發構建
- 構建命令：無（靜態網站）
- 輸出目錄：根目錄 `/`

**部署後檢查**：
1. 訪問 https://kongguimap.hk
2. 檢查地圖是否正常加載
3. 測試搜索功能
4. 驗證移動端顯示

---

## 四、常見問題與解決方案

### 4.1 數據準確性問題

| 問題 | 原因 | 解決方案 |
|-----|------|---------|
| 餐廳不存在 | 虛假資訊/已結業 | Google Places API 驗證後刪除 |
| 位置偏差 | 手動輸入錯誤 | 使用 API 返回的經緯度 |
| 地址錯誤 | 門牌號錯誤 | 核實後修正 |

**案例**：
- 祥香茶餐廳 → 經 API 驗證不存在，已刪除
- 堅尼地城麥當勞 → 位置偏差 200+ 米，已修正

### 4.2 技術問題

| 問題 | 解決方案 |
|-----|---------|
| 地圖加載緩慢 | 檢查 OpenStreetMap tile 服務 |
| 移動端顯示異常 | 檢查 viewport meta 標籤 |
| 搜索無結果 | 檢查 toLowerCase() 處理 |
| 導航跳轉失敗 | 檢查 URL encode |

### 4.3 部署問題

| 問題 | 解決方案 |
|-----|---------|
| Cloudflare 404 | 確認自定義域名配置 |
| 緩存未更新 | 清除 Cloudflare 緩存 |
| GitHub 推送失敗 | 檢查 token 權限 |

---

## 五、功能模塊說明

### 5.1 核心功能

1. **地圖展示**：Leaflet.js + OpenStreetMap
2. **餐廳列表**：左側可滾動列表，支持搜索
3. **搜索功能**：名稱、地址、類型模糊搜索
4. **導航功能**：Google Maps / Apple Maps 跳轉
5. **用戶提交**：表單收集新餐廳建議

### 5.2 響應式設計

**桌面端**：
- 左側邊欄 360px
- 右側地圖自適應

**移動端（<768px）**：
- 地圖佔 55% 屏幕高度
- 列表佔 45%，底部抽屜式
- 提交按鈕浮動定位

### 5.3 用戶提交處理

**當前實現**：
- 數據保存到 localStorage
- 管理員手動審核後加入

**未來優化方向**：
- 接入 EmailJS 發送郵件通知
- 或接入 Google Sheets API 自動記錄

---

## 六、擴展計劃

### 6.1 區域擴展優先級

1. ✅ 堅尼地城（已完成）
2. ✅ 西營盤（已完成）
3. ✅ 銅鑼灣（已完成）
4. ✅ 中環（已完成）
5. ✅ 旺角（已完成）
6. 🔄 深水埗（待開發）
7. 🔄 尖沙咀（待開發）
8. 🔄 灣仔（待開發）

### 6.2 功能擴展

- [ ] 用戶評分/評論
- [ ] 收藏功能
- [ ] 路線規劃
- [ ] 營業時間顯示
- [ ] 圖片上傳

---

## 七、聯繫與反饋

**用戶反饋渠道**：
- 網站內「提交餐廳」按鈕
- GitHub Issues

**維護者**：ccccxi4

---

*最後更新：2026年4月13日*
