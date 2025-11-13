### Chapter 10: 에러 처리와 복구

#### 10.1 에러 처리 전략

**[Catch](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.catch) - 에러 처리:**

```csharp
// 에러 발생 시 대체 Observable 사용
var primary = GetDataFromPrimarySource();
var fallback = GetDataFromFallbackSource();

primary.Catch(fallback)
    .Subscribe(data => Console.WriteLine(data));

// 에러 무시하고 계속
sequence.Catch(Observable.Empty<int>())
    .Subscribe(x => Console.WriteLine(x));
```

**OnErrorResumeNext - 에러 후 계속:**

```csharp
var sources = new[]
{
    Observable.Throw<int>(new Exception("Error 1")),
    Observable.Range(1, 3),
    Observable.Throw<int>(new Exception("Error 2")),
    Observable.Range(4, 3)
};

Observable.OnErrorResumeNext(sources)
    .Subscribe(
        x => Console.WriteLine(x),
        ex => Console.WriteLine($"Error: {ex.Message}"),
        () => Console.WriteLine("Completed"));
// 출력: 1 2 3 4 5 6 Completed (에러 무시)
```

#### 10.2 재시도 메커니즘

**[Retry](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.retry) - 자동 재시도:**

```csharp
// 최대 3번 재시도
unreliableOperation
    .Retry(3)
    .Subscribe(
        result => Console.WriteLine($"Success: {result}"),
        ex => Console.WriteLine($"Failed after 3 retries: {ex.Message}"));

// 지수 백오프로 재시도
unreliableOperation
    .RetryWhen(errors =>
        errors.SelectMany((ex, attempt) =>
            Observable.Timer(TimeSpan.FromSeconds(Math.Pow(2, attempt)))))
    .Subscribe(result => Console.WriteLine(result));
```

#### 10.3 리소스 관리

**[Using](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.using) - 리소스 자동 정리:**

```csharp
var data = Observable.Using(
    () => new StreamReader("data.txt"),  // 리소스 생성
    reader => Observable.Generate(
        reader,
        r => !r.EndOfStream,
        r => r,
        r => r.ReadLine()));

data.Subscribe(Console.WriteLine);
// 완료 후 StreamReader 자동으로 Dispose
```

**[Finally](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.finally) - 완료/에러 시 작업:**

```csharp
sequence
    .Finally(() => Console.WriteLine("Cleanup"))
    .Subscribe(
        x => Console.WriteLine(x),
        ex => Console.WriteLine($"Error: {ex.Message}"),
        () => Console.WriteLine("Completed"));
// 완료 또는 에러 발생 시 Finally 블록 실행
```

---
