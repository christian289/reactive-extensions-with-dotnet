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
