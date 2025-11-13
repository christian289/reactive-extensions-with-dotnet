# Reactive Extensions(Rx.NET) 완벽 가이드
### 초보자부터 실무까지의 반응형 프로그래밍 여정

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 소개

이 가이드는 Reactive Extensions for .NET (Rx.NET)에 대한 포괄적인 한국어 학습 자료입니다. 기초 개념부터 실무 패턴까지, 반응형 프로그래밍의 모든 것을 다룹니다.

### ✨ 특징

- 📘 **체계적인 학습 경로**: 8개 Part, 21개 Chapter로 구성된 단계별 학습
- 💻 **풍부한 예제**: 100개 이상의 실전 C# 코드 예제
- 🔗 **풍부한 참조**: Microsoft Docs 및 공식 문서 링크
- 🎯 **실무 중심**: 실제 프로젝트에 적용 가능한 패턴과 베스트 프랙티스

### 🚀 시작하기

#### NuGet 패키지 설치:

```bash
dotnet add package System.Reactive
dotnet add package System.Reactive.Linq
```

#### 첫 번째 예제:

```csharp
using System;
using System.Reactive.Linq;

var numbers = Observable.Range(1, 10)
    .Where(x => x % 2 == 0)
    .Select(x => x * x);

numbers.Subscribe(x => Console.WriteLine($"Value: {x}"));
// 출력: Value: 4, Value: 16, Value: 36, Value: 64, Value: 100
```

---

## 📚 목차

### 📘 Part 1: 기초 개념과 철학

반응형 프로그래밍의 기본 개념과 Rx.NET의 핵심 타입을 학습합니다.

- **[Chapter 1: Reactive Extensions 소개](docs/part1/chapter01.md)**
  - Reactive Programming 패러다임
  - 명령형 vs 선언적 프로그래밍
  - Push vs Pull 모델
  - Rx.NET의 탄생 배경과 역사

- **[Chapter 2: 필수 기반 지식](docs/part1/chapter02.md)**
  - .NET의 비동기 프로그래밍 (Task, async/await)
  - LINQ 기초
  - 디자인 패턴 (Observer, Iterator, Pub-Sub)

- **[Chapter 3: Rx의 핵심 타입과 인터페이스](docs/part1/chapter03.md)**
  - IObservable<T>와 IObserver<T>
  - Subject 타입들 (Subject, BehaviorSubject, ReplaySubject, AsyncSubject)
  - IScheduler와 동시성 관리

### 📗 Part 2: Observable 시퀀스 생성과 구독

Observable을 생성하고 구독하는 다양한 방법을 학습합니다.

- **[Chapter 4: Observable 생성 패턴](docs/part2/chapter04.md)**
  - Factory 메서드 (Return, Empty, Never, Throw, Range)
  - 시간 기반 생성 (Timer, Interval, Generate)
  - 이벤트를 Observable로 변환 (FromEventPattern)
  - Observable.Create를 통한 커스텀 구현

- **[Chapter 5: 구독과 생명주기 관리](docs/part2/chapter05.md)**
  - Subscribe 메서드와 IDisposable
  - Hot vs Cold Observable
  - Subject 활용 패턴

### 📙 Part 3: Rx Operators 완벽 가이드

Rx의 강력한 연산자들을 마스터합니다.

- **[Chapter 6: 변환(Transformation) 연산자](docs/part3/chapter06.md)**
  - Select, SelectMany, Cast, OfType
  - Scan, GroupBy, Buffer, Window

- **[Chapter 7: 필터링(Filtering) 연산자](docs/part3/chapter07.md)**
  - Where, Take, Skip
  - Distinct, DistinctUntilChanged
  - Throttle, Debounce, Sample

- **[Chapter 8: 결합(Combining) 연산자](docs/part3/chapter08.md)**
  - Concat, StartWith, Merge
  - Zip, CombineLatest
  - Amb, Switch, WithLatestFrom

- **[Chapter 9: 집계(Aggregation) 연산자](docs/part3/chapter09.md)**
  - Count, Sum, Average, Min, Max
  - Aggregate (Reduce)
  - Any, All, Contains

- **[Chapter 10: 에러 처리와 복구](docs/part3/chapter10.md)**
  - Catch, OnErrorResumeNext
  - Retry, RetryWhen
  - Using, Finally

### 📕 Part 4: 고급 개념과 패턴

고급 기능과 패턴을 학습합니다.

- **[Chapter 11: Scheduling과 동시성](docs/part4/chapter11.md)**
  - Scheduler 타입과 특징
  - SubscribeOn vs ObserveOn
  - TestScheduler와 가상 시간

- **[Chapter 12: 시간 기반 연산자](docs/part4/chapter12.md)**
  - Delay, Timeout
  - Buffer/Window with time
  - Throttle vs Debounce 심화

- **[Chapter 13: Backpressure와 Flow Control](docs/part4/chapter13.md)**
  - Backpressure 이해하기
  - Flow Control 전략

### 📒 Part 5: 실무 패턴과 최적화

실무에서 사용하는 패턴과 최적화 기법을 다룹니다.

- **[Chapter 14: 함수형 반응형 프로그래밍 (FRP)](docs/part5/chapter14.md)**
  - 함수형 프로그래밍 원칙
  - Observable as Monad

- **[Chapter 15: OOP vs Reactive 패러다임](docs/part5/chapter15.md)**
  - 패러다임 차이점
  - MVVM 패턴과 Rx
  - ReactiveUI 프레임워크

- **[Chapter 16: 성능 최적화](docs/part5/chapter16.md)**
  - 메모리 관리와 구독 누수 방지
  - 연산자 체인 최적화

### 📓 Part 6: 실전 프로젝트

실제 프로젝트 예제로 배운 내용을 적용합니다.

- **[Chapter 17: 실시간 데이터 처리 시스템](docs/part6/chapter17.md)**
  - 주식 시세 모니터링 시스템
  - 센서 데이터 집계

- **[Chapter 18: UI 이벤트 처리](docs/part6/chapter18.md)**
  - WPF/WinForms와 Rx
  - 자동 완성, 드래그 앤 드롭 구현

- **[Chapter 19: 마이크로서비스와 이벤트 소싱](docs/part6/chapter19.md)**
  - Event-Driven Architecture
  - CQRS와 Saga 패턴

### 📔 Part 7: 테스팅과 디버깅

테스트와 디버깅 기법을 학습합니다.

- **[Chapter 20: 단위 테스트](docs/part7/chapter20.md)**
  - TestScheduler 활용
  - Marble Testing

- **[Chapter 21: 디버깅 기법](docs/part7/chapter21.md)**
  - Do (Tap) 연산자
  - Materialize/Dematerialize

### 📖 Part 8: 부록

참조 자료와 추가 리소스를 제공합니다.

- **[Appendix A: Rx Operator 빠른 참조](docs/appendix/appendix-a.md)**
  - 연산자 카테고리별 목록
  - Microsoft Docs 링크

- **[Appendix B: 베스트 프랙티스 체크리스트](docs/appendix/appendix-b.md)**
  - 구독 관리, 성능, 에러 처리
  - 코드 리뷰 가이드라인

- **[Appendix C: 마이그레이션 가이드](docs/appendix/appendix-c.md)**
  - 이벤트를 Observable로 변환
  - async/await를 Rx로 통합

- **[Appendix D: 용어집(Glossary)](docs/appendix/appendix-d.md)**
  - Rx 관련 용어 정리
  - 함수형 프로그래밍 용어

- **[Appendix E: 추가 리소스](docs/appendix/appendix-e.md)**
  - 공식 문서 링크
  - 커뮤니티 리소스
  - 관련 라이브러리

---

## 🎯 학습 로드맵

### 초급자 (1-2주)
1. Part 1: 기초 개념 (Chapter 1-3)
2. Part 2: Observable 생성 (Chapter 4-5)
3. Part 3: 기본 연산자 (Chapter 6-7)

### 중급자 (2-3주)
1. Part 3: 고급 연산자 (Chapter 8-10)
2. Part 4: 스케줄링과 시간 (Chapter 11-13)
3. Part 5: 실무 패턴 (Chapter 14-16)

### 고급자 (2-3주)
1. Part 6: 실전 프로젝트 (Chapter 17-19)
2. Part 7: 테스팅 (Chapter 20-21)
3. 자신만의 프로젝트에 적용

---

## 📊 통계

- **총 Chapter 수**: 21개
- **코드 예제**: 100개 이상
- **예제 코드 검증**: ✅ 모든 예제 문법 오류 없음
- **Microsoft Docs 참조**: 50개 이상
- **총 분량**: 2,500+ 라인

---

## 🔗 주요 참조 링크

### 공식 문서
- [Reactive Extensions 공식 사이트](http://reactivex.io/)
- [Rx.NET GitHub](https://github.com/dotnet/reactive)
- [Microsoft Docs - Reactive Extensions](https://learn.microsoft.com/en-us/dotnet/api/system.reactive)
- [Introduction to Rx](http://introtorx.com/)

### 프레임워크 & 라이브러리
- [ReactiveUI](https://www.reactiveui.net/) - MVVM 프레임워크
- [Akka.NET](https://getakka.net/) - 액터 모델 with Rx
- [DynamicData](https://github.com/reactivemarbles/DynamicData) - Reactive Collections

### 학습 자료
- [ReactiveX Documentation](http://reactivex.io/documentation/operators.html)
- [Intro to Rx eBook](http://introtorx.com/)

---

## 🤝 기여하기

이 가이드에 대한 피드백이나 개선 제안은 환영합니다!

### 기여 방법
1. 이슈 생성: 오타, 오류, 개선 제안
2. Pull Request: 새로운 예제나 설명 추가
3. 번역 참여: 다른 언어로 번역

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

## 📞 문의

질문이나 제안사항이 있으시면 Issue를 통해 연락주세요.

---

**만든이:** Reactive Extensions 커뮤니티
**마지막 업데이트:** 2025년 1월
**버전:** 1.0.0

---

## ⭐ 이 가이드가 도움이 되셨다면 Star를 눌러주세요!
