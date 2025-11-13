### Chapter 8: 결합(Combining) 연산자

#### 8.1 순차적 결합

**[Concat](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.concat) - 순차 연결:**

```csharp
var first = Observable.Range(1, 3);
var second = Observable.Range(4, 3);
first.Concat(second)
    .Subscribe(x => Console.Write($"{x} "));
// 출력: 1 2 3 4 5 6
```

**[StartWith](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.startwith) - 초기값 추가:**

```csharp
Observable.Range(1, 5)
    .StartWith(0)
    .Subscribe(x => Console.Write($"{x} "));
// 출력: 0 1 2 3 4 5
```

#### 8.2 동시적 결합

**[Merge](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.merge) - 병합:**

```csharp
var stream1 = Observable.Interval(TimeSpan.FromSeconds(1)).Select(x => $"A{x}");
var stream2 = Observable.Interval(TimeSpan.FromSeconds(1.5)).Select(x => $"B{x}");

stream1.Merge(stream2)
    .Take(10)
    .Subscribe(x => Console.WriteLine($"{DateTime.Now:ss.fff} - {x}"));
```

**[Zip](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.zip) - 쌍으로 조합:**

```csharp
var numbers = Observable.Range(1, 5);
var letters = Observable.ToObservable(new[] { "A", "B", "C", "D", "E" });

numbers.Zip(letters, (num, letter) => $"{num}{letter}")
    .Subscribe(x => Console.Write($"{x} "));
// 출력: 1A 2B 3C 4D 5E
```

**[CombineLatest](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.combinelatest) - 최신 값 조합:**

```csharp
// UI 예제: 여러 필드의 유효성 검사
var usernameValid = usernameTextBox.TextChanged
    .Select(text => text.Length >= 3);

var passwordValid = passwordTextBox.TextChanged
    .Select(text => text.Length >= 8);

usernameValid.CombineLatest(passwordValid, (u, p) => u && p)
    .Subscribe(isValid => submitButton.Enabled = isValid);
```

#### 8.3 조건부 결합

**[Amb](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.amb) - 가장 빠른 것 선택:**

```csharp
// 여러 서버 중 가장 빠른 응답 사용
var server1 = GetDataFromServer("server1.com");
var server2 = GetDataFromServer("server2.com");
var server3 = GetDataFromServer("server3.com");

Observable.Amb(server1, server2, server3)
    .Subscribe(data => Console.WriteLine($"Fastest response: {data}"));
```

**[Switch](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.switch) - 최신 스트림으로 전환:**

```csharp
// 검색어가 변경되면 이전 검색 취소
searchQuery
    .Select(query => PerformSearchAsync(query))  // Observable<Observable<Result>>
    .Switch()  // 최신 검색 결과만 사용
    .Subscribe(results => DisplayResults(results));
```
