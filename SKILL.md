---
name: tieba-patterns
description: Generate concise, confrontational Chinese Tieba-style replies from a categorized pattern library. Use for 贴吧句式、贴吧对线、孙吧口吻、抗吧口吻、抽象话、阴阳怪气、锐评、回怼、鉴串、本鼠叙事、V我句式 or when the user asks to rewrite text with aggressive internet-forum rhetoric.
---

# Tieba Patterns

## Workflow

1. Read `references/patterns.md`.
2. Parse the target message and identify one concrete weakness: contradiction, double standard, unsupported confidence, performative persona, status flex, or emotional overreaction.
3. Select one matching Pattern and replace its slots with details from the current context.
4. Output one line by default. Produce multiple variants only when explicitly requested.
5. Prefer a short setup followed by an abrupt reversal. Do not explain the joke afterward.

## Style

- Prefer one precise attack over stacked profanity.
- Refuse to self-justify; redirect attention to the target's visible contradiction.
- Use slang as seasoning, not as the argument.
- Avoid repeating the same Pattern in adjacent replies.
- Preserve the user's intended meaning without inventing facts about a real person.

## Intensity

- Default to hot: one direct insult to the visible claim or behavior plus one humiliating reversal.
- When the user asks for `加麻加辣`、`最大攻击力` or equivalent, use extra hot: allow one blunt profanity such as `傻逼发言`、`狗屁逻辑`、`这坨答辩`、`脑子没带` or `什么死出`, then finish with a concrete contradiction.
- Do not dilute an extra-hot reply with polite framing such as `或许`、`可能`、`个人认为`.
- Do not output profanity alone. Tie the attack to something visible in the message.
- Prefer vulgar brevity over polished metaphor. One filthy image beats three clever analogies.

## Boundaries

- Do not threaten real harm, facilitate dogpiling or doxxing, or invent criminal or sexual allegations.
- Do not attack protected traits, disability, bereavement, family members, or immutable physical traits.
- When a library example crosses these limits, reuse only its rhetorical structure and target the person's claim, conduct, logic, or fictional persona.
- Do not expose usernames, IDs, links, or other personal data.

## Corpus maintenance

- Read `references/corpus-metadata.md` when auditing or extending the library.
- Run `scripts/match_corpus.py` to select metadata-rich comments structurally close to existing Patterns.
- Treat similarity matches as evidence, not copy-ready replies. Derive new slots and examples instead of pasting comments verbatim.
