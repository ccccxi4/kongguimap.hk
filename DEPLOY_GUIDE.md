# Cloudflare Pages 部署指南

## 步骤 1: 登录 Cloudflare
- 打开 https://dash.cloudflare.com
- 登录你的账号

## 步骤 2: 创建 Pages 项目
1. 点击左侧菜单 **Pages**
2. 点击 **"Create a project"**
3. 选择 **"Connect to Git"**

## 步骤 3: 连接 GitHub
1. 点击 **"Connect GitHub"**
2. 授权 Cloudflare 访问你的 GitHub 账号
3. 在列表中找到并选择 `ccccxi4/kongguimap.hk` 仓库
4. 点击 **"Begin setup"**

## 步骤 4: 构建设置
填写以下信息：
- **Project name**: `kongguimap-hk`（或你喜欢的名字）
- **Production branch**: `main`
- **Framework preset**: 选择 **None**
- **Build command**: （留空，不填）
- **Build output directory**: （留空，不填）

## 步骤 5: 部署
1. 点击 **"Save and Deploy"**
2. 等待 1-2 分钟构建完成
3. 获得网址：`https://kongguimap-hk.pages.dev`

## 完成！
你的网站已上线，每次推送代码到 GitHub 会自动重新部署。
