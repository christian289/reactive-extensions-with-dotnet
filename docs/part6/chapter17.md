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
