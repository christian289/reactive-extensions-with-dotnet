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
