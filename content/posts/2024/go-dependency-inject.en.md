---
title: "Dependency Inversion in Go"
slug: "go-dependency-inject"
date: 2024-11-21T11:26:22+08:00
categories: [Software Architecture]
tags: [go]
aliases: [/posts/go-dependency-inject/]
description: ""
---
> This article is fairly basic; it was material I used when training Java programmers in Go.

## Why Dependency Inversion Principle (DIP)?

[Dependency Inversion](https://en.wikipedia.org/wiki/Dependency_inversion_principle), also called dependency inversion or DIP, is a very important design principle in software development. Many programmers have never learned about it, or only know the general idea from Java Spring. Today I'd like to use a brief article and a simple Go example to explain how to implement dependency inversion in the simplest way.

If you don't yet know what it is, you can refer to the description in Wikipedia, or read [Martin Fowler's article on DIP](https://martinfowler.com/articles/dipInTheWild.html).

The Dependency Inversion Principle addresses a common risk in software development: dependency.

Try to recall:

1. When you try to use mocks to shield underlying details for testing, you find that the class you want to test references a large number of framework-provided interfaces, requiring you to mock many underlying implementations.
2. When you try to modify an old low-level class, but there are too many upper-layer service classes depending on it, you worry about side effects while refactoring the upper-layer code at every dependency point.

Let's analyze these two scenarios:

In scenario 1, the application class depends on the implementation provided by the framework, making it difficult to separate the application class from the framework. The industry method for dealing with this problem is called **Inversion of Control** (IoC). The application class should not depend on the framework; instead, the framework provides slots, registering the application class with the framework, and the framework uniformly dispatches the application to execute the corresponding methods.

In scenario 2, the service class depends on the low-level class, making modifications to the low-level class increasingly difficult. The solution is **Dependency Injection** (DI). The upper-layer class does not directly reference the low-level class, but instead, the low-level class on which the upper-layer class depends is injected at the point of use.

Combining these two scenarios captures the core of the Dependency Inversion Principle:

- High-level modules should not depend on low-level modules; both should depend on abstractions.
- Abstractions should not depend on details. Details should depend on abstractions.

These two principles ensure high cohesion and low coupling among modules, while also creating the conditions for mocking and iteratively updating modules.

## Implementing It in Go

Suppose we need to query user information from a user service. There are two interfaces: `UserRepository` serves as the data layer responsible for querying the database, and `UserService` handles business logic and depends on `UserRepository`. At the same time, to facilitate testing, we also need to write a mock data layer implementation. The entire structure is shown in the figure below.

![Go example](/images/go-dependency-inject/example.png)

Next, very easily, we implement the two interfaces and write their implementation classes. At the same time, we also write a `NewUserService` in the `UserService` implementation class to inject the `UserRepository` implementation it depends on.

```go
// Implement the specific interface in user_repository.go
type UserRepository interface {
    GetByID(id int) (*User, error)
    Save(user *User) error
}

// ... specific implementation of UserRepository, omitted

// Implemented in user_service.go
type UserService interface {
    GetUser(id int) (*User, error)
    CreateUser(name string, age int) error
}

// ... specific implementation of UserService, omitted

func NewUserService(repo UserRepository) UserService {
    return &UserServiceImpl{
        repo: repo,
    }
}
```

So the question arises: can we directly reference the repository in `user_service.go`? Obviously not, because this would create a dependency between the two modules.

This is the core of dependency inversion: the upper-layer module does not directly reference the lower-layer module; instead, the executing class initializes the Service and injects the dependent lower-layer service.

```go
// In main.go
func main() {
    repo := &MySQLUserRepository{}
    userService := NewUserService(repo)
}
```

This way, when writing test mock code, you don't need to modify any code logic. You can simply replace the parameter of `NewUserService` in the test with a fake test instance.

```go
// In user_service_test.go
func TestUserService() {
    repo := &MockTestUserRepository{}
    userService := NewUserService(repo)
}
```

In addition, if the data layer changes its implementation or migrates to another database, you only need to modify two places: the data layer's implementer and the dependency injector. The caller `UserService` is completely unaffected. The entire project won't form a dependency trap.

## Summary

The two core principles of the Dependency Inversion Principle:

- Modules do not depend on other modules, but both depend on abstract interfaces.
- Abstract interfaces do not depend on implementations; implementations depend on abstract interfaces.

Implementing these two principles in Go isn't difficult—you just need to transform the original caller-implementer relationship into a registrar-caller-implementer relationship. There are also some libraries and frameworks in Go that implement dependency inversion, but the core ideas are not different.
