---
title: "User Story Mapping"
slug: "user-story-mapping"
date: 2023-04-07T06:37:53+08:00
categories: [Agile]
tags: [agile, user-story]
aliases: [/posts/user-story-mapping/]
description: ""
---
> A user story is a common term in software development and project management. Its purpose is to express functionality in everyday or business language—a simple description of a feature. Written from the customer's or user's point of view, it captures valuable features, guidance, and frameworks to interact with users, thereby driving work forward. It can be seen as a kind of specification document, but more precisely, it represents the customer's needs and direction.

During the requirements analysis phase of agile development, you use process tools such as **user story mapping** to transform those abstract, vague user requirements into concrete, prioritized, modularized user stories.

A user story map looks like this.

![](/images/user-story-mapping/user-story.png)

## The Process of Drawing a User Story Map

Drawing a user story map should follow a few basic principles:

1. Think and record at the same time; visualize every step on sticky notes
2. Focus on the whole; don't get lost in details too early
3. Prioritize by **outcome**, not by feature
4. Verify that the problem the product is solving truly exists
5. Use concrete solutions, such as high-fidelity prototypes or hand-drawn sketches
6. Validate ideas with prototypes and user testing
7. The goal of a user story map is to enable the team to communicate effectively, raise questions, and estimate effort
8. The more frequently you measure effort during estimation, the more accurate you'll be

### Use Goal-Level Hierarchy

When breaking down user stories, follow the principle of layer-by-layer decomposition. Each layer should focus on the granularity of that layer's tasks; don't dive into details too early.

First, set the macro-level **activities**. For example, break down user needs into several large activities, such as viewing accounts, depositing money, and so on.

Next, lay out the **main backbone stories**. For each activity, break it down into individual steps—these steps are the backbone stories. Each backbone story:

1. Is a verb phrase
2. Stories should stay at the same level of granularity as each other
3. Are arranged from left to right in chronological order; any intermediate steps you think of can be inserted or reordered at any time

Third, for each backbone story, brainstorm to add more smaller user stories, written on sticky notes and placed below.

Finally, by priority, put the important user stories on top and the less important ones at the bottom. Then draw horizontal swim lanes to divide the stories into different stages based on specific **target outcomes**.

![](/images/user-story-mapping/user-story-2.png)

For example, if the first stage completes the basic functionality, then all the user stories in the top horizontal row are what the first release needs to deliver.

This completes the design of the user stories. Let's recap the process:

1. Identify the key activities
2. Lay out the backbone stories
3. Refine the user stories
4. Team brainstorming to add missing user stories
5. Prioritize from top to bottom
6. Cut the user stories horizontally to define each iteration's work and key outcomes

## Applying Design Thinking

The process for drawing user stories is outlined above, but in fact the hardest part is finding the real user needs. To uncover valuable needs from customers or users in a specific domain, **Design Thinking** is typically used to help the team communicate and find the focus problem.

![](/images/user-story-mapping/design-thinking.png)

Design Thinking has five steps.

- **Empathize**: Communicate and find the problem.
- **Define**: Narrow down to a few important problems and elaborate.
- **Ideate**: Come up with multiple solutions for each problem.
- **Prototype**: Build concrete, visual prototypes.
- **Test**: Test with users and gather feedback.

## Forming a Discovery Team

A discovery team consists of three key roles:

- A Product Owner who understands the product and the requirements
- A UX Designer who understands design and interaction
- A Senior Developer who understands the technology

The early discovery phase should be carried out by a team of no more than five people, and you should avoid **design by committee** (i.e., most of the team joining the design process, which leads to chaos and inconsistency).

When prioritizing tasks in the early phase, the following priority should be observed:

> Business goals > Customer/user goals > Features
