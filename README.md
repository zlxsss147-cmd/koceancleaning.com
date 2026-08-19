# Kocean Cleaning — koceancleaning.com

浙江易畅经营体 · Kocean 清洁产品 B2B 英文站（SEO 引流 + 权威背书）

## 技术栈

- **Astro 4**（静态站点，Markdown 内容优先）
- 内容集合：`src/content/blog/`（写 `.md` 文件即自动出页面）
- 部署：Cloudflare Pages（待配置，push 即部署）

## 常用命令

```bash
npm install        # 安装依赖
npm run dev        # 本地开发 http://localhost:4321
npm run build      # 构建到 dist/
npm run preview    # 预览构建产物
```

## 目录结构

```
src/
├── content/
│   ├── config.ts          # 内容集合 schema（blog 字段定义）
│   └── blog/              # ★ 文章就放在这里（.md 或 .mdx）
├── data/site.ts           # 站点全局数据（导航/产品分类/联系方式）
├── layouts/BaseLayout.astro
├── pages/                 # 首页/产品/OEM/About/Contact/Blog
└── styles/global.css
```

## 内容流水线（AI 每日 2 篇）

1. AI 按「主旨清单」生成 `.md` → `src/content/blog/`
2. push 到 GitHub `draft` 分支（不直接上生产）
3. 人工审核 → 合并到 `main` → Cloudflare 自动构建上线

## Blog 文章 frontmatter 字段

```yaml
---
title: "文章标题（SEO 关键词友好）"
description: "160 字以内摘要（搜索展示用）"
pubDate: 2026-08-19
category: "Nonwoven Materials"   # 五大类之一
tags: ["nonwoven", "spunlace"]
draft: false                     # true 则不上线
---
```

五大内容支柱：Nonwoven Materials / Buying Guides / Applications / OEM & Quality / Industry & Sustainability（比例约 6:3:1）。
