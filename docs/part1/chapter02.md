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
