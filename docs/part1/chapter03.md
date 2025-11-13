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
