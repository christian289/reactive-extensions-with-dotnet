### Chapter 16: 성능 최적화

**메모리 누수 방지:**

```csharp
// BAD: 메모리 누수
public class BadViewModel
{
    public BadViewModel()
    {
        Observable.Interval(TimeSpan.FromSeconds(1))
            .Subscribe(x => DoSomething(x));  // Dispose 안함!
    }
}

// GOOD: 적절한 정리
public class GoodViewModel : IDisposable
{
    private readonly CompositeDisposable _disposables = new CompositeDisposable();

    public GoodViewModel()
    {
        Observable.Interval(TimeSpan.FromSeconds(1))
            .Subscribe(x => DoSomething(x))
            .DisposeWith(_disposables);  // 자동 정리
    }

    public void Dispose() => _disposables.Dispose();
}
```

**연산자 순서 최적화:**

```csharp
// BAD: 비효율적
Observable.Range(1, 1000000)
    .Select(x => ExpensiveOperation(x))  // 100만번 실행
    .Take(10);  // 10개만 필요

// GOOD: 효율적
Observable.Range(1, 1000000)
    .Take(10)  // 먼저 10개만 선택
    .Select(x => ExpensiveOperation(x));  // 10번만 실행
```

---
