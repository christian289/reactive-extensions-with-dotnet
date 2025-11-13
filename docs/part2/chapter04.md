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
