# 投资人对话总结 Agent

An **Agentic VC Feedback Loop**：将每次投资人对话作为一次 observation，通过 multi-step reasoning 建模投资人问题背后的决策逻辑，输出 decision artifacts，支撑创始团队持续 refine 产品、叙事与沟通策略。

---

## 系统定位

### 这不是什么

本系统**不是**：chatbot、summarizer、transcription tool 或 simple analysis script。  
它**不**旨在「总结投资人说了什么」。

### 这是什么

一个 **Agentic System**，具备：

- **explicit role assumption**：Tier-1 VC 视角（Web2 & Web3 投资与投后）
- **multi-step reasoning**：从表面问题反推 investor core motive，评估 team response，给出 actionable feedback
- **decision feedback loop**：每一次投资人通话 = loop 中的一次 observation；输出的 Excel 不是报告，而是 **decision artifacts**

### 设计目标

- **建模「投资人为什么这样问」**，而非复述「投资人问了什么」
- 通过可累积的 decision artifacts，帮助团队在多次迭代中持续 refine：
  - 产品方向（product）
  - 对外叙事（narrative）
  - 投资人沟通策略（team preparation）

---

## Agentic Flow

单次调用完成一次 loop 迭代：

1. **Observation 输入**：上传包含投资人与团队交流文字的文件（.txt / .md / .pdf / .docx / .html）
2. **Text Extraction**：后端抽取纯文本（不处理音频、图片、扫描件）
3. **Reasoning**：DeepSeek 原生 API 单次调用，完成全部分析
4. **Artifact 输出**：导出 Excel，每行 = 一个投资人核心问题，列对应结构化分析字段
5. **Download**：用户下载 decision artifacts，用于后续复盘与策略调整

### 支持的文件类型

| 扩展名 | 说明 |
|--------|------|
| .txt   | 纯文本 |
| .md    | Markdown |
| .pdf   | 可直接提取文本的 PDF（不处理扫描版） |
| .docx  | Word 文档 |
| .html  | 网页/HTML |

> 注意：文件需为可解析为纯文本的格式。扫描版 PDF、图片、音频等不支持。

---

## 如何启动

> 以下命令中的 `项目目录` 请替换为你本地下载该项目的实际路径。

### 环境要求

- **Python 3.9+**
- **DeepSeek API Key**（从 [platform.deepseek.com](https://platform.deepseek.com) 获取）

### 方式一：使用虚拟环境（推荐）

避免与系统 Python 或 Anaconda 环境冲突，建议使用 `venv`：

```bash
# 1. 进入项目目录
cd 项目目录

# 2. 创建虚拟环境
python3 -m venv venv

# 3. 激活虚拟环境
source venv/bin/activate   # macOS / Linux
# 或 Windows: venv\Scripts\activate

# 4. 安装依赖
pip install -r backend/requirements.txt

# 5. 配置 API Key（若尚未配置）
# 编辑 .env 文件，填入 DEEPSEEK_API_KEY=sk-xxx

# 6. 启动服务
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 方式二：使用启动脚本

```bash
# 1. 进入项目目录
cd 项目目录

# 2. 安装依赖（若未安装）
pip install -r backend/requirements.txt

# 3. 确保 .env 中已配置 DEEPSEEK_API_KEY

# 4. 添加执行权限并启动
chmod +x run.sh
./run.sh
```

### 方式三：手动启动

```bash
cd 项目目录/backend

export DEEPSEEK_API_KEY=sk-xxx   # 或通过 .env 配置
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 访问产品

启动成功后，终端会显示：

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

在浏览器中打开：**http://localhost:8000**

### 停止服务

在运行 uvicorn 的终端中按 **Ctrl + C** 即可停止服务。

### 重新启动

若已关闭终端，重新打开一个新终端，按上述「方式一」或「方式二」再次执行启动命令即可。

---

## 配置说明

### API Key 配置

1. 复制示例配置：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env`，填入你的 DeepSeek API Key：
   ```
   DEEPSEEK_API_KEY=sk-你的密钥
   ```

> API Key 仅存在于服务端环境变量中，不会暴露给前端。

---

## 项目结构

```
投资人对话总结Agent/
├── backend/
│   ├── main.py         # FastAPI 入口，上传→分析→下载
│   ├── extractors.py   # 文本抽取（txt/md/pdf/docx/html）
│   ├── analyzer.py     # DeepSeek API 调用
│   ├── excel_export.py # Excel 导出
│   └── requirements.txt
├── frontend/
│   └── index.html      # 上传与下载 UI
├── .env                # 环境变量（含 API Key，勿提交）
├── .env.example        # 环境变量示例
├── run.sh              # 启动脚本
└── README.md
```

---

## 使用流程

1. 在页面中**上传**一个包含投资人与团队交流文字的文件
2. 点击 **「开始分析」**
3. 等待分析完成（通常需 10–30 秒）
4. **下载**生成的 Excel 文件（文件名格式：`原文件名_分析结果.xlsx`）

---

## 常见问题

### 出现 Intel MKL 错误

若使用 Anaconda 时出现 `Intel MKL FATAL ERROR: Cannot load libmkl_core.1.dylib`，建议改用 **方式一（venv）** 启动，可避免该问题。

### 上传后报 Internal Server Error

1. 查看运行 uvicorn 的终端中的报错信息
2. 确认 `.env` 中 `DEEPSEEK_API_KEY` 已正确配置
3. 尝试上传 .txt 文件测试，以区分是文件解析问题还是 API 调用问题

### PDF 无法解析

仅支持**可直接提取文本**的 PDF。扫描版 PDF 会提示「该 PDF 无法解析为文本（可能是扫描版）」。

---

## 成功标准自检

- [x] 支持 .txt / .md / .pdf / .docx / .html
- [x] 正确抽取文本并完成分析
- [x] Excel 可正常下载并打开
- [x] Excel 每行对应一个投资人核心问题
- [x] 内容体现 VC 判断逻辑，非泛化建议
