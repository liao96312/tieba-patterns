# Corpus metadata

## Collection

- Collected: 2026-07-30
- Bars: 孙笑川吧、抗压背锅吧
- Post rows: 119 raw, 117 unique by `note_id`
- Unique posts by bar: 孙笑川吧 67; 抗压背锅吧 50
- Comment rows: 3,281 raw, 3,231 unique by `comment_id`
- Unique comments by bar: 孙笑川吧 2,151; 抗压背锅吧 1,080
- Reply rows with `parent_comment_id`: 1,206
- Clean normalized expressions: 1,932
- Observed publish range: 2022-10-03 07:20:10 through 2026-07-30 14:20

## Raw fields

Posts:

`note_id, title, desc, note_url, publish_time, creator_hash, user_nickname, tieba_name, tieba_link, total_replay_num, total_replay_page, source_keyword, last_modify_ts`

Comments:

`comment_id, parent_comment_id, content, creator_hash, user_nickname, publish_time, sub_comment_count, note_id, note_url, tieba_id, tieba_name, tieba_link, last_modify_ts`

Do not expose `creator_hash`, `user_nickname`, user links, or identifiers in generated replies.

## Local artifacts

- `work/tieba_raw/tieba/jsonl/`
- `work/tieba_resample_raw/tieba/jsonl/`
- `work/tieba_enrich_raw/tieba/jsonl/`
- `work/tieba_enrich_broad_raw/tieba/jsonl/`
- `work/tieba_enrich_clean/corpus.jsonl`
- `work/tieba_enrich_clean/matched_comments.jsonl`

`matched_comments.jsonl` retains structural metadata but omits user identity fields. Its fields are:

`pattern, score, tieba_name, note_id, note_title, comment_id, parent_comment_id, publish_time, sub_comment_count, frequency, content`

## Matching rule

1. Normalize Unicode, URLs, whitespace, mentions, and reply prefixes.
2. Deduplicate first by comment ID and then by normalized text.
3. Compare comments with Pattern templates and examples using sequence ratio plus character-bigram overlap.
4. Require score `>= 0.32`.
5. Also require a fixed Pattern anchor of at least three characters, unless similarity is `>= 0.55`.
6. Use matches as evidence for abstraction; do not paste them into generated replies.

The strict pass matched 10 expressions already structurally close to the original 50 Patterns. Broader recurring-family mining produced the additions below.

## Recurring families used for Patterns 51–70

| Family | Unique expressions | Weighted occurrences |
|---|---:|---:|
| 催更/直播 | 19 | 40 |
| 鉴串 | 16 | 21 |
| 爆金币 | 21 | 77 |
| 熟人捕获 | 7 | 11 |
| 何意味 | 22 | 24 |
| 围观标记 | 5 | 7 |
| 抢功归因 | 8 | 13 |
| 伪正经规劝 | 3 | 6 |
| 直接处理 | 7 | 9 |
| 真假裁决 | 5 | 5 |
| 等级资历 | 14 | 14 |
| 鼠类归档 | 49 | 58 |
| 抽象短评 | 5 | 9 |
| 希腊奶 | 23 | 28 |
| 认可敷衍 | 4 | 5 |

Count unique expressions first. Weighted occurrences are supporting context only because a single active thread can otherwise dominate the corpus.

## Patterns 71–108 audit

- No additional crawl was required.
- The existing clean corpus contains 1,010 independent 抗压背锅吧 expressions and 1,021 weighted occurrences.
- Patterns 71–108 were abstracted from recurring 抗吧 devices including `桂霞`、`XX孝子`、`你什么冠军`、`定制`、`控制变量`、`碰瓷`、`团建`、`充值洗白`、`公开处刑`、`一目了然` and long causal post-match analysis.
- Esports-specific Patterns should only be used when the conversation supplies an esports, ranking, competition, fandom, or performance-comparison context.

## Slang verification (2026-07-31)

- User correction: `3` / `+3` means a reply grants three Tieba experience points and is commonly posted alone to water experience; it does not mean “散”.
- Corpus-supported general terms: `gkd`、`CY/插眼`、`何意味`、`希腊奶`、`硕鼠/巨鼠`、`爆金币/爆币`、`ATM启动`、`好似`、`串经验`、`单机贴吧`.
- Corpus-supported esports terms: `抗抗`、`捞批捞`、`定制`、`控制变量`、`大飞`、`蝌蚪`、`鸡蛋`、`猪杂`、`尿罐子/尿粉`、`胎手/胎盘子`、`48/48b`、`科目四`.
- External checks used direct Tieba discussions where possible and secondary meme glossaries only to disambiguate origin: `CY/插眼` (shenmegeng.cn), `希腊奶` (moegirl.icu), `GKD` (yglsr.com), `鸡蛋` and `48/48b` (tieba.baidu.com), `大飞` (18183.com), `猪杂` (jishi3.com), `胎手` (ali213.net), `尿罐子/尿粉` (yehuowiki.com), and `科目四` (danmuxiu.cn).
- `浮木`、`48/48b`、`科目四` and black names tied to real family or private-life trauma are interpret-only or prohibited in generation.
- `巧克力`、`尺老狗` remain unresolved or context-dependent. Keep them in source metadata, not in the runtime slang dictionary.
