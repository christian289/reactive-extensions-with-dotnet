### Chapter 6: 변환(Transformation) 연산자

#### 6.1 기본 변환 연산자

**[Select](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.select) (Map) - 각 요소 변환:**

```csharp
// 간단한 변환
Observable.Range(1, 5)
    .Select(x => x * x)
    .Subscribe(x => Console.Write($"{x} "));
// 출력: 1 4 9 16 25

// 객체로 변환
Observable.Range(1, 3)
    .Select(x => new { Number = x, Square = x * x, Cube = x * x * x })
    .Subscribe(obj => Console.WriteLine($"Number: {obj.Number}, Square: {obj.Square}, Cube: {obj.Cube}"));
```

**[SelectMany](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.selectmany) (FlatMap) - 평탄화:**

```csharp
// 비동기 작업 평탄화
var userIds = Observable.Range(1, 3);
userIds
    .SelectMany(id => GetUserAsync(id))  // 각 ID를 Observable<User>로 변환 후 평탄화
    .Subscribe(user => Console.WriteLine($"User: {user.Name}"));

// 여러 Observable을 하나로
var nested = Observable.Range(1, 3)
    .Select(x => Observable.Range(x, 3));  // Observable<Observable<int>>

nested.SelectMany(inner => inner)  // Observable<int>로 평탄화
    .Subscribe(x => Console.Write($"{x} "));
// 출력: 1 2 3 2 3 4 3 4 5
```

**Cast / [OfType](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.oftype) - 타입 변환/필터:**

```csharp
var mixed = new object[] { 1, "two", 3, "four", 5 };
Observable.ToObservable(mixed)
    .OfType<int>()  // int만 필터링
    .Subscribe(x => Console.WriteLine(x));
// 출력: 1, 3, 5
```

#### 6.2 고급 변환 패턴

**[Scan](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.scan) - 누적 계산:**

```csharp
// 누적 합계
Observable.Range(1, 5)
    .Scan((acc, x) => acc + x)
    .Subscribe(x => Console.Write($"{x} "));
// 출력: 1 3 6 10 15

// 실용 예제: 실시간 주식 포트폴리오 가치
stockPrices
    .Scan(0m, (total, price) => total + price.Value)
    .Subscribe(total => Console.WriteLine($"Portfolio value: ${total}"));
```

**[GroupBy](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.groupby) - 그룹핑:**

```csharp
Observable.Range(1, 10)
    .GroupBy(x => x % 3)  // 3으로 나눈 나머지로 그룹화
    .SelectMany(group =>
        group.Select(x => $"Key: {group.Key}, Value: {x}"))
    .Subscribe(Console.WriteLine);
```

**[Buffer](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.buffer) / [Window](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.window) - 배치 처리:**

```csharp
// Buffer: 요소를 리스트로 모음
Observable.Range(1, 10)
    .Buffer(3)  // 3개씩 묶음
    .Subscribe(list => Console.WriteLine($"[{string.Join(", ", list)}]"));
// 출력: [1, 2, 3], [4, 5, 6], [7, 8, 9], [10]

// Window: 요소를 Observable로 그룹화
Observable.Range(1, 10)
    .Window(3)
    .SelectMany(window => window.ToList())
    .Subscribe(list => Console.WriteLine($"Window: [{string.Join(", ", list)}]"));
```
