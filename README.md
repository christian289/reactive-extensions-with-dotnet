# Reactive Extensions(Rx.NET) 완벽 가이드
### 초보자부터 실무까지의 반응형 프로그래밍 여정

---

## 📘 Part 1: 기초 개념과 철학

### Chapter 1: Reactive Extensions 소개
- 1.1 Reactive Programming이란 무엇인가?
  - 반응형 프로그래밍 패러다임의 이해
  - 명령형 프로그래밍 vs 선언적 프로그래밍
  - Push 모델 vs Pull 모델
- 1.2 Rx.NET의 탄생 배경과 역사
  - Observer 패턴의 한계
  - 비동기 프로그래밍의 복잡성 해결
- 1.3 왜 Reactive Extensions를 사용해야 하는가?
  - 실시간 데이터 스트림 처리
  - 이벤트 기반 프로그래밍의 단순화
  - 비동기 작업의 구성 가능성(Composability)

### Chapter 2: 필수 기반 지식
- 2.1 .NET의 비동기 프로그래밍 모델
  - Task와 async/await 이해
  - 이벤트와 델리게이트
- 2.2 LINQ(Language Integrated Query) 기초
  - LINQ 쿼리 문법
  - 메서드 체인과 함수형 프로그래밍
- 2.3 디자인 패턴 기초
  - Observer 패턴
  - Iterator 패턴
  - Pub-Sub 패턴

### Chapter 3: Rx의 핵심 타입과 인터페이스
- 3.1 IObservable<T>와 IObserver<T>
  - Observable과 Observer의 계약
  - OnNext, OnError, OnCompleted 규칙
- 3.2 ISubject<T> 인터페이스
  - Subject의 이중성: Observer이자 Observable
  - Subject 타입들: Subject, BehaviorSubject, ReplaySubject, AsyncSubject
- 3.3 IScheduler 인터페이스
  - 동시성과 시간 관리
  - 스케줄러의 역할과 중요성

---

## 📗 Part 2: Observable 시퀀스 생성과 구독

### Chapter 4: Observable 생성 패턴
- 4.1 Factory 메서드를 통한 생성
  - Observable.Return, Observable.Empty, Observable.Never
  - Observable.Throw, Observable.Range
- 4.2 시간 기반 Observable 생성
  - Observable.Timer
  - Observable.Interval
  - Observable.Generate
- 4.3 이벤트를 Observable로 변환
  - Observable.FromEventPattern
  - .NET 이벤트 연동
  - FileSystemWatcher 예제
- 4.4 Observable.Create를 통한 커스텀 구현
  - 리소스 관리와 Disposal
  - 동시성 규칙 준수

### Chapter 5: 구독과 생명주기 관리
- 5.1 Subscribe 메서드와 IDisposable
  - 구독 해제의 중요성
  - using 패턴과 CompositeDisposable
- 5.2 Hot vs Cold Observable
  - 구독 시점과 데이터 스트림
  - Publish와 Connect를 통한 변환
- 5.3 Subject 활용 패턴
  - 메시지 큐 브리징
  - 이벤트 집계자(Event Aggregator) 패턴

---

## 📙 Part 3: Rx Operators 완벽 가이드

### Chapter 6: 변환(Transformation) 연산자
- 6.1 기본 변환 연산자
  - Select (Map)
  - SelectMany (FlatMap)
  - Cast, OfType
- 6.2 고급 변환 패턴
  - Scan (누적)
  - GroupBy
  - Buffer와 Window

### Chapter 7: 필터링(Filtering) 연산자
- 7.1 조건 기반 필터링
  - Where
  - Take, Skip
  - TakeWhile, SkipWhile
- 7.2 중복 제거와 샘플링
  - Distinct, DistinctUntilChanged
  - Sample, Throttle
  - Debounce

### Chapter 8: 결합(Combining) 연산자
- 8.1 순차적 결합
  - Concat
  - StartWith
  - Append, Prepend
- 8.2 동시적 결합
  - Merge
  - Zip
  - CombineLatest
- 8.3 조건부 결합
  - Amb (Ambiguous)
  - Switch
  - WithLatestFrom

### Chapter 9: 집계(Aggregation) 연산자
- 9.1 기본 집계 연산
  - Count, Sum, Average
  - Min, Max
  - Aggregate (Reduce)
- 9.2 조건부 집계
  - Any, All
  - Contains
  - ElementAt, First, Last

### Chapter 10: 에러 처리와 복구
- 10.1 에러 처리 전략
  - Catch
  - OnErrorResumeNext
- 10.2 재시도 메커니즘
  - Retry
  - RetryWhen
- 10.3 리소스 관리
  - Using
  - Finally

---

## 📕 Part 4: 고급 개념과 패턴

### Chapter 11: Scheduling과 동시성
- 11.1 Scheduler 타입과 특징
  - ImmediateScheduler
  - CurrentThreadScheduler  
  - EventLoopScheduler
  - NewThreadScheduler
  - TaskPoolScheduler (ThreadPoolScheduler)
- 11.2 SubscribeOn vs ObserveOn
  - 실행 컨텍스트 제어
  - UI 스레드와의 상호작용
- 11.3 TestScheduler와 가상 시간
  - 단위 테스트를 위한 시간 제어
  - Marble Testing

### Chapter 12: 시간 기반 연산자
- 12.1 시간 지연과 이동
  - Delay
  - Timeout
  - Timestamp, TimeInterval
- 12.2 시간 윈도우 연산
  - Buffer with time
  - Window with time
  - Throttle vs Debounce 심화

### Chapter 13: Backpressure와 Flow Control
- 13.1 Backpressure 이해하기
  - 생산자-소비자 속도 불일치 문제
  - 버퍼 오버플로우 방지
- 13.2 Flow Control 전략
  - Buffering 전략
  - Dropping 전략
  - Latest/Sample 전략

---

## 📒 Part 5: 실무 패턴과 최적화

### Chapter 14: 함수형 반응형 프로그래밍 (FRP)
- 14.1 함수형 프로그래밍 원칙
  - 불변성(Immutability)
  - 순수 함수(Pure Functions)
  - 고차 함수(Higher-Order Functions)
- 14.2 Rx와 함수형 패러다임
  - 모나드로서의 Observable
  - 함수 합성과 파이프라이닝

### Chapter 15: OOP vs Reactive 패러다임
- 15.1 패러다임 차이점
  - 상태 관리의 차이
  - 제어 흐름의 역전
  - 명령형 vs 선언적 스타일
- 15.2 하이브리드 접근법
  - 기존 OOP 코드베이스와 통합
  - MVVM 패턴과 Rx
  - ReactiveUI 프레임워크

### Chapter 16: 성능 최적화
- 16.1 메모리 관리
  - 구독 누수 방지
  - WeakReference 패턴
- 16.2 연산자 체인 최적화
  - 연산자 순서의 중요성
  - Share, Publish, RefCount 활용
- 16.3 커스텀 연산자 구현
  - 성능을 위한 특수 연산자

---

## 📓 Part 6: 실전 프로젝트

### Chapter 17: 실시간 데이터 처리 시스템
- 17.1 주식 시세 모니터링 시스템
  - 실시간 가격 스트림 처리
  - 이동 평균 계산
  - 알림 시스템 구현
- 17.2 센서 데이터 집계
  - IoT 디바이스 데이터 수집
  - 이상치 감지
  - 대시보드 업데이트

### Chapter 18: UI 이벤트 처리
- 18.1 WPF/WinForms와 Rx
  - 복잡한 사용자 상호작용 처리
  - 자동 완성 구현
  - 드래그 앤 드롭 처리
- 18.2 웹 애플리케이션 (SignalR)
  - 실시간 채팅 구현
  - 협업 도구 개발

### Chapter 19: 마이크로서비스와 이벤트 소싱
- 19.1 Event-Driven Architecture
  - 메시지 브로커 통합 (Kafka, RabbitMQ)
  - CQRS 패턴 구현
- 19.2 분산 시스템에서의 Rx
  - 서비스 간 통신
  - 사가(Saga) 패턴

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
