# DialogAI - 多场景对话分析平台

AI 驱动的对话分析平台，支持多种场景的结构化分析与 Excel 报告导出。

**线上地址**：https://meetingnotes.cyou

---

## 功能特性

### 四大分析场景

| 场景 | 说明 |
|------|------|
| **VC Pitch 反馈** | 分析投资人与创始团队的对话，还原问题背后的真实动机，评估回答质量 |
| **电商 B2B 对谈** | 分析采购方与供应商的谈判对话，提取关键诉求，优化报价话术 |
| **面试分析** | 分析面试对话，识别考察维度，评估回答表现，提供改进建议 |
| **会议总结** | 结构化会议纪要，提取决策、行动项，自动分配责任人和时间节点 |

### 核心能力

- Google OAuth 登录
- 上传对话文件（PDF / Word / TXT）
- 可选上传背景资料 PDF 作为分析上下文
- AI 分析（DeepSeek API）
- 中英文 Excel 报告导出

---

## 技术架构

```
meetingnotes.cyou (Vercel)
├── Next.js 14 前端（React + TypeScript + Tailwind CSS）
├── Python Serverless API（FastAPI）
└── Supabase PostgreSQL（数据库）
```

### 项目结构

```
├── vercel.json              # Vercel 部署配置
├── requirements.txt         # Python 依赖
├── api/
│   └── index.py             # Vercel Serverless 入口
├── backend/
│   ├── main.py              # FastAPI 应用
│   ├── config.py            # 环境变量配置
│   ├── database.py          # SQLAlchemy 数据库连接
│   ├── models.py            # 数据模型（User, AnalysisRecord）
│   ├── analyzer.py          # DeepSeek API 调用
│   ├── extractors.py        # 文件文本抽取
│   ├── excel_export.py      # Excel 导出
│   ├── translator.py        # 中英文翻译
│   ├── auth/                # Google OAuth + JWT 认证
│   ├── routers/             # API 路由
│   └── prompts/             # 各场景 LLM 提示词
├── frontend/
│   ├── src/app/             # Next.js App Router 页面
│   ├── src/components/      # React 组件
│   ├── src/lib/             # API 客户端、Auth 工具
│   └── public/              # 静态资源（logo、favicon）
└── lib/                     # 共享 Python 工具库
```

---

## 部署

### 环境变量

| 变量 | 说明 |
|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 |
| `DATABASE_URL` | Supabase PostgreSQL 连接字符串 |
| `JWT_SECRET` | JWT 签名密钥 |
| `GOOGLE_CLIENT_ID` | Google OAuth 客户端 ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth 客户端密钥 |
| `ALLOWED_ORIGINS` | CORS 允许的域名 |
| `NEXT_PUBLIC_GOOGLE_CLIENT_ID` | 前端 Google 客户端 ID |

### Vercel 一键部署

项目配置为单个 Vercel 项目同时部署前端和后端：

1. 在 Vercel 导入本仓库
2. 在 Settings → Environment Variables 中添加以上环境变量
3. 部署完成

---

## 本地开发

```bash
# 1. 克隆并安装后端依赖
git clone https://github.com/Oceanjackson1/Agentic-VC-Feedback-Loop.git
cd Agentic-VC-Feedback-Loop
python3 -m venv venv && source venv/bin/activate
pip install -r backend/requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入各项密钥

# 3. 启动后端
cd backend && uvicorn main:app --reload --port 8000

# 4. 启动前端（新终端）
cd frontend && npm install && npm run dev
```

访问 http://localhost:3000

---

## 开发者

Built by [Ocean](https://x.com/Ocean_Jackon)
