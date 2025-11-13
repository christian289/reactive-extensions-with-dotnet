### Chapter 18: UI 이벤트 처리

**자동 완성 구현:**

```csharp
public class AutoCompleteViewModel
{
    public AutoCompleteViewModel()
    {
        var searchText = this.WhenAnyValue(x => x.SearchText);

        Suggestions = searchText
            .Throttle(TimeSpan.FromMilliseconds(300))  // 입력 완료 대기
            .DistinctUntilChanged()                    // 중복 제거
            .Where(text => text?.Length >= 3)          // 최소 3글자
            .SelectMany(text => GetSuggestionsAsync(text))  // API 호출
            .Catch(Observable.Return(Array.Empty<string>()))  // 에러 처리
            .ObserveOn(RxApp.MainThreadScheduler)      // UI 스레드
            .ToProperty(this, x => x.Suggestions);
    }
}
```

**드래그 앤 드롭:**

```csharp
var mouseDown = Observable.FromEventPattern<MouseEventArgs>(
    h => canvas.MouseDown += h,
    h => canvas.MouseDown -= h);

var mouseMove = Observable.FromEventPattern<MouseEventArgs>(
    h => canvas.MouseMove += h,
    h => canvas.MouseMove -= h);

var mouseUp = Observable.FromEventPattern<MouseEventArgs>(
    h => canvas.MouseUp += h,
    h => canvas.MouseUp -= h);

// 드래그 제스처
var drags = from down in mouseDown
            let startPos = down.EventArgs.GetPosition(canvas)
            from move in mouseMove.TakeUntil(mouseUp)
            let currentPos = move.EventArgs.GetPosition(canvas)
            select new { Start = startPos, Current = currentPos };

drags.Subscribe(drag =>
{
    var deltaX = drag.Current.X - drag.Start.X;
    var deltaY = drag.Current.Y - drag.Start.Y;
    UpdateElementPosition(deltaX, deltaY);
});
```
