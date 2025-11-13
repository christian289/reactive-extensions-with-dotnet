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
