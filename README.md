# Reactive Extensions(Rx.NET) 완벽 가이드
### 초보자부터 실무까지의 반응형 프로그래밍 여정

---

## 📘 Part 1: 기초 개념과 철학

### Chapter 1: Reactive Extensions 소개

#### 1.1 Reactive Programming이란 무엇인가?

**반응형 프로그래밍 패러다임의 이해**

[Reactive Programming](https://learn.microsoft.com/en-us/dotnet/api/system.reactive)은 데이터 스트림과 변화의 전파를 중심으로 하는 프로그래밍 패러다임입니다. 전통적인 프로그래밍에서는 변수에 값을 할당하면 그 값이 고정되지만, 반응형 프로그래밍에서는 시간에 따라 변하는 값들의 스트림을 다룹니다.

예를 들어, 엑셀의 수식을 생각해보세요:
- 셀 C1에 `=A1+B1`이라는 수식이 있다면
- A1이나 B1의 값이 변경될 때마다 C1은 자동으로 재계산됩니다
- 이것이 바로 반응형 프로그래밍의 핵심 개념입니다

```csharp
// 전통적인 방식
int a = 1;
int b = 2;
int c = a + b;  // c = 3
a = 10;         // c는 여전히 3

// Reactive 방식 (개념적)
IObservable<int> a = ...;
IObservable<int> b = ...;
IObservable<int> c = a.CombineLatest(b, (x, y) => x + y);
// a나 b가 변경되면 c도 자동으로 업데이트됨
```

**명령형 프로그래밍 vs 선언적 프로그래밍**

- **명령형 프로그래밍**: "어떻게(How)" 수행할지를 단계별로 명시
  ```csharp
  // 명령형: 1부터 10까지의 짝수를 찾아 제곱하기
  var result = new List<int>();
  for (int i = 1; i <= 10; i++)
  {
      if (i % 2 == 0)
      {
          result.Add(i * i);
      }
  }
  ```

- **선언적 프로그래밍**: "무엇을(What)" 원하는지를 명시
  ```csharp
  // 선언적: LINQ 사용
  var result = Enumerable.Range(1, 10)
      .Where(x => x % 2 == 0)
      .Select(x => x * x);

  // Rx는 이를 시간 차원으로 확장
  var result = Observable.Range(1, 10)
      .Where(x => x % 2 == 0)
      .Select(x => x * x);
  ```

**Push 모델 vs Pull 모델**

[IEnumerable<T>](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.ienumerable-1)와 [IObservable<T>](https://learn.microsoft.com/en-us/dotnet/api/system.iobservable-1)의 차이를 이해하는 것이 중요합니다:

| 특성 | Pull 모델 (IEnumerable) | Push 모델 (IObservable) |
|------|------------------------|------------------------|
| 데이터 흐름 | 소비자가 데이터를 요청 (Pull) | 생산자가 데이터를 전송 (Push) |
| 제어권 | 소비자가 제어 | 생산자가 제어 |
| 동기/비동기 | 주로 동기적 | 본질적으로 비동기적 |
| 시간 개념 | 시간 독립적 | 시간이 핵심 요소 |

```csharp
// Pull 모델: IEnumerable<T>
IEnumerable<int> numbers = GetNumbers();
foreach (var num in numbers)  // 소비자가 다음 항목을 요청
{
    Console.WriteLine(num);
}

// Push 모델: IObservable<T>
IObservable<int> numbers = GetNumbersAsync();
numbers.Subscribe(num =>      // 생산자가 데이터를 푸시
    Console.WriteLine(num));
```

#### 1.2 Rx.NET의 탄생 배경과 역사

**Observer 패턴의 한계**

[Observer 패턴](https://learn.microsoft.com/en-us/dotnet/standard/events/)은 .NET의 이벤트 시스템의 기반이지만, 여러 한계점이 있습니다:

1. **완료(Completion) 개념 부재**: 이벤트가 언제 끝나는지 알 수 없음
2. **에러 처리 부재**: 예외 처리를 위한 표준화된 방법이 없음
3. **구성 가능성 부족**: 여러 이벤트를 조합하거나 변환하기 어려움
4. **메모리 누수**: 이벤트 구독 해제를 잊기 쉬움

```csharp
// 전통적인 .NET 이벤트의 문제
button.Click += OnButtonClick;  // 구독
// ... 어딘가에서 구독 해제를 잊음
// button.Click -= OnButtonClick;  // 메모리 누수 발생!

// 여러 이벤트 조합이 복잡함
button1.Click += (s, e) => {
    button2.Click += (s2, e2) => {
        // 중첩된 이벤트 핸들러...
    };
};
```

**비동기 프로그래밍의 복잡성 해결**

Rx.NET은 2009년 Microsoft의 Erik Meijer와 그의 팀이 만들었습니다. [LINQ](https://learn.microsoft.com/en-us/dotnet/csharp/linq/)의 성공을 시간 차원으로 확장한 것으로, "LINQ to Events"라고도 불립니다.

주요 목표:
- 비동기 데이터 스트림을 동기 컬렉션처럼 쉽게 다루기
- 시간 기반 연산을 선언적으로 표현
- 복잡한 이벤트 조합을 간단하게 구성

#### 1.3 왜 Reactive Extensions를 사용해야 하는가?

**실시간 데이터 스트림 처리**

현대 애플리케이션은 다양한 실시간 데이터를 처리해야 합니다:
- 사용자 입력 (마우스, 키보드, 터치)
- 네트워크 요청/응답
- 센서 데이터 (IoT)
- 주식 시세, 암호화폐 가격
- 웹소켓 메시지

Rx.NET은 이러한 모든 데이터 소스를 일관된 방식으로 처리할 수 있게 해줍니다.

```csharp
// 실시간 검색: 사용자 입력 후 300ms 대기, 중복 제거, 검색 실행
searchTextBox.TextChanged
    .Select(evt => searchTextBox.Text)
    .Throttle(TimeSpan.FromMilliseconds(300))
    .DistinctUntilChanged()
    .SelectMany(query => SearchAsync(query))
    .ObserveOn(SynchronizationContext.Current)
    .Subscribe(results => UpdateUI(results));
```

**이벤트 기반 프로그래밍의 단순화**

전통적인 이벤트 처리:
```csharp
// 복잡하고 에러 발생하기 쉬운 코드
bool isDragging = false;
Point startPoint;

canvas.MouseDown += (s, e) => {
    isDragging = true;
    startPoint = e.Location;
};

canvas.MouseMove += (s, e) => {
    if (isDragging) {
        var delta = e.Location - startPoint;
        // 드래그 처리...
    }
};

canvas.MouseUp += (s, e) => {
    isDragging = false;
};
```

Rx를 사용한 선언적 접근:
```csharp
// 명확하고 간결한 코드
var drags = from mouseDown in canvas.MouseDownEvent()
            from mouseMove in canvas.MouseMoveEvent()
                                    .TakeUntil(canvas.MouseUpEvent())
            select new { Start = mouseDown.Location, Current = mouseMove.Location };

drags.Subscribe(drag => {
    var delta = drag.Current - drag.Start;
    // 드래그 처리...
});
```

**비동기 작업의 구성 가능성 (Composability)**

[Task](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.task)와 [async/await](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)는 단일 비동기 작업에는 훌륭하지만, 여러 작업을 조합할 때는 Rx가 더 강력합니다:

```csharp
// Task: 단일 비동기 작업에 적합
var result = await GetDataAsync();

// Observable: 여러 값의 스트림에 적합
IObservable<StockPrice> stockPrices = GetStockPriceStream();

// 강력한 조합 가능성
var portfolioValue = stockPrices
    .GroupBy(price => price.Symbol)
    .Select(group => group
        .CombineLatest(sharesOwned[group.Key], (price, shares) => price * shares))
    .Merge()
    .Scan((total, value) => total + value)
    .Sample(TimeSpan.FromSeconds(1));
```

### Chapter 2: 필수 기반 지식

#### 2.1 .NET의 비동기 프로그래밍 모델

**Task와 async/await 이해**

[Task<T>](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.task-1)는 .NET의 비동기 프로그래밍을 위한 핵심 타입입니다. Task는 단일 비동기 작업을 나타내며, 완료 시 하나의 결과 또는 예외를 반환합니다.

```csharp
// Task 기본 사용법
public async Task<string> FetchDataAsync()
{
    using var client = new HttpClient();
    string result = await client.GetStringAsync("https://api.example.com/data");
    return result;
}

// 호출 방법
string data = await FetchDataAsync();
```

**Task vs Observable 비교:**

```csharp
// Task: 단일 값, 한 번만 실행
Task<int> singleValue = Task.FromResult(42);
int result = await singleValue;  // 42를 한 번만 받음

// Observable: 여러 값, 스트림
IObservable<int> multipleValues = Observable.Range(1, 5);
multipleValues.Subscribe(x => Console.WriteLine(x));  // 1, 2, 3, 4, 5를 연속으로 받음
```

**이벤트와 델리게이트**

[이벤트](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/events/)는 .NET에서 관찰자 패턴을 구현하는 기본 메커니즘입니다. [델리게이트](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/delegates/)는 메서드에 대한 참조를 나타내는 타입입니다.

```csharp
// 델리게이트 정의
public delegate void PriceChangedHandler(decimal oldPrice, decimal newPrice);

// 이벤트 선언
public class Stock
{
    public event PriceChangedHandler PriceChanged;

    private decimal _price;
    public decimal Price
    {
        get => _price;
        set
        {
            if (_price != value)
            {
                decimal oldPrice = _price;
                _price = value;
                PriceChanged?.Invoke(oldPrice, value);
            }
        }
    }
}

// 이벤트 구독
var stock = new Stock();
stock.PriceChanged += (oldPrice, newPrice) =>
    Console.WriteLine($"Price changed from {oldPrice} to {newPrice}");
```

**Rx로 변환:**

```csharp
// 이벤트를 Observable로 변환
IObservable<(decimal Old, decimal New)> priceChanges =
    Observable.FromEventPattern<PriceChangedHandler, (decimal, decimal)>(
        h => stock.PriceChanged += h,
        h => stock.PriceChanged -= h)
    .Select(evt => evt.EventArgs);

// 이제 LINQ 연산자를 사용할 수 있음
priceChanges
    .Where(prices => Math.Abs(prices.New - prices.Old) > 10)  // 10 이상 변동만
    .Throttle(TimeSpan.FromSeconds(1))  // 1초에 한 번만
    .Subscribe(prices =>
        Console.WriteLine($"Significant change: {prices.Old} -> {prices.New}"));
```

#### 2.2 LINQ(Language Integrated Query) 기초

**LINQ 쿼리 문법**

[LINQ](https://learn.microsoft.com/en-us/dotnet/csharp/linq/)는 .NET에서 데이터를 쿼리하기 위한 통합 모델입니다. Rx는 LINQ를 시간 차원으로 확장한 것입니다.

```csharp
// 컬렉션에 대한 LINQ
var numbers = new[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

// 쿼리 구문
var evenSquares = from n in numbers
                  where n % 2 == 0
                  select n * n;

// 메서드 구문 (동일한 결과)
var evenSquares2 = numbers
    .Where(n => n % 2 == 0)
    .Select(n => n * n);

// 결과: [4, 16, 36, 64, 100]
```

**LINQ to Observable:**

```csharp
// Observable에 대한 LINQ (Rx)
IObservable<int> numbers = Observable.Range(1, 10);

// 동일한 LINQ 연산자를 사용
IObservable<int> evenSquares = numbers
    .Where(n => n % 2 == 0)
    .Select(n => n * n);

// 구독하여 결과 받기
evenSquares.Subscribe(x => Console.WriteLine(x));
// 출력: 4, 16, 36, 64, 100
```

**메서드 체인과 함수형 프로그래밍**

Rx는 [함수형 프로그래밍](https://learn.microsoft.com/en-us/dotnet/standard/linq/)의 핵심 개념을 활용합니다:

```csharp
// 메서드 체이닝을 통한 데이터 파이프라인
var pipeline = Observable.Interval(TimeSpan.FromSeconds(1))  // 1초마다 숫자 방출
    .Select(x => x * 2)                                       // 2배로
    .Where(x => x % 4 == 0)                                   // 4의 배수만
    .Take(5)                                                  // 처음 5개만
    .Select(x => $"Value: {x}");                              // 문자열로 변환

// 각 단계가 순수 함수로 구성됨 (부작용 없음)
pipeline.Subscribe(Console.WriteLine);
// 출력: Value: 0, Value: 4, Value: 8, Value: 12, Value: 16
```

**고차 함수 (Higher-Order Functions):**

```csharp
// SelectMany는 고차 함수의 예 (함수를 인자로 받음)
IObservable<string> flattenedResults = userIds
    .SelectMany(userId => GetUserDetailsAsync(userId))  // 각 userId를 Observable로 변환
    .SelectMany(user => GetUserPostsAsync(user.Id))     // 각 user를 다시 Observable로 변환
    .Select(post => post.Title);

// 이는 중첩된 비동기 호출을 평탄화(flatten)함
```

#### 2.3 디자인 패턴 기초

**Observer 패턴**

[Observer 패턴](https://learn.microsoft.com/en-us/dotnet/standard/events/observer-design-pattern)은 한 객체의 상태 변화를 다른 객체들에게 자동으로 알리는 패턴입니다.

```csharp
// .NET의 표준 Observer 패턴 인터페이스
public interface IObserver<T>
{
    void OnNext(T value);        // 새 값 수신
    void OnError(Exception error); // 에러 수신
    void OnCompleted();           // 완료 알림
}

public interface IObservable<T>
{
    IDisposable Subscribe(IObserver<T> observer);
}

// Observer 구현 예제
public class ConsoleObserver<T> : IObserver<T>
{
    public void OnNext(T value)
    {
        Console.WriteLine($"Received: {value}");
    }

    public void OnError(Exception error)
    {
        Console.WriteLine($"Error: {error.Message}");
    }

    public void OnCompleted()
    {
        Console.WriteLine("Sequence completed");
    }
}

// 사용
IObservable<int> source = Observable.Range(1, 5);
IObserver<int> observer = new ConsoleObserver<int>();
IDisposable subscription = source.Subscribe(observer);

// 출력:
// Received: 1
// Received: 2
// Received: 3
// Received: 4
// Received: 5
// Sequence completed
```

**Observer 패턴의 계약 (Grammar):**

Rx는 엄격한 규칙을 따릅니다:
```
OnNext* (OnError | OnCompleted)?
```

- `OnNext`는 0번 이상 호출될 수 있음
- `OnError` 또는 `OnCompleted` 중 하나만 호출됨 (선택적)
- `OnError` 또는 `OnCompleted` 후에는 더 이상 호출 없음

**Iterator 패턴**

[Iterator 패턴](https://learn.microsoft.com/en-us/dotnet/api/system.collections.ienumerator)은 컬렉션의 요소를 순차적으로 접근하는 패턴입니다.

```csharp
// IEnumerable과 IObservable의 대칭성 (Duality)
IEnumerable<int> enumerable = Enumerable.Range(1, 5);
IObservable<int> observable = Observable.Range(1, 5);

// Pull (Iterator): 소비자가 제어
foreach (int item in enumerable)  // MoveNext() 호출
{
    Console.WriteLine(item);  // Current 접근
}

// Push (Observer): 생산자가 제어
observable.Subscribe(item =>      // OnNext() 자동 호출
    Console.WriteLine(item));
```

**Duality (쌍대성):**

| IEnumerable<T> (Pull) | IObservable<T> (Push) |
|----------------------|----------------------|
| `T Current { get; }` | `void OnNext(T value)` |
| `bool MoveNext()` | (자동 푸시) |
| (예외 발생) | `void OnError(Exception e)` |
| `MoveNext() returns false` | `void OnCompleted()` |

**Pub-Sub 패턴 (Publisher-Subscriber)**

Pub-Sub 패턴은 Observer 패턴의 확장으로, 발행자와 구독자 사이에 중개자가 있습니다.

```csharp
// Subject는 Observable이면서 Observer (Pub-Sub 중개자)
var subject = new Subject<string>();

// 구독자 1
subject.Subscribe(msg => Console.WriteLine($"Subscriber 1: {msg}"));

// 구독자 2
subject.Subscribe(msg => Console.WriteLine($"Subscriber 2: {msg}"));

// 발행
subject.OnNext("Hello");
subject.OnNext("World");
subject.OnCompleted();

// 출력:
// Subscriber 1: Hello
// Subscriber 2: Hello
// Subscriber 1: World
// Subscriber 2: World
```

**Event Bus 패턴:**

```csharp
// 애플리케이션 전역 이벤트 버스
public class EventBus
{
    private readonly Subject<object> _subject = new Subject<object>();

    public void Publish<T>(T message)
    {
        _subject.OnNext(message);
    }

    public IObservable<T> Subscribe<T>()
    {
        return _subject.OfType<T>();
    }
}

// 사용
var eventBus = new EventBus();

eventBus.Subscribe<string>()
    .Subscribe(msg => Console.WriteLine($"String: {msg}"));

eventBus.Subscribe<int>()
    .Subscribe(num => Console.WriteLine($"Number: {num}"));

eventBus.Publish("Hello");  // String: Hello
eventBus.Publish(42);       // Number: 42
eventBus.Publish("World");  // String: World
```

### Chapter 3: Rx의 핵심 타입과 인터페이스

#### 3.1 IObservable<T>와 IObserver<T>

**Observable과 Observer의 계약**

Rx의 핵심은 두 개의 간단한 인터페이스입니다:

```csharp
// .NET Framework에 내장된 표준 인터페이스
public interface IObservable<out T>
{
    IDisposable Subscribe(IObserver<T> observer);
}

public interface IObserver<in T>
{
    void OnNext(T value);
    void OnError(Exception error);
    void OnCompleted();
}
```

이 두 인터페이스는 .NET Framework 4.0부터 [System 네임스페이스](https://learn.microsoft.com/en-us/dotnet/api/system.iobservable-1)에 포함되어 있습니다.

**계약의 의미:**

```csharp
// Observable: 데이터 소스
IObservable<int> source = Observable.Range(1, 5);

// Observer: 세 가지 콜백 제공
source.Subscribe(
    onNext: value => Console.WriteLine($"Value: {value}"),
    onError: error => Console.WriteLine($"Error: {error.Message}"),
    onCompleted: () => Console.WriteLine("Completed")
);

// 출력:
// Value: 1
// Value: 2
// Value: 3
// Value: 4
// Value: 5
// Completed
```

**OnNext, OnError, OnCompleted 규칙**

Rx Observable은 엄격한 문법(Grammar)을 따릅니다:

```
OnNext* (OnError | OnCompleted)?
```

**규칙 설명:**
1. `OnNext`는 0회 이상 호출될 수 있음
2. 완료는 `OnError` (에러 발생) 또는 `OnCompleted` (정상 완료) 중 하나
3. `OnError` 또는 `OnCompleted` 호출 후에는 더 이상 아무것도 호출되지 않음
4. `OnError`와 `OnCompleted`는 상호 배타적 (둘 다 호출되지 않음)

```csharp
// 정상 완료 예제
var completed = Observable.Create<int>(observer =>
{
    observer.OnNext(1);
    observer.OnNext(2);
    observer.OnNext(3);
    observer.OnCompleted();  // 완료
    // observer.OnNext(4);   // 이건 호출되지 않음!
    return Disposable.Empty;
});

// 에러 예제
var error = Observable.Create<int>(observer =>
{
    observer.OnNext(1);
    observer.OnError(new Exception("Something went wrong"));
    // observer.OnNext(2);   // 이것도 호출되지 않음!
    // observer.OnCompleted(); // 이것도 호출되지 않음!
    return Disposable.Empty;
});

// 무한 시퀀스 (완료 없음)
var infinite = Observable.Interval(TimeSpan.FromSeconds(1));
// OnNext만 계속 호출되고 OnCompleted는 호출되지 않음
```

**IDisposable과 구독 해제:**

[IDisposable](https://learn.microsoft.com/en-us/dotnet/api/system.idisposable)은 리소스 정리를 위한 .NET의 표준 패턴입니다.

```csharp
// Subscribe는 IDisposable을 반환
IDisposable subscription = observable.Subscribe(x => Console.WriteLine(x));

// 구독 해제 (더 이상 값을 받지 않음)
subscription.Dispose();

// using 패턴 사용
using (observable.Subscribe(x => Console.WriteLine(x)))
{
    // 스코프를 벗어나면 자동으로 Dispose 호출
}

// 여러 구독을 한 번에 관리
var disposables = new CompositeDisposable();
disposables.Add(observable1.Subscribe(x => Console.WriteLine($"1: {x}")));
disposables.Add(observable2.Subscribe(x => Console.WriteLine($"2: {x}")));
// 모든 구독을 한 번에 해제
disposables.Dispose();
```

#### 3.2 ISubject<T> 인터페이스

**Subject의 이중성: Observer이자 Observable**

[Subject<T>](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.subjects.subject-1)는 Observable이면서 동시에 Observer입니다. 마치 이벤트 허브처럼 동작합니다.

```csharp
public interface ISubject<in TSource, out TResult> :
    IObserver<TSource>,    // 데이터를 받을 수 있음
    IObservable<TResult>   // 데이터를 방출할 수 있음
{
}

public interface ISubject<T> : ISubject<T, T>, IObserver<T>, IObservable<T>
{
}
```

**Subject 기본 사용:**

```csharp
var subject = new Subject<int>();

// Observer로 사용: 데이터 푸시
subject.Subscribe(x => Console.WriteLine($"Subscriber 1: {x}"));
subject.Subscribe(x => Console.WriteLine($"Subscriber 2: {x}"));

// Observable로 사용: 데이터 방출
subject.OnNext(1);  // 모든 구독자에게 전달
subject.OnNext(2);
subject.OnCompleted();

// 출력:
// Subscriber 1: 1
// Subscriber 2: 1
// Subscriber 1: 2
// Subscriber 2: 2
```

**Subject 타입들**

**1. Subject<T> - 기본 Subject**

```csharp
var subject = new Subject<int>();

subject.Subscribe(x => Console.WriteLine($"Early: {x}"));
subject.OnNext(1);  // Early: 1

subject.Subscribe(x => Console.WriteLine($"Late: {x}"));
subject.OnNext(2);  // Early: 2, Late: 2

// 늦게 구독한 observer는 이전 값을 받지 못함
```

**2. [BehaviorSubject<T>](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.subjects.behaviorsubject-1) - 현재 값 유지**

```csharp
// 초기값이 필요
var subject = new BehaviorSubject<int>(0);

subject.Subscribe(x => Console.WriteLine($"Early: {x}"));
// 출력: Early: 0 (초기값을 즉시 받음)

subject.OnNext(1);  // Early: 1
subject.OnNext(2);  // Early: 2

subject.Subscribe(x => Console.WriteLine($"Late: {x}"));
// 출력: Late: 2 (가장 최근 값을 즉시 받음)

subject.OnNext(3);  // Early: 3, Late: 3

// 현재 값 접근 가능
Console.WriteLine($"Current value: {subject.Value}");  // 3
```

**사용 사례:** UI 상태, 설정 값, 현재 사용자 정보

**3. [ReplaySubject<T>](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.subjects.replaysubject-1) - 이전 값들 재생**

```csharp
// 모든 값을 기억
var subject = new ReplaySubject<int>();

subject.OnNext(1);
subject.OnNext(2);
subject.OnNext(3);

// 늦게 구독해도 모든 이전 값을 받음
subject.Subscribe(x => Console.WriteLine($"Late: {x}"));
// 출력:
// Late: 1
// Late: 2
// Late: 3

subject.OnNext(4);  // Late: 4

// 버퍼 크기 제한 가능
var limitedSubject = new ReplaySubject<int>(bufferSize: 2);
limitedSubject.OnNext(1);
limitedSubject.OnNext(2);
limitedSubject.OnNext(3);

limitedSubject.Subscribe(x => Console.WriteLine(x));
// 출력: 2, 3 (마지막 2개만)

// 시간 기반 버퍼
var timeSubject = new ReplaySubject<int>(window: TimeSpan.FromSeconds(5));
// 최근 5초 동안의 값만 재생
```

**사용 사례:** 캐싱, 이벤트 재생, 히스토리 추적

**4. [AsyncSubject<T>](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.subjects.asyncsubject-1) - 마지막 값만**

```csharp
var subject = new AsyncSubject<int>();

subject.Subscribe(x => Console.WriteLine($"Subscriber: {x}"));

subject.OnNext(1);  // 아무 출력 없음
subject.OnNext(2);  // 아무 출력 없음
subject.OnNext(3);  // 아무 출력 없음
subject.OnCompleted();  // 출력: Subscriber: 3

// OnCompleted 호출 시 마지막 값만 전달됨
```

**사용 사례:** 비동기 작업의 최종 결과 (Task<T>와 유사)

**Subject 비교 표:**

| Subject 타입 | 초기값 | 버퍼 | 완료 전 구독 | 완료 후 구독 |
|-------------|--------|------|-------------|-------------|
| Subject | 없음 | 없음 | 이후 값만 | 완료만 받음 |
| BehaviorSubject | 필수 | 1개 (현재값) | 현재값 + 이후 값 | 마지막 값 + 완료 |
| ReplaySubject | 없음 | 전체/제한 | 모든 이전값 + 이후 값 | 모든 값 + 완료 |
| AsyncSubject | 없음 | 1개 (마지막값) | 아무것도 안받음 | 마지막 값 + 완료 |

#### 3.3 IScheduler 인터페이스

**동시성과 시간 관리**

[IScheduler](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.concurrency.ischeduler)는 Rx에서 "언제" 그리고 "어디서" 작업이 실행될지를 제어합니다.

```csharp
public interface IScheduler
{
    DateTimeOffset Now { get; }

    IDisposable Schedule<TState>(
        TState state,
        Func<IScheduler, TState, IDisposable> action);

    IDisposable Schedule<TState>(
        TState state,
        TimeSpan dueTime,
        Func<IScheduler, TState, IDisposable> action);

    IDisposable Schedule<TState>(
        TState state,
        DateTimeOffset dueTime,
        Func<IScheduler, TState, IDisposable> action);
}
```

**스케줄러의 역할과 중요성**

스케줄러는 세 가지 핵심 기능을 제공합니다:

1. **실행 컨텍스트 제어** - 어떤 스레드에서 실행할지
2. **시간 가상화** - 테스트를 위한 시간 제어
3. **동시성 관리** - 스레드 안전성 보장

```csharp
// 스케줄러 없이 (기본 동작)
Observable.Range(1, 5)
    .Subscribe(x => Console.WriteLine(
        $"Thread: {Thread.CurrentThread.ManagedThreadId}, Value: {x}"));

// 특정 스케줄러 사용
Observable.Range(1, 5)
    .ObserveOn(NewThreadScheduler.Default)  // 새 스레드에서 관찰
    .Subscribe(x => Console.WriteLine(
        $"Thread: {Thread.CurrentThread.ManagedThreadId}, Value: {x}"));
```

**주요 스케줄러 타입:**

```csharp
// 1. ImmediateScheduler - 즉시 실행 (동기적)
Scheduler.Immediate.Schedule(() => Console.WriteLine("Immediate"));

// 2. CurrentThreadScheduler - 현재 스레드에서 실행 (큐 사용)
Scheduler.CurrentThread.Schedule(() => Console.WriteLine("Current"));

// 3. NewThreadScheduler - 새 스레드 생성
Scheduler.NewThread.Schedule(() => Console.WriteLine("New Thread"));

// 4. ThreadPoolScheduler - .NET ThreadPool 사용
Scheduler.ThreadPool.Schedule(() => Console.WriteLine("ThreadPool"));

// 5. TaskPoolScheduler - Task 기반
TaskPoolScheduler.Default.Schedule(() => Console.WriteLine("Task"));

// 6. SynchronizationContextScheduler - UI 스레드 (WPF, WinForms)
// var uiScheduler = new SynchronizationContextScheduler(
//     SynchronizationContext.Current);
```

**SubscribeOn vs ObserveOn:**

```csharp
var observable = Observable.Create<int>(observer =>
{
    Console.WriteLine($"Creating on thread: {Thread.CurrentThread.ManagedThreadId}");
    observer.OnNext(1);
    observer.OnNext(2);
    observer.OnCompleted();
    return Disposable.Empty;
});

observable
    .SubscribeOn(NewThreadScheduler.Default)  // 구독 작업을 실행할 스레드
    .Select(x =>
    {
        Console.WriteLine($"Select on thread: {Thread.CurrentThread.ManagedThreadId}");
        return x * 2;
    })
    .ObserveOn(ThreadPoolScheduler.Instance)  // 이후 작업을 실행할 스레드
    .Subscribe(x =>
        Console.WriteLine($"Subscribe on thread: {Thread.CurrentThread.ManagedThreadId}, Value: {x}"));
```

**실용 예제: UI 업데이트**

```csharp
// WPF/WinForms에서 백그라운드 작업 후 UI 업데이트
Observable
    .Start(() =>  // ThreadPool에서 무거운 작업 실행
    {
        Thread.Sleep(2000);  // 2초 걸리는 작업 시뮬레이션
        return CalculateHeavyResult();
    }, TaskPoolScheduler.Default)
    .ObserveOn(SynchronizationContext.Current)  // UI 스레드로 전환
    .Subscribe(result =>
    {
        // UI 업데이트 (메인 스레드에서 안전하게 실행)
        resultTextBox.Text = result.ToString();
    });
```

**TestScheduler - 테스트를 위한 가상 시간:**

```csharp
var scheduler = new TestScheduler();

var source = Observable.Interval(TimeSpan.FromSeconds(1), scheduler)
    .Take(5);

var results = scheduler.Start(
    () => source,
    created: 0,
    subscribed: 0,
    disposed: TimeSpan.FromSeconds(10).Ticks);

// 실제 시간이 흐르지 않고 가상 시간으로 테스트
foreach (var result in results.Messages)
{
    Console.WriteLine($"Time: {result.Time}, Value: {result.Value}");
}
```

---

## 📗 Part 2: Observable 시퀀스 생성과 구독

### Chapter 4: Observable 생성 패턴

#### 4.1 Factory 메서드를 통한 생성

Rx는 다양한 팩토리 메서드를 제공하여 Observable을 쉽게 생성할 수 있습니다.

**기본 팩토리 메서드:**

```csharp
// Observable.Return - 단일 값을 방출하고 완료
IObservable<int> single = Observable.Return(42);
single.Subscribe(
    x => Console.WriteLine($"Value: {x}"),
    () => Console.WriteLine("Completed"));
// 출력: Value: 42
//       Completed

// Observable.Empty - 즉시 완료 (값 없음)
IObservable<int> empty = Observable.Empty<int>();
empty.Subscribe(
    x => Console.WriteLine($"Value: {x}"),
    () => Console.WriteLine("Empty completed"));
// 출력: Empty completed

// Observable.Never - 아무것도 방출하지 않고 완료되지도 않음
IObservable<int> never = Observable.Never<int>();
never.Subscribe(
    x => Console.WriteLine($"Value: {x}"),
    () => Console.WriteLine("This will never print"));
// 출력 없음 (무한 대기)

// Observable.Throw - 즉시 에러 방출
IObservable<int> error = Observable.Throw<int>(new Exception("Error!"));
error.Subscribe(
    x => Console.WriteLine($"Value: {x}"),
    ex => Console.WriteLine($"Error: {ex.Message}"),
    () => Console.WriteLine("Completed"));
// 출력: Error: Error!
```

**[Observable.Range](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.range) - 연속된 정수 시퀀스:**

```csharp
// 1부터 10까지의 숫자 생성
IObservable<int> range = Observable.Range(1, 10);
range.Subscribe(x => Console.Write($"{x} "));
// 출력: 1 2 3 4 5 6 7 8 9 10

// 실용 예제: 병렬 처리
Observable.Range(1, 100)
    .Select(i => CalculateExpensiveOperation(i))
    .Subscribe(result => Console.WriteLine(result));
```

**[Observable.Repeat](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.repeat) - 값 반복:**

```csharp
// "Hello"를 3번 반복
Observable.Repeat("Hello", 3)
    .Subscribe(x => Console.WriteLine(x));
// 출력:
// Hello
// Hello
// Hello
```

#### 4.2 시간 기반 Observable 생성

**[Observable.Timer](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.timer) - 지연 후 값 방출:**

```csharp
// 3초 후 한 번만 방출
var timer = Observable.Timer(TimeSpan.FromSeconds(3));
Console.WriteLine($"Started at {DateTime.Now:HH:mm:ss}");
timer.Subscribe(x => Console.WriteLine($"Fired at {DateTime.Now:HH:mm:ss}, Value: {x}"));
// 출력:
// Started at 10:00:00
// Fired at 10:00:03, Value: 0

// 3초 후 시작하여 1초마다 반복
var repeatingTimer = Observable.Timer(
    dueTime: TimeSpan.FromSeconds(3),
    period: TimeSpan.FromSeconds(1));
repeatingTimer
    .Take(5)
    .Subscribe(x => Console.WriteLine($"{DateTime.Now:HH:mm:ss} - {x}"));
```

**[Observable.Interval](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.interval) - 주기적 값 방출:**

```csharp
// 1초마다 값 방출 (0부터 시작)
var interval = Observable.Interval(TimeSpan.FromSeconds(1));
interval
    .Take(5)
    .Subscribe(x => Console.WriteLine($"Tick: {x}"));
// 출력 (1초마다):
// Tick: 0
// Tick: 1
// Tick: 2
// Tick: 3
// Tick: 4

// 실용 예제: 실시간 대시보드 업데이트
Observable.Interval(TimeSpan.FromSeconds(5))
    .SelectMany(_ => FetchDashboardDataAsync())
    .Subscribe(data => UpdateDashboard(data));
```

**[Observable.Generate](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.generate) - 커스텀 시퀀스:**

```csharp
// 피보나치 수열 생성
var fibonacci = Observable.Generate(
    initialState: (0, 1),                          // 시작 상태
    condition: state => state.Item1 < 100,         // 계속 조건
    iterate: state => (state.Item2, state.Item1 + state.Item2),  // 다음 상태
    resultSelector: state => state.Item1);          // 결과 선택

fibonacci.Subscribe(x => Console.Write($"{x} "));
// 출력: 0 1 1 2 3 5 8 13 21 34 55 89

// 시간 기반 Generate
var timeSequence = Observable.Generate(
    initialState: 0,
    condition: x => x < 5,
    iterate: x => x + 1,
    resultSelector: x => x,
    timeSelector: x => TimeSpan.FromSeconds(x));  // 점점 길어지는 간격
```

#### 4.3 이벤트를 Observable로 변환

**[Observable.FromEventPattern](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.fromeventpattern) - .NET 이벤트 연동:**

```csharp
// Button Click 이벤트를 Observable로 변환
public class MyForm
{
    private Button _button = new Button();

    public void SetupReactiveEvents()
    {
        // 표준 .NET 이벤트를 Observable로 변환
        var clicks = Observable.FromEventPattern<EventHandler, EventArgs>(
            handler => _button.Click += handler,
            handler => _button.Click -= handler);

        clicks
            .Throttle(TimeSpan.FromSeconds(1))  // 디바운싱
            .Subscribe(evt => Console.WriteLine("Button clicked!"));

        // 간단한 구문 (EventHandler<T> 사용 시)
        var simplifiedClicks = Observable.FromEventPattern(
            h => _button.Click += h,
            h => _button.Click -= h);
    }
}
```

**FileSystemWatcher 예제:**

```csharp
// 파일 시스템 변경 감지
var watcher = new FileSystemWatcher(@"C:\temp")
{
    EnableRaisingEvents = true,
    IncludeSubdirectories = true
};

// 파일 생성 이벤트를 Observable로
var created = Observable.FromEventPattern<FileSystemEventHandler, FileSystemEventArgs>(
    handler => watcher.Created += handler,
    handler => watcher.Created -= handler)
    .Select(evt => evt.EventArgs);

// 파일 변경 이벤트를 Observable로
var changed = Observable.FromEventPattern<FileSystemEventHandler, FileSystemEventArgs>(
    handler => watcher.Changed += handler,
    handler => watcher.Changed -= handler)
    .Select(evt => evt.EventArgs);

// 모든 파일 시스템 이벤트 통합
var allEvents = Observable.Merge(created, changed);

allEvents
    .Throttle(TimeSpan.FromMilliseconds(500))  // 빠른 연속 이벤트 필터링
    .Subscribe(e => Console.WriteLine($"{e.ChangeType}: {e.FullPath}"));
```

**마우스 이벤트 예제:**

```csharp
// WPF/WinForms에서 마우스 이벤트 처리
var mouseMove = Observable.FromEventPattern<MouseEventArgs>(
    h => canvas.MouseMove += h,
    h => canvas.MouseMove -= h);

var mouseDown = Observable.FromEventPattern<MouseEventArgs>(
    h => canvas.MouseDown += h,
    h => canvas.MouseDown -= h);

var mouseUp = Observable.FromEventPattern<MouseEventArgs>(
    h => canvas.MouseUp += h,
    h => canvas.MouseUp -= h);

// 드래그 제스처 구현
var drags = from start in mouseDown
            from move in mouseMove.TakeUntil(mouseUp)
            select new
            {
                StartX = start.EventArgs.X,
                StartY = start.EventArgs.Y,
                CurrentX = move.EventArgs.X,
                CurrentY = move.EventArgs.Y
            };

drags.Subscribe(drag =>
    Console.WriteLine($"Dragging from ({drag.StartX},{drag.StartY}) to ({drag.CurrentX},{drag.CurrentY})"));
```

#### 4.4 Observable.Create를 통한 커스텀 구현

**[Observable.Create](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.create) - 완전한 제어:**

```csharp
// 기본 구조
var custom = Observable.Create<int>(observer =>
{
    // 값 방출
    observer.OnNext(1);
    observer.OnNext(2);
    observer.OnNext(3);
    observer.OnCompleted();

    // 정리 작업을 위한 IDisposable 반환
    return Disposable.Create(() =>
    {
        Console.WriteLine("Subscription disposed");
    });
});
```

**리소스 관리와 Disposal:**

```csharp
// WebSocket을 Observable로 래핑
public IObservable<string> CreateWebSocketObservable(string url)
{
    return Observable.Create<string>(async observer =>
    {
        var client = new ClientWebSocket();

        try
        {
            // 연결
            await client.ConnectAsync(new Uri(url), CancellationToken.None);
            Console.WriteLine("WebSocket connected");

            var buffer = new byte[1024];

            // 메시지 수신 루프
            while (client.State == WebSocketState.Open)
            {
                var result = await client.ReceiveAsync(
                    new ArraySegment<byte>(buffer),
                    CancellationToken.None);

                if (result.MessageType == WebSocketMessageType.Text)
                {
                    var message = Encoding.UTF8.GetString(buffer, 0, result.Count);
                    observer.OnNext(message);
                }
                else if (result.MessageType == WebSocketMessageType.Close)
                {
                    observer.OnCompleted();
                    break;
                }
            }
        }
        catch (Exception ex)
        {
            observer.OnError(ex);
        }

        // 정리: 구독 해제 시 WebSocket 닫기
        return Disposable.Create(() =>
        {
            if (client.State == WebSocketState.Open)
            {
                client.CloseAsync(
                    WebSocketCloseStatus.NormalClosure,
                    "Disposed",
                    CancellationToken.None).Wait();
            }
            client.Dispose();
            Console.WriteLine("WebSocket disposed");
        });
    });
}

// 사용
var ws = CreateWebSocketObservable("ws://example.com/socket");
var subscription = ws.Subscribe(
    msg => Console.WriteLine($"Received: {msg}"),
    ex => Console.WriteLine($"Error: {ex.Message}"),
    () => Console.WriteLine("Connection closed"));

// 구독 해제 시 자동으로 WebSocket 정리
subscription.Dispose();
```

**동시성 규칙 준수:**

Rx Observable은 다음 규칙을 따라야 합니다:
1. **직렬화 (Serialization)**: OnNext는 동시에 호출되어서는 안 됨
2. **순서 보장**: 메시지는 순서대로 전달되어야 함

```csharp
// 잘못된 예: 동시성 규칙 위반
var bad = Observable.Create<int>(observer =>
{
    // 여러 스레드에서 동시에 OnNext 호출 (위험!)
    Task.Run(() => observer.OnNext(1));
    Task.Run(() => observer.OnNext(2));
    Task.Run(() => observer.OnNext(3));

    return Disposable.Empty;
});

// 올바른 예: 직렬화 보장
var good = Observable.Create<int>(observer =>
{
    var scheduler = new EventLoopScheduler();

    scheduler.Schedule(() => observer.OnNext(1));
    scheduler.Schedule(() => observer.OnNext(2));
    scheduler.Schedule(() => observer.OnNext(3));
    scheduler.Schedule(() => observer.OnCompleted());

    return scheduler;  // IDisposable을 반환하여 자동 정리
});

// 또는 Synchronize 사용
var synchronized = Observable.Create<int>(observer =>
{
    var syncObserver = Observer.Synchronize(observer);

    Task.Run(() => syncObserver.OnNext(1));
    Task.Run(() => syncObserver.OnNext(2));
    Task.Run(() => syncObserver.OnNext(3));

    return Disposable.Empty;
});
```

### Chapter 5: 구독과 생명주기 관리

#### 5.1 Subscribe 메서드와 IDisposable

**Subscribe 오버로드:**

```csharp
var source = Observable.Range(1, 5);

// 1. OnNext만
source.Subscribe(x => Console.WriteLine(x));

// 2. OnNext와 OnError
source.Subscribe(
    x => Console.WriteLine(x),
    ex => Console.WriteLine($"Error: {ex.Message}"));

// 3. OnNext, OnError, OnCompleted
source.Subscribe(
    x => Console.WriteLine(x),
    ex => Console.WriteLine($"Error: {ex.Message}"),
    () => Console.WriteLine("Completed"));

// 4. IObserver<T> 구현 전달
source.Subscribe(new MyObserver());

// 5. 구독만 하고 아무것도 하지 않음 (부작용만 실행)
source.Subscribe();
```

**구독 해제의 중요성:**

```csharp
// 메모리 누수 예제
public class LeakyViewModel
{
    private IObservable<long> _timer = Observable.Interval(TimeSpan.FromSeconds(1));

    public LeakyViewModel()
    {
        // 위험: Dispose하지 않음!
        _timer.Subscribe(x => UpdateUI(x));
    }
    // ViewModel이 소멸되어도 타이머는 계속 실행됨
}

// 올바른 예제
public class ProperViewModel : IDisposable
{
    private IDisposable _subscription;
    private IObservable<long> _timer = Observable.Interval(TimeSpan.FromSeconds(1));

    public ProperViewModel()
    {
        _subscription = _timer.Subscribe(x => UpdateUI(x));
    }

    public void Dispose()
    {
        _subscription?.Dispose();  // 리소스 정리
    }
}
```

**using 패턴과 [CompositeDisposable](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.disposables.compositedisposable):**

```csharp
// using 패턴
using (var subscription = observable.Subscribe(x => Console.WriteLine(x)))
{
    // 구독 활성
} // 여기서 자동으로 Dispose 호출

// CompositeDisposable: 여러 구독을 한 번에 관리
public class DashboardViewModel : IDisposable
{
    private readonly CompositeDisposable _disposables = new CompositeDisposable();

    public DashboardViewModel()
    {
        // 여러 Observable 구독
        _disposables.Add(
            _stockPrices.Subscribe(UpdatePrices));

        _disposables.Add(
            _news.Subscribe(UpdateNews));

        _disposables.Add(
            _alerts.Subscribe(ShowAlert));
    }

    public void Dispose()
    {
        // 모든 구독을 한 번에 해제
        _disposables.Dispose();
    }
}

// SerialDisposable: 이전 구독을 자동으로 해제
var serial = new SerialDisposable();
serial.Disposable = observable1.Subscribe(x => Console.WriteLine($"1: {x}"));
// 새 구독으로 교체 (이전 구독 자동 해제)
serial.Disposable = observable2.Subscribe(x => Console.WriteLine($"2: {x}"));
```

#### 5.2 Hot vs Cold Observable

**Cold Observable - 구독 시 시작:**

```csharp
// Cold: 각 구독자가 독립적인 데이터 스트림을 받음
var cold = Observable.Interval(TimeSpan.FromSeconds(1)).Take(5);

Console.WriteLine("Subscriber 1:");
cold.Subscribe(x => Console.WriteLine($"  1: {x}"));

Thread.Sleep(3000);  // 3초 대기

Console.WriteLine("Subscriber 2:");
cold.Subscribe(x => Console.WriteLine($"  2: {x}"));

// 출력:
// Subscriber 1:
//   1: 0
//   1: 1
//   1: 2
// Subscriber 2:
//   2: 0  <- 처음부터 다시 시작!
//   1: 3
//   2: 1
//   1: 4
//   2: 2
//   2: 3
//   2: 4
```

**Hot Observable - 이미 실행 중:**

```csharp
// Hot: 모든 구독자가 같은 스트림을 공유
var cold = Observable.Interval(TimeSpan.FromSeconds(1)).Take(5);
var hot = cold.Publish();  // Cold를 Hot으로 변환
hot.Connect();  // 시작

Console.WriteLine("Subscriber 1:");
hot.Subscribe(x => Console.WriteLine($"  1: {x}"));

Thread.Sleep(3000);  // 3초 대기

Console.WriteLine("Subscriber 2:");
hot.Subscribe(x => Console.WriteLine($"  2: {x}"));

// 출력:
// Subscriber 1:
//   1: 0
//   1: 1
//   1: 2
// Subscriber 2:
//   1: 3
//   2: 3  <- 현재 위치부터 받음!
//   1: 4
//   2: 4
```

**[Publish](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.publish)와 Connect:**

```csharp
// Publish: IConnectableObservable로 변환
var source = Observable.Interval(TimeSpan.FromSeconds(1)).Take(5);
var published = source.Publish();

// 여러 구독자 추가 (아직 시작 안 됨)
published.Subscribe(x => Console.WriteLine($"A: {x}"));
published.Subscribe(x => Console.WriteLine($"B: {x}"));

// Connect 호출 시 시작
var connection = published.Connect();

// 구독 해제 시 모든 구독자에게 영향
connection.Dispose();
```

**[RefCount](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.refcount) - 자동 연결/해제:**

```csharp
// RefCount: 첫 구독자가 구독하면 Connect, 마지막 구독자가 해제하면 Disconnect
var source = Observable.Interval(TimeSpan.FromSeconds(1))
    .Do(x => Console.WriteLine($"Producing {x}"))
    .Publish()
    .RefCount();  // 자동 연결 관리

// 첫 구독: Connect 호출됨
var sub1 = source.Subscribe(x => Console.WriteLine($"Sub1: {x}"));

Thread.Sleep(2000);

// 두 번째 구독: 이미 실행 중인 스트림 공유
var sub2 = source.Subscribe(x => Console.WriteLine($"Sub2: {x}"));

Thread.Sleep(2000);

// 첫 번째 구독 해제: 아직 sub2가 있으므로 계속 실행
sub1.Dispose();

Thread.Sleep(2000);

// 마지막 구독 해제: 자동으로 Disconnect
sub2.Dispose();
```

**Share - Publish().RefCount() 단축:**

```csharp
// Share는 Publish().RefCount()와 동일
var shared = Observable.Interval(TimeSpan.FromSeconds(1))
    .Do(x => Console.WriteLine($"Producing {x}"))
    .Share();  // Hot + RefCount

var sub1 = shared.Subscribe(x => Console.WriteLine($"Sub1: {x}"));
var sub2 = shared.Subscribe(x => Console.WriteLine($"Sub2: {x}"));
```

#### 5.3 Subject 활용 패턴

**메시지 큐 브리징:**

```csharp
// RabbitMQ를 Observable로 래핑
public class MessageQueueObservable
{
    private readonly Subject<string> _messages = new Subject<string>();
    private IConnection _connection;
    private IModel _channel;

    public IObservable<string> Messages => _messages.AsObservable();

    public void Connect(string queueName)
    {
        var factory = new ConnectionFactory() { HostName = "localhost" };
        _connection = factory.CreateConnection();
        _channel = _connection.CreateModel();

        var consumer = new EventingBasicConsumer(_channel);
        consumer.Received += (model, ea) =>
        {
            var body = ea.Body.ToArray();
            var message = Encoding.UTF8.GetString(body);
            _messages.OnNext(message);  // Subject로 푸시
        };

        _channel.BasicConsume(queue: queueName, autoAck: true, consumer: consumer);
    }

    public void Dispose()
    {
        _messages.OnCompleted();
        _channel?.Close();
        _connection?.Close();
    }
}

// 사용
var mq = new MessageQueueObservable();
mq.Connect("myqueue");

mq.Messages
    .Where(msg => msg.Contains("urgent"))
    .Subscribe(msg => Console.WriteLine($"Urgent: {msg}"));
```

**이벤트 집계자(Event Aggregator) 패턴:**

```csharp
// 애플리케이션 전역 이벤트 버스
public interface IEventAggregator
{
    IObservable<T> GetEvent<T>();
    void Publish<T>(T @event);
}

public class EventAggregator : IEventAggregator
{
    private readonly ConcurrentDictionary<Type, object> _subjects =
        new ConcurrentDictionary<Type, object>();

    public IObservable<T> GetEvent<T>()
    {
        var subject = (ISubject<T>)_subjects.GetOrAdd(
            typeof(T),
            _ => new Subject<T>());

        return subject.AsObservable();
    }

    public void Publish<T>(T @event)
    {
        if (_subjects.TryGetValue(typeof(T), out var subject))
        {
            ((ISubject<T>)subject).OnNext(@event);
        }
    }
}

// 이벤트 정의
public class UserLoggedInEvent
{
    public string Username { get; set; }
    public DateTime Timestamp { get; set; }
}

public class OrderPlacedEvent
{
    public int OrderId { get; set; }
    public decimal Amount { get; set; }
}

// 사용
var eventAggregator = new EventAggregator();

// 구독자 1: 로그인 이벤트 처리
eventAggregator.GetEvent<UserLoggedInEvent>()
    .Subscribe(evt => Console.WriteLine($"User {evt.Username} logged in"));

// 구독자 2: 주문 이벤트 처리
eventAggregator.GetEvent<OrderPlacedEvent>()
    .Subscribe(evt => Console.WriteLine($"Order {evt.OrderId}: ${evt.Amount}"));

// 발행
eventAggregator.Publish(new UserLoggedInEvent
{
    Username = "john",
    Timestamp = DateTime.Now
});

eventAggregator.Publish(new OrderPlacedEvent
{
    OrderId = 123,
    Amount = 99.99m
});
```

---

## 📙 Part 3: Rx Operators 완벽 가이드

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

## 📕 Part 4: 고급 개념과 패턴

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

### Chapter 12: 시간 기반 연산자

**Buffer/Window with Time:**

```csharp
// 5초마다 배치 처리
Observable.Interval(TimeSpan.FromMilliseconds(100))
    .Buffer(TimeSpan.FromSeconds(5))
    .Subscribe(list => Console.WriteLine($"Received {list.Count} items"));
```

### Chapter 13: [Backpressure](https://github.com/dotnet/reactive/blob/main/Rx.NET/Documentation/IntroToRx/15_SchedulingAndThreading.md)와 Flow Control

**Backpressure 문제:**

```csharp
// 빠른 생산자, 느린 소비자 시나리오
var fastProducer = Observable.Interval(TimeSpan.FromMilliseconds(1));
fastProducer
    .Sample(TimeSpan.FromMilliseconds(100))  // 샘플링으로 압력 완화
    .Subscribe(x => SlowConsumer(x));

// Buffer로 처리
fastProducer
    .Buffer(100)  // 100개씩 모아서 처리
    .Subscribe(batch => ProcessBatch(batch));
```

---

## 📒 Part 5: 실무 패턴과 최적화

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

### Chapter 15: OOP vs Reactive 패러다임

**[MVVM](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/data-binding-overview) 패턴과 Rx:**

```csharp
public class SearchViewModel : INotifyPropertyChanged
{
    private readonly Subject<string> _searchQuery = new Subject<string>();

    public string SearchText
    {
        set => _searchQuery.OnNext(value);
    }

    public SearchViewModel()
    {
        // 자동 검색with 디바운싱
        _searchQuery
            .Throttle(TimeSpan.FromMilliseconds(300))
            .DistinctUntilChanged()
            .SelectMany(query => SearchAsync(query))
            .ObserveOn(SynchronizationContext.Current)
            .Subscribe(results => SearchResults = results);
    }
}
```

**[ReactiveUI](https://www.reactiveui.net/) 프레임워크:**

```csharp
public class MyViewModel : ReactiveObject
{
    private string _searchQuery;
    public string SearchQuery
    {
        get => _searchQuery;
        set => this.RaiseAndSetIfChanged(ref _searchQuery, value);
    }

    public MyViewModel()
    {
        // ReactiveCommand
        var canSearch = this.WhenAnyValue(x => x.SearchQuery)
            .Select(q => !string.IsNullOrWhiteSpace(q));

        SearchCommand = ReactiveCommand.CreateFromTask(
            async () => await SearchAsync(SearchQuery),
            canSearch);
    }
}
```

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

## 📓 Part 6: 실전 프로젝트

### Chapter 17: 실시간 데이터 처리 시스템

**주식 시세 모니터링 시스템:**

```csharp
public class StockMonitor
{
    public IObservable<StockPrice> MonitorStock(string symbol)
    {
        return Observable.Create<StockPrice>(observer =>
        {
            var client = new WebSocketClient();
            client.Connect($"wss://stocks.example.com/{symbol}");

            client.MessageReceived
                .Select(msg => ParseStockPrice(msg))
                .Subscribe(observer);

            return Disposable.Create(() => client.Dispose());
        });
    }

    // 이동 평균 계산
    public IObservable<decimal> CalculateMovingAverage(
        IObservable<StockPrice> prices, int period)
    {
        return prices
            .Select(p => p.Price)
            .Buffer(period, 1)  // 슬라이딩 윈도우
            .Where(buffer => buffer.Count == period)
            .Select(buffer => buffer.Average());
    }

    // 알림 시스템
    public IObservable<Alert> CreateAlerts(IObservable<StockPrice> prices)
    {
        return prices
            .Buffer(2, 1)
            .Where(buffer => buffer.Count == 2)
            .Select(buffer => new { Previous = buffer[0], Current = buffer[1] })
            .Where(pair =>
                Math.Abs(pair.Current.Price - pair.Previous.Price) > 5)
            .Select(pair => new Alert
            {
                Message = $"Price changed by {pair.Current.Price - pair.Previous.Price}",
                Severity = AlertSeverity.High
            });
    }
}
```

### Chapter 18: UI 이벤트 처리

**자동 완성 구현:**

```csharp
public class AutoCompleteViewModel
{
    public AutoCompleteViewModel()
    {
        var searchText = this.WhenAnyValue(x => x.SearchText);

        Suggestions = searchText
            .Throttle(TimeSpan.FromMilliseconds(300))  // 입력 완료 대기
            .DistinctUntilChanged()                    // 중복 제거
            .Where(text => text?.Length >= 3)          // 최소 3글자
            .SelectMany(text => GetSuggestionsAsync(text))  // API 호출
            .Catch(Observable.Return(Array.Empty<string>()))  // 에러 처리
            .ObserveOn(RxApp.MainThreadScheduler)      // UI 스레드
            .ToProperty(this, x => x.Suggestions);
    }
}
```

**드래그 앤 드롭:**

```csharp
var mouseDown = Observable.FromEventPattern<MouseEventArgs>(
    h => canvas.MouseDown += h,
    h => canvas.MouseDown -= h);

var mouseMove = Observable.FromEventPattern<MouseEventArgs>(
    h => canvas.MouseMove += h,
    h => canvas.MouseMove -= h);

var mouseUp = Observable.FromEventPattern<MouseEventArgs>(
    h => canvas.MouseUp += h,
    h => canvas.MouseUp -= h);

// 드래그 제스처
var drags = from down in mouseDown
            let startPos = down.EventArgs.GetPosition(canvas)
            from move in mouseMove.TakeUntil(mouseUp)
            let currentPos = move.EventArgs.GetPosition(canvas)
            select new { Start = startPos, Current = currentPos };

drags.Subscribe(drag =>
{
    var deltaX = drag.Current.X - drag.Start.X;
    var deltaY = drag.Current.Y - drag.Start.Y;
    UpdateElementPosition(deltaX, deltaY);
});
```

### Chapter 19: 마이크로서비스와 이벤트 소싱

**[CQRS](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) 패턴:**

```csharp
// Command Side
public class OrderCommandHandler
{
    private readonly Subject<OrderEvent> _events = new Subject<OrderEvent>();

    public IObservable<OrderEvent> Events => _events.AsObservable();

    public void PlaceOrder(PlaceOrderCommand command)
    {
        // 비즈니스 로직
        var @event = new OrderPlacedEvent
        {
            OrderId = Guid.NewGuid(),
            CustomerId = command.CustomerId,
            Amount = command.Amount
        };

        _events.OnNext(@event);
    }
}

// Query Side
public class OrderQueryModel
{
    public OrderQueryModel(IObservable<OrderEvent> events)
    {
        events.OfType<OrderPlacedEvent>()
            .Subscribe(evt => UpdateReadModel(evt));
    }
}
```

**[Saga 패턴](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/saga/saga):**

```csharp
public class OrderSaga
{
    public IObservable<SagaResult> ExecuteOrderSaga(Order order)
    {
        return Observable.Create<SagaResult>(async observer =>
        {
            try
            {
                // Step 1: Reserve Inventory
                await inventoryService.ReserveAsync(order.Items);

                // Step 2: Process Payment
                await paymentService.ChargeAsync(order.Payment);

                // Step 3: Ship Order
                await shippingService.ShipAsync(order);

                observer.OnNext(SagaResult.Success);
                observer.OnCompleted();
            }
            catch (Exception ex)
            {
                // Compensating transactions
                await inventoryService.ReleaseAsync(order.Items);
                await paymentService.RefundAsync(order.Payment);

                observer.OnError(ex);
            }

            return Disposable.Empty;
        });
    }
}
```

---

## 📔 Part 7: 테스팅과 디버깅

### Chapter 20: 단위 테스트

**[TestScheduler](https://learn.microsoft.com/en-us/previous-versions/dotnet/reactive-extensions/hh212074(v=vs.103)) 활용:**

```csharp
[Fact]
public void Test_Throttle()
{
    var scheduler = new TestScheduler();
    var source = scheduler.CreateHotObservable(
        OnNext(100, 1),
        OnNext(200, 2),
        OnNext(250, 3),  // 이것은 throttle됨
        OnNext(400, 4),
        OnCompleted<int>(500)
    );

    var result = source.Throttle(TimeSpan.FromTicks(100), scheduler);

    var observer = scheduler.Start(
        () => result,
        created: 0,
        subscribed: 0,
        disposed: 1000);

    observer.Messages.AssertEqual(
        OnNext(300, 2),  // 200ms + 100ms throttle
        OnNext(500, 4),
        OnCompleted<int>(500)
    );
}
```

**Marble Testing:**

```csharp
// Marble diagram: --1--2----3-|
// Throttle(2):     -----2------3|
```

### Chapter 21: 디버깅 기법

**[Do](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.do) (Tap) - 부작용 없는 관찰:**

```csharp
Observable.Range(1, 5)
    .Do(x => Console.WriteLine($"Before: {x}"))
    .Where(x => x % 2 == 0)
    .Do(x => Console.WriteLine($"After filter: {x}"))
    .Select(x => x * x)
    .Do(x => Console.WriteLine($"After select: {x}"))
    .Subscribe(x => Console.WriteLine($"Final: {x}"));
```

**[Materialize](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.materialize)/Dematerialize:**

```csharp
// 모든 알림을 데이터로 변환
source
    .Materialize()
    .Subscribe(notification =>
    {
        if (notification.Kind == NotificationKind.OnNext)
            Console.WriteLine($"Value: {notification.Value}");
        else if (notification.Kind == NotificationKind.OnError)
            Console.WriteLine($"Error: {notification.Exception.Message}");
        else
            Console.WriteLine("Completed");
    });
```

---

## 📖 Part 8: 부록

### Appendix A: Rx Operator 빠른 참조

**생성 연산자:**
- [Observable.Return](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.return) - 단일 값
- [Observable.Range](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.range) - 연속된 정수
- [Observable.Interval](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.interval) - 주기적 값
- [Observable.Timer](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.timer) - 지연 후 값
- [Observable.Create](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.create) - 커스텀 생성

**변환 연산자:**
- [Select](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.select) - 각 요소 변환
- [SelectMany](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.selectmany) - 평탄화
- [Scan](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.scan) - 누적 연산
- [GroupBy](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.groupby) - 그룹핑
- [Buffer](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.buffer) / [Window](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.window) - 배치 처리

**필터링 연산자:**
- [Where](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.where) - 조건 필터
- [Take](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.take) / [Skip](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.skip) - 요소 선택/건너뛰기
- [Distinct](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.distinct) - 중복 제거
- [Throttle](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.throttle) / [Debounce](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.debounce) - 이벤트 제한
- [Sample](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.sample) - 주기적 샘플링

**결합 연산자:**
- [Merge](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.merge) - 병합
- [Concat](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.concat) - 순차 연결
- [Zip](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.zip) - 쌍으로 조합
- [CombineLatest](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.combinelatest) - 최신 값 조합
- [Switch](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.switch) - 스트림 전환

**에러 처리:**
- [Catch](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.catch) - 에러 처리
- [Retry](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.retry) - 재시도
- [Finally](https://learn.microsoft.com/en-us/dotnet/api/system.reactive.linq.observable.finally) - 정리 작업

### Appendix B: 베스트 프랙티스 체크리스트

✅ **구독 관리**
- 모든 구독을 Dispose하거나 CompositeDisposable로 관리
- ViewModel/Component의 수명주기와 연동
- using 패턴 활용

✅ **성능**
- 무거운 연산 전에 Take/Where로 필터링
- Share/Publish로 Hot Observable 공유
- 적절한 Scheduler 사용

✅ **에러 처리**
- 모든 Observable에 OnError 핸들러 제공
- Catch/Retry로 복원력 확보
- Finally로 리소스 정리 보장

✅ **테스팅**
- TestScheduler로 시간 기반 테스트
- IScheduler 주입으로 테스트 가능성 확보

### Appendix C: 마이그레이션 가이드

**이벤트 -> Observable:**

```csharp
// Before
button.Click += OnButtonClick;

// After
Observable.FromEventPattern(h => button.Click += h, h => button.Click -= h)
    .Subscribe(_ => OnButtonClick());
```

**async/await -> Rx:**

```csharp
// Before
var result = await GetDataAsync();
ProcessData(result);

// After
Observable.FromAsync(() => GetDataAsync())
    .Subscribe(result => ProcessData(result));

// 또는 Task를 Observable로 변환
GetDataAsync().ToObservable()
    .Subscribe(result => ProcessData(result));
```

### Appendix D: 용어집(Glossary)

- **Observable** - 시간에 따라 값을 방출하는 데이터 스트림
- **Observer** - Observable을 구독하여 값을 받는 객체
- **Subject** - Observable이자 Observer인 양방향 브리지
- **Cold Observable** - 구독 시 시작되는 Observable (예: HTTP 요청)
- **Hot Observable** - 이미 실행 중인 Observable (예: 마우스 이벤트)
- **Scheduler** - 작업 실행의 시기와 위치를 제어
- **Marble Diagram** - Observable 시퀀스의 시각적 표현
- **Backpressure** - 생산자가 소비자보다 빠를 때의 압력
- **Dispose** - 구독 해제 및 리소스 정리

### Appendix E: 추가 리소스

**공식 문서:**
- [Reactive Extensions 공식 사이트](http://reactivex.io/)
- [Rx.NET GitHub](https://github.com/dotnet/reactive)
- [Microsoft Docs - Reactive Extensions](https://learn.microsoft.com/en-us/dotnet/api/system.reactive)
- [Introduction to Rx](http://introtorx.com/)

**커뮤니티 리소스:**
- [ReactiveUI](https://www.reactiveui.net/) - MVVM 프레임워크
- [Akka.NET](https://getakka.net/) - 액터 모델 with Rx
- [DynamicData](https://github.com/reactivemarbles/DynamicData) - Reactive Collections

**관련 라이브러리:**
- System.Reactive - 핵심 Rx 라이브러리
- System.Reactive.Linq - LINQ 연산자
- System.Reactive.Subjects - Subject 구현
- System.Reactive.Concurrency - Scheduler 구현

**학습 자료:**
- [Intro to Rx eBook](http://introtorx.com/)
- [ReactiveX Documentation](http://reactivex.io/documentation/operators.html)
- [Channel 9 - Rx 비디오](https://channel9.msdn.com/Tags/reactive+extensions)

---

## 💡 시작하기

### NuGet 패키지 설치:

```bash
dotnet add package System.Reactive
dotnet add package System.Reactive.Linq
```

### 기본 예제:

```csharp
using System;
using System.Reactive.Linq;

// 간단한 Observable 생성
var numbers = Observable.Range(1, 10);

// 변환 및 필터링
var evenSquares = numbers
    .Where(x => x % 2 == 0)
    .Select(x => x * x);

// 구독
evenSquares.Subscribe(
    x => Console.WriteLine($"Value: {x}"),
    ex => Console.WriteLine($"Error: {ex.Message}"),
    () => Console.WriteLine("Completed")
);
```

---

## 📞 피드백 및 기여

이 가이드에 대한 피드백이나 개선 제안은 환영합니다!

---

**만든이:** Reactive Extensions 커뮤니티
**마지막 업데이트:** 2025
**라이센스:** MIT

---

## 📔 Part 7: 테스팅과 디버깅

### Chapter 20: 단위 테스트
- 20.1 TestScheduler 활용
  - 가상 시간 제어
  - 결정적 테스트 작성
- 20.2 Marble Testing
  - Marble 다이어그램 이해
  - 테스트 시나리오 작성
- 20.3 Mock과 Stub
  - Observable 모킹
  - 테스트 더블 패턴

### Chapter 21: 디버깅 기법
- 21.1 디버깅 연산자
  - Do (Tap)
  - Materialize/Dematerialize
- 21.2 로깅과 추적
  - 커스텀 로깅 연산자
  - 성능 프로파일링
- 21.3 일반적인 함정과 해결책
  - 메모리 누수 패턴
  - 데드락 방지

---

## 📖 Part 8: 부록

### Appendix A: Rx Operator 빠른 참조
- 카테고리별 연산자 목록
- 사용 예제와 Marble 다이어그램

### Appendix B: 베스트 프랙티스 체크리스트
- 코드 리뷰 가이드라인
- 안티패턴 목록

### Appendix C: 마이그레이션 가이드
- 이벤트 기반 코드를 Rx로 전환
- async/await와 Rx 통합

### Appendix D: 용어집(Glossary)
- Rx 관련 용어 정리
- 함수형 프로그래밍 용어

### Appendix E: 추가 리소스
- 공식 문서 링크
- 커뮤니티 리소스
- 관련 라이브러리 (ReactiveUI, Akka.NET 등)

---

## 📚 실습 프로젝트 저장소
- GitHub 저장소 구조
- 챕터별 예제 코드
- 도전 과제와 해답
