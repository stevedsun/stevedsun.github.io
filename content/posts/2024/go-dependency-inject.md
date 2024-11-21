---
title: "Go 语言的依赖倒置"
date: 2024-11-21T11:26:22+08:00
categories: [Cloud Native Computing]
tags: [go]
aliases: [/posts/go-dependency-inject/]
description: ""
---

> 这篇文章比较基础，是我在给 Java 程序员做 go 语言培训时用到的。

## 为什么要做依赖倒置（DIP）？

[依赖倒置](https://en.wikipedia.org/wiki/Dependency_inversion_principle)，或叫依赖反转、DIP，是软件开发非常重要的设计原则。很多程序员没有了解过相关知识，或者只从 Java Spring 知道大致思想。我今天想用一篇简短的文章，用 Go 语言做一个简单的例子，讲解一下怎么最简单地实现依赖倒置。

如果你还不知道它是什么，可以参考 wiki 中的描述，或者阅读[马丁福勒关于 DIP 的文章](https://martinfowler.com/articles/dipInTheWild.html)。

依赖倒置原则要解决一个软件开发中常见的风险：依赖。

尝试回忆一下：

1. 当你尝试通过 Mock 方式屏蔽底层细节做测试时，你发现你要测试的类引用了大量框架提供的接口，导致你需要 mock 大量底层的实现。
2. 当你尝试修改一个旧的底层类，但是依赖该类的上层服务类太多，你一边担心造成副作用，一边在所有依赖的位置重构上层代码。

我们分析一下这两个场景：

场景 1 里，应用类依赖于框架提供的实现，导致应用类很难从框架上剥离出来，业内处理这种问题的方法叫**控制反转**（IoC, Inversion of Control）。即应用类不应该依赖框架，而是框架提供插槽一样，把应用类注册给框架，由框架统一调度应用，执行对应的方法。

场景 2 里，服务类依赖底层类，导致底层修改难度越来越大。解决办法是**依赖注入**（DI, Dependency Injection）。即上层类不直接引用底层类，而是在使用的地方把上层类依赖的底层类注入进来。

把这两个场景结合起来，就是依赖倒置原则的核心：

- 高层次的模块不应该依赖于低层次的模块，两者都应该依赖于抽象接口。
- 抽象接口不应该依赖于具体实现。而具体实现则应该依赖于抽象接口。

这两个原则保证了代码中模块的高内聚、低耦合，同时给 Mock、迭代更新模块创造了条件。

## 用 Go 语言实现它

假设现在要从一个用户的服务中查询用户的信息。有两个接口，UserRepository 作为数据层负责查询数据库， UserService 负责业务逻辑，它依赖 UserRepository。同时为了方便测试，我们还要写一个 Mock 的数据层实现。 整个结构如下图。

![Go example](/images/go-dependency-inject/example.png)

接下来非常轻松地，我们实现两个接口，并写了他们的实现类。同时我们还在 UserService 的实现类里写了一个 NewUserService，来把它依赖的 UserRepository 实现注入进来。

```go
// 在 user_repository.go 中实现具体的接口
type UserRepository interface {
    GetByID(id int) (*User, error)
    Save(user *User) error
}

// ... 具体实现 UserRepository，略

// user_service.go 中实现
type UserService interface {
    GetUser(id int) (*User, error)
    CreateUser(name string, age int) error
}

// ... 具体实现 UserService，略

func NewUserService(repo UserRepository) UserService {
    return &UserServiceImpl{
        repo: repo,
    }
}
```

那么问题来了，可不可以直接在 `user_service.go` 中直接把 repository 引用进来呢？显然不行，因为这样，两个模块就形成了依赖关系。

这一点是依赖反转的核心，上层模块不直接引用下层模块，而是由执行的类来初始化 Service 并将依赖的下层服务注入进来。

```go
// 在main.go 中
func main() {
    repo := &MySQLUserRepository{}
    userService := NewUserService(repo)
}
```

这样，当编写测试 Mock 代码时，不需要修改任何代码逻辑，直接在测试中将`NewUserService` 的参数替换成测试的假实例即可。

```go
// 在 user_service_test.go 中
func TestUserService() {
    repo := &MockTestUserRepository{}
    userService := NewUserService(repo)
}
```

另外，如果数据层修改了实现，或者迁移到另外的数据库，你只需要修改两个地方：数据层的实现者和依赖注入者。对于调用者 `UserService` 则完全不受到影响。整个项目也不会形成依赖陷阱。

## 总结

依赖倒置原则的两个核心原则：

- 模块不依赖于其他模块，而是都依赖于抽象接口
- 抽象接口不依赖于实现，而实现依赖于抽象接口

在 Go 语言中实现这两条原则并不麻烦，只要将原本的调用方-实现方，转换成注册方-调用方-实现方。在 Go 中也有一些库和框架实现依赖反转，其实核心思想并没有差异。
