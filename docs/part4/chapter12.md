### Chapter 12: 시간 기반 연산자

**Buffer/Window with Time:**

```csharp
// 5초마다 배치 처리
Observable.Interval(TimeSpan.FromMilliseconds(100))
    .Buffer(TimeSpan.FromSeconds(5))
    .Subscribe(list => Console.WriteLine($"Received {list.Count} items"));
```
