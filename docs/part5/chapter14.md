### Chapter 14: 함수형 반응형 프로그래밍 (FRP)

**[불변성](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/functional/immutable) 원칙:**

```csharp
// 불변 객체 사용
public record StockPrice(string Symbol, decimal Price, DateTime Timestamp);

var prices = Observable.Interval(TimeSpan.FromSeconds(1))
    .Select(i => new StockPrice("AAPL", 150 + i, DateTime.Now));
```

**Observable as Monad:**

```csharp
// Functor (Select)
IObservable<int> numbers = Observable.Range(1, 5);
IObservable<int> doubled = numbers.Select(x => x * 2);  // fmap

// Monad (SelectMany)
IObservable<User> users = userIds.SelectMany(id => GetUserAsync(id));  // bind
```
