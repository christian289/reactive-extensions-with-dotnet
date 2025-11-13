### Chapter 9: 집계(Aggregation) 연산자

**기본 집계 ([Count](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.count), [Sum](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.sum), [Average](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.average)):**

```csharp
Observable.Range(1, 5)
    .Sum()
    .Subscribe(sum => Console.WriteLine($"Sum: {sum}"));  // 15

Observable.Range(1, 5)
    .Average()
    .Subscribe(avg => Console.WriteLine($"Average: {avg}"));  // 3
```

**[Aggregate](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.aggregate) (Reduce) - 커스텀 집계:**

```csharp
Observable.Range(1, 5)
    .Aggregate((acc, x) => acc * x)  // 팩토리얼
    .Subscribe(result => Console.WriteLine($"5! = {result}"));  // 120
```

**조건부 집계 ([Any](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.any), [All](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.all)):**

```csharp
// 짝수가 하나라도 있는지
Observable.Range(1, 10)
    .Any(x => x % 2 == 0)
    .Subscribe(result => Console.WriteLine($"Has even: {result}"));  // True

// 모두 양수인지
Observable.Range(1, 10)
    .All(x => x > 0)
    .Subscribe(result => Console.WriteLine($"All positive: {result}"));  // True
```
