---
title: "Notes on the RESTful Web Services Cookbook"
slug: "restful-api-cookbook"
date: 2024-07-13T16:12:34+08:00
categories: [Software Architecture]
tags: [api]
aliases: [/posts/restful-api-cookbook/]
description: "Highlights and lesser-known details from the RESTful Web Services Cookbook."
---

[RESTful Web Services Cookbook](https://www.oreilly.com/library/view/restful-web-services/9780596809140/) is a short, concise guide to designing RESTful APIs. This post (notes) records the key points from the book.

> Since RESTful conventions are second nature to most backend developers, I will skip the well-known parts and focus on the details in the book that many developers tend to overlook.

## HTTP Methods

### GET

Performs **safe** and **idempotent** retrieval of information.

### POST

The target of execution is a collection of resources (a factory), not a specific URI.

Use cases:

- Create a new resource by treating a resource as a factory.
- Modify one or more resources through a controller resource.
- Execute queries that require a large data input (many parameters).
- **When no other HTTP method seems appropriate, perform an unsafe or non-idempotent operation.**

Approach:

- Designate an existing resource as the factory for creating new resources. Although any resource can be used as a factory, the common practice is to use a collection resource.
- Have the client submit a POST request to the factory resource, attaching a representation of the resource to be created. Through the optional **Slug** header, the client can suggest a name to the server as part of the URI of the created resource.
- After the resource is created, return response code **201 (Created)** and include the URI of the new resource in the **Location** header.
- If the response body contains a full representation of the new resource, include the URI of the new resource in the **Content-Location** header.

### PUT

Only use PUT to create a new resource when the client controls the structure of the URI. **In other words, PUT can also create a resource, but only when the client specifies the URI.**

## Determining the Granularity of Resource Objects

Resources should be designed to match the client's usage patterns, not based on existing database or object models.

- Cacheability
- Reduce modification frequency
- Mutability — separate mutable from immutable data

### How to Design Composite Resources?

**Composite resources** reduce the visibility of the uniform interface because their representations contain data that overlaps with other resources.

- If composite resources are used **infrequently**, consider using **caching** instead.
- Consider the network overhead — would a composite resource reduce server throughput and increase latency?

## HTTP Body

Taking a JSON body as an example:

1. It is best to include a self-referential link.
2. If the results are paginated, it is best to include a link to the next page.
3. If the results are paginated, indicate the size of the collection (the total).
4. If the queried object is localized, add a property to indicate the language of the localized content.

```json
{
  "name": "John",
  "id": "urn:example:user:1234",
  "link": {
    "rel": "self",
    "href": "http://www.example.org/person/john"
  },
  "address": {
    "id": "urn:example:address:4567",
    "link": {
      "rel": "self",
      "href": "http://www.example.org/person/john/address"
    }
  }
}
```

## HTTP Response

1. For client errors, return a 4xx status code plus a Date (the time the error occurred).
2. For server errors, return a 5xx status code plus a Date (the time the error occurred).
3. The body should describe the error. If there are external documents and links for reference, provide a Link header or include the link directly in the body.
4. To support later tracing and analysis, errors are logged on the server. Provide an identifier or link that can be used to locate the error.

## Designing the Query Structure

### Designing Query Requests

1. To improve caching and performance, try to avoid range queries. Workarounds include:
   - Use predefined queries
   - Alternatively, use the HTTP header: Range
2. Avoid using general-purpose query languages (SQL, XPATH).
3. Avoid tight coupling between the URI and the underlying data storage (treating the backend as a database on the front end).
4. For requests with many parameters, consider using POST (since URIs have a maximum length)
   - The downside of a POST interface is that it loses caching ability
   - POST requests are not cacheable, so the Cache-Control and Expires headers are useless
   - To solve the caching problem, have the POST create a temporary resource, return the link to the client, and let the client use GET to fetch that resource next time

### Designing Query Response Results

1. Return a collection. Add appropriate cache expiration headers.
2. If there are no results, return an **empty collection**.
