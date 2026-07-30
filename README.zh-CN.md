# Tieba Patterns

**语言：** [English](README.md) | 简体中文

![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Patterns](https://img.shields.io/badge/Patterns-108-EF4444)

Tieba Patterns 是一个可复用的 Codex skill，根据分类修辞句式生成简短、贴合上下文的中文论坛回复。它强调短铺垫、快反转，攻击可见的观点或行为，不针对个人隐私、受保护特征或无关身份。

## 功能

| 模块 | 能力 |
| --- | --- |
| 句式库 | 108 类贴吧风格修辞句式 |
| 上下文分析 | 识别矛盾、双重标准、无依据自信和情绪过激 |
| 输出控制 | 默认只输出一句，明确要求时才提供多个版本 |
| 安全边界 | 排除威胁、开盒、围攻、受保护特征攻击和虚构指控 |
| 语料维护 | 提供 JSONL 匹配脚本，筛选与现有句式结构相近的评论 |
| Codex 集成 | 包含 skill 指令和 OpenAI agent 元数据 |

## 安装

将仓库复制到 Codex skills 目录：

```powershell
git clone https://github.com/liao96312/tieba-patterns.git
Copy-Item -Recurse -Force .\tieba-patterns "$env:USERPROFILE\.codex\skills\tieba-patterns"
```

重启 Codex，然后按名称调用：

```text
Use $tieba-patterns to write one sharp context-aware Tieba-style reply.
```

## 工作方式

1. 读取分类句式库。
2. 从目标消息中找出一个具体弱点。
3. 选择匹配的修辞结构。
4. 用当前上下文替换句式槽位。
5. 输出一句短回复，不在后面解释笑点。

具体行为、强度和安全边界见 [`SKILL.md`](SKILL.md)。

## 语料匹配

仓库内的脚本可以从 JSONL 语料中筛选与现有句式结构相近、带元数据的评论：

```powershell
python .\scripts\match_corpus.py `
  --patterns .\references\patterns.md `
  --posts .\data\posts.jsonl `
  --comments .\data\comments.jsonl `
  --threshold 0.32 `
  --per-pattern 25 `
  --output .\work\matched.jsonl
```

匹配结果只用于维护句式库，不能直接复制发布。新增内容前应逐条审核并重新改写。

## 仓库结构

```text
SKILL.md                       skill 工作流、风格、强度和边界
agents/openai.yaml             Codex 展示信息和默认提示词
references/patterns.md         分类修辞句式库
references/corpus-metadata.md  语料来源与维护说明
scripts/match_corpus.py        JSONL 相似度匹配脚本
```

## 验证

```powershell
python .\scripts\match_corpus.py --help
```

## 状态

这是一个聚焦于 skill 与参考句式库的仓库，不包含爬虫、自动发帖、账号自动化或个人信息采集流程。
