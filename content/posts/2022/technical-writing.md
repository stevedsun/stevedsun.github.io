---
title: "技术文档写作指南"
date: 2022-08-21T15:29:00+08:00
description: "谷歌技术文档写作指南"
tags: [技术规范 Technical-Specs]
tags: [写作, 技术文档]
aliases: [/posts/technical-writing/]
---

本文内容摘录自 [Technical Writing](https://developers.google.com/tech-writing/overview) （谷歌技术文档写作指南）的第一部分。

本文适用于想要提高技术文档写作、技术领域日常沟通能力的读者，对于一些商务的、非文学性质的英语办公场景沟通，也能起一定帮助作用。

阅读过本文的读者可以：

- 提高在日常办公中清晰、准确、客观地传达概念和逻辑的能力。
- 掌握英文技术文档写作规范。

## 词汇（Words）

- 对于已有的术语，不要重复发明新的词汇，可以用一个链接指向解释它的页面。
- 如果有必要，可以在文档中直接定义新的术语，但如果术语比较多，最好建立一个术语对照表。
- 文档各处出现的术语应该保持一致的名称或缩写。
- 关于缩写：第一次出现要用**粗体**写全称并用括号指明缩写，之后的文章中不要反复混用全称和缩写。

  {{< admonition tip "举例" >}}
  This document is for engineers who are new to the **Telekinetic Tactile Network** (**TTN**) or need to understand how to order TTN replacement parts through finger motions.
  {{< /admonition >}}

- 如果一个术语出现频率不高，请不要使用缩写。
- 使用缩写的情况有：1. 缩写明显更简短；2. 该术语出现频率很高。

- 谨慎使用代名词（It，they，that 等）。
  - 代名词一定要出现在它所指代的名词之后。
  - 如果代名词远离它指代的名词（超过 5 个单词），就不用代名词。
  - 在名词和代名词之间出现第二个名词，会产生歧义，应避免这种情况。

类比计算机编程语言：

缩写 = 对术语的一层抽象。读者需要花费更多脑力去把它展开成对应的名词。

代名词 = 指针。它容易引起歧义，所以要避免在读者大脑中引起「空指针」错误。

## 主动语态（Active voice）

- 技术文档中应尽量使用主动语态。
  - 被动语态在读者大脑中需要额外的加工转换才能被理解。
  - 被动语态用来间接地表达行为，容易引起混乱。
  - 有些被动语态省略了行为主体，会迫使读者猜测主语是谁。
- 如果使用被动语态，应正确使用过去分词的各种形式和介词（如 as，by）。
- 祈使句的动词（命令式动词）应该使用主动语态。
- 科技论文中经常出现被动语态（如 It has been suggested that...），这种写法并不能传递更多信息，很多科学期刊也开始鼓励使用主动语态。

## 炼句（Clear sentences，Short sentences）

- 选择准确、有力、具体的动词。减少不精确的、软弱的或通用的动词。
  {{< admonition tip "错误的例子" >}}
  is，are，occur，happen
  {{< /admonition >}}

- Be 动词和通用动词可以用，但它们通常是一些不良写作习惯的信号，如
  - 句子中缺少行为主体
  - 句子使用了被动语态
- 减少 there be 句式，把 there be 句式中的主语和动词提炼出来
  {{< admonition tip "错误的例子" >}}

  避免这样用：There is no guarantee that the updates will be received in sequential order.

  应改为：Clients might not receive the updates in sequential order.
  {{< /admonition >}}

- 尽量少用或不用形容词和副词，因为这些词汇过于主观。
- 尽量使用短的句子。短句比长句更易读、易维护、不易犯错。
  - 每一个句子只表达一个观点。
  - 长句尽量转换成列表。
  - 用简洁表达，去掉多余的词汇
  - 减少从句。
  - 正确区分 that 和 which 从句。

## 列表和表格（Lists and tables）

- 正确区分有序列表（数字列表，numbered lists）和无序列表（圆点列表，bulleted lists）。
- 把句内列举的项（embedded list）转换成无序列表，如：

  {{< admonition tip "举例" >}}

  The llamacatcher API enables callers to create and query llamas, analyze alpacas, delete vicugnas, and track dromedaries.

  应换成：

  The llamacatcher API enables callers to do the following:

  - Create and query llamas.
  - Analyze alpacas.
  - Delete vicugnas.
  - Track dromedaries.

  {{< /admonition >}}

- 保持列表项之间的平行关系（避免把不同层级的东西混在一列）。
- 在使用有序列表时，用一个命令式动词开头，如：

  {{< admonition tip "举例" >}}

  1. Download the Frambus app from Google Play or iTunes.
  2. Configure the Frambus app's settings.
  3. Start the Frambus app.

  {{< /admonition >}}

- 只有列表每一个项都是句子时，才使用首字母大写和句号，否则不需要。
- 使用表格应遵循的原则：
  - 每列都有标题
  - 单元格字数尽量少
  - 尽量保证每一列的数据类型相同
- 表格或列表的前面，用一句话来介绍上下文

## 段落（Paragraphs）

- 以中心句开头。
- 每段只围绕一个主题写作，不要包含其他段落中出现的主题内容。
- 三到五句话一段，不要超过七句。
- 段落能够解释清楚三件事： what，why，how。

## 读者（Audience）

> 好的文档 = 读者要完成任务所需的知识和技能 - 读者已有的知识和技能

- 定义读者的身份（开发者、科学家、技术经理、未毕业的工程专业学生、毕业生、非技术人员……）。
- 了解目标读者对不同知识的掌握程度。
- 确定读者需要什么，读过文档能学到什么。比如在设计规范开头这样写：
  {{< admonition tip "举例">}}
  After reading the design spec, the audience will learn the following: …
  {{< /admonition >}}

- 满足读者：
  - 解释必要的词汇和概念。
  - 对新手友好。
  - 使用简单的英语词汇。
  - 对不同文化、语言环境的读者友好，避免使用成语或俗语。

## 文档（Documents）

- 声明文档的适用场景（scope）。
  - 最好能声明哪些场景不适用（non-scope），不适合哪些读者阅读。这不仅对读者有用，对写作者也能限制其写作的范围。
- 声明目标读者。
  - 最好能指出读者在阅读前应该具备的知识和经验。
- 在开头部分概括文档的关键点
  - 可以通过比较、对比旧观点的手法，让读者明白你要表达的新观点。
- 按读者需要组织文档格式。
  {{< admonition tip "好的大纲举例" >}}

  1.  Overview of the algorithm
      - Compare and contrast with quicksort, including Big O comparisons
        - Link to Wikipedia article on quicksort
      - Optimal datasets for the algorithm
  2.  Implementing the algorithm
      - Implementation in pseudocode
      - Implementation tips, including common mistakes
  3.  Deeper analysis of algorithm - Edge cases - Known unknowns

  {{< /admonition >}}

## 标点符号（Punctuation）

{{< admonition note "Note" >}}

这部分原文涉及英文标点符号的用法，大部分和汉语规则近似，略过不译。以下是我在排版方面的经验：
大多数中国人对英文排版易错的地方是空格的滥用。可以参考这篇文章： [英文标点要如何排版？](https://zhuanlan.zhihu.com/p/110266694)。

{{< /admonition >}}

概括起来：

- `, ; : . ? !` 这些符号后加空格
- `() '' ""` 这些成对的符号左右加空格，内部不加空格
- `/ - _`不加空格

## 总结

- 统一使用术语。
- 避免模棱两可的代名词。
- 主动语态优于被动语态。
- 选择具体的动词而不是模糊的动词。
- 每句话集中在一个想法上。
- 将一些长句子转化为列表。
- 消除不必要的词。
- 有顺序时使用有序（数字）列表，无顺序时使用无序（圆点）列表。
- 保持列表项目平行（概念层次相同）。
- 用祈使（命令性）的词作为有序列表项的开头。
- 适当地介绍列表和表格。
- 开宗明义，明确段落的中心点。
- 将每一段落集中在一个主题上。
- 确定你的读者需要学习什么。
- 使文档适应读者。
- 在文档的开头指出关键信息。

## 延伸阅读资料

- [Docs for Developers](https://docsfordevelopers.com/)
- [Software Engineering at Google](https://www.oreilly.com/library/view/software-engineering-at/9781492082781/)
- [Gitlab Technical Writing Fundamentals courese](https://about.gitlab.com/handbook/engineering/ux/technical-writing/fundamentals/)
