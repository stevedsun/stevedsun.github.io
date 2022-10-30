# 规范的错误信息


本文整理了 Google 官方文档中关于错误信息的编写规范。适用于有一定编程经验，尤其从事业务开发的程序员。

通过本文你可以：

- 写出风格统一、用户友好的错误信息
- 提高代码的可维护性，降低沟通成本

Google 文档原文：[Error Messages](https://developers.google.com/tech-writing/error-messages)

## 基本原则

- 错误不应该被掩盖 (Don't fail silently)
- 遵循语言的规范 (Follow the programming language guides)
- 实现完整的错误模型 (Implement the full error model)
  ```
  包含错误码、错误内容、错误原因、处理方法
  ```
- 避免吞掉问题根源 (Avoid swallowing the root cause)
- 输出错误代码 (Log the error codes)
- 快速抛出错误 (Raise errors immediately)

## 解释错误原因

使用错误信息给用户解释原因时，应该遵循：

- 具体，准确，避免含糊。
- 在错误信息中包含用户输入的错误内容。如果输入的内容特别长：
  - 渐进地显示，提供一个可展开详情的省略号。
  - 截断内容，只保留必要部分。
- 明确告诉用户，系统的要求和限制

## 解释如何处理问题

- 对用户来说，错误信息必须有可操作性。也就是说，在解释了问题的原因后，说明如何解决这个问题。
- 最好给用户提供一个例子。

## 清晰的错误信息

- 简明扼要，使用主动语态。（这方面内容可以参考[技术文档写作指南](https://sund.site/posts/2022/technical-writing/)）
- 避免出现双重否定句式。
- 让目标用户能够理解，即根据用户掌握的知识，提供有帮助的内容。
- 专业术语应前后一致。

## 错误信息的格式

- 使用链接提供更多信息。
- 渐进式呈现错误信息（比如可以展开详情的省略号）。
- 错误提示应该贴近错误发生的位置。
- 避免错误信息滥用字体或颜色。
- 使用正确的语气:
  - 不要告诉用户错在哪，告诉用户应该做什么。
  - 避免责备、幽默、道歉的语气。

## 对后端开发的建议

- 错误要有错误码
- 可以在错误信息结构里提供一个指向错误解释的 ID，如：
  ```json
  {
    "error": "Bad Request - Request is missing a required parameter: -collection_name. Update parameter and resubmit. Issue Reference Number BR0x0071"
  }
  ```

