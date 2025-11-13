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
