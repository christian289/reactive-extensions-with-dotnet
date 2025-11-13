### Chapter 11: Scheduling과 동시성

#### 11.1 Scheduler 타입과 특징 (Chapter 3.3에서 상세 설명됨)

**[Delay](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.delay) - 시간 지연:**

```csharp
// 모든 값을 3초 지연
Observable.Range(1, 5)
    .Delay(TimeSpan.FromSeconds(3))
    .Timestamp()
    .Subscribe(x => Console.WriteLine($"{x.Timestamp:ss.fff} - {x.Value}"));
```

**[Timeout](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.timeout) - 시간 초과:**

```csharp
// 5초 안에 응답 없으면 에러
slowOperation
    .Timeout(TimeSpan.FromSeconds(5))
    .Subscribe(
        result => Console.WriteLine($"Success: {result}"),
        ex => Console.WriteLine("Timeout!"));
```
