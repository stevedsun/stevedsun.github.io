---
title: "规范的错误信息"
date: 2022-08-23T22:18:00+08:00
tags: [错误日志, 技术文档]
description: ""
---

## 基本原则

- Don't fail silently
- Follow the programming language guides
- Implement the full error model
- Avoid swallowing the root cause
- Log the error codes
- Raise errors immediately

## 解释错误原因

- 具体，准确，避免含糊。
- 在错误信息中识别用户输入。如果错误输入特别长：
  - 渐进地显示，提供一个可点击的省略号。
  - 截断，只保留必要部分。
- 明确告诉用户，系统的要求和限制

## 解释如何处理问题

- 给用户可操作的错误信息。也就是说，在解释了问题的原因后，说明如何解决这个问题。
- 提供一个例子。

## 清晰的错误信息

- 简明扼要，使用主动语态。
- 避免双重否定句式。
- 让目标用户能够理解。
- 专业术语前后一致。

## 错误信息的格式

- 使用链接提供更多信息。
- 渐进式呈现错误信息（如可点击的省略号）。
- 错误提示应该靠近错误发生的位置。
- 避免混乱的字体颜色。
- 使用正确的语气。
  - 不要告诉用户错在哪，告诉用户应该做什么。
  - 避免责备、幽默、道歉的语气。

## 对后端开发的建议

- 错误要有错误码
- 在错误信息结构里提供一个指向错误解释的 ID，如：
  `{ "error" : "Bad Request - Request is missing a required parameter: -collection_name. Update parameter and resubmit. Issue Reference Number BR0x0071" }`
