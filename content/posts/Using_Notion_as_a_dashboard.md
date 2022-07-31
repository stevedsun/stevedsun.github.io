---
title: "Notion as a dashboard"
date: 2022-07-31T21:01:56+08:00
description: "Using Notion as the backend service's dashboard."
tags: [Notion]
---

I have built a Chrome extension [无用主意](https://chrome.google.com/webstore/detail/%E6%97%A0%E7%94%A8%E4%B8%BB%E6%84%8F%E6%A0%87%E7%AD%BE%E9%A1%B5/lieiofhdejclfpflofeooilpeaphlcgd?hl=zh-CN) during the last month. The backend service which implemented by Flask is using Notion as a dashboard.

![](https://raw.githubusercontent.com/stevedsun/images/main/20220731212027.png)

## Notion API

If you want your service to connect Notion, you have to create a Notion integration at [this page](https://www.notion.so/my-integrations). Afterwards, you have to share a specific Notion page to the integration you just created.

![](https://raw.githubusercontent.com/stevedsun/images/main/20220731213331.png)

Now, you can call [Notion API](https://developers.notion.com/reference/intro) to visit your page.

Once the service has permission to write and read data to Notion page, we can sync data between Notion and Flask service.

I'm using a `status` column to let me know which row has been updated into service's sqlite database.

![](https://raw.githubusercontent.com/stevedsun/images/main/20220731212654.png)

And also, I can update this row's content, then mark `status` as "To Update" to tell Flask service to sync this line later. At every night, Flask service sync data from Notion page to sqlite and mark `status` as "Done".

By this way, I am making Notion as my backend service dashboard.









