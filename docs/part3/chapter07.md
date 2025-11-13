### Chapter 7: 필터링(Filtering) 연산자

#### 7.1 조건 기반 필터링

**[Where](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.where) - 조건 필터:**

```csharp
Observable.Range(1, 10)
    .Where(x => x % 2 == 0)
    .Subscribe(x => Console.Write($"{x} "));
// 출력: 2 4 6 8 10
```

**[Take](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.take) / [Skip](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.skip):**

```csharp
// 처음 3개만
Observable.Range(1, 10).Take(3)
    .Subscribe(x => Console.Write($"{x} "));
// 출력: 1 2 3

// 처음 3개 건너뛰기
Observable.Range(1, 10).Skip(3)
    .Subscribe(x => Console.Write($"{x} "));
// 출력: 4 5 6 7 8 9 10

// 페이지네이션
int pageSize = 5;
int pageNumber = 2;
items.Skip((pageNumber - 1) * pageSize).Take(pageSize);
```

#### 7.2 중복 제거와 샘플링

**[Distinct](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.distinct) / [DistinctUntilChanged](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.distinctuntilchanged):**

```csharp
// 중복 제거
var values = new[] { 1, 2, 2, 3, 3, 3, 1, 2 };
Observable.ToObservable(values)
    .DistinctUntilChanged()  // 연속된 중복만 제거
    .Subscribe(x => Console.Write($"{x} "));
// 출력: 1 2 3 1 2
```

**[Throttle](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.throttle) ([Debounce](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.debounce)) - 이벤트 제한:**

```csharp
// 실시간 검색: 입력이 멈춘 후 300ms 대기
searchTextBox.TextChanged
    .Throttle(TimeSpan.FromMilliseconds(300))
    .DistinctUntilChanged()
    .Subscribe(text => PerformSearch(text));
```

**[Sample](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.sample) - 주기적 샘플링:**

```csharp
// 1초마다 최신 값만 가져오기
fastChangingValue
    .Sample(TimeSpan.FromSeconds(1))
    .Subscribe(value => UpdateUI(value));
```
