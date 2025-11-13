### Chapter 15: OOP vs Reactive 패러다임

**[MVVM](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/data-binding-overview) 패턴과 Rx:**

```csharp
public class SearchViewModel : INotifyPropertyChanged
{
    private readonly Subject<string> _searchQuery = new Subject<string>();

    public string SearchText
    {
        set => _searchQuery.OnNext(value);
    }

    public SearchViewModel()
    {
        // 자동 검색with 디바운싱
        _searchQuery
            .Throttle(TimeSpan.FromMilliseconds(300))
            .DistinctUntilChanged()
            .SelectMany(query => SearchAsync(query))
            .ObserveOn(SynchronizationContext.Current)
            .Subscribe(results => SearchResults = results);
    }
}
```

**[ReactiveUI](https://www.reactiveui.net/) 프레임워크:**

```csharp
public class MyViewModel : ReactiveObject
{
    private string _searchQuery;
    public string SearchQuery
    {
        get => _searchQuery;
        set => this.RaiseAndSetIfChanged(ref _searchQuery, value);
    }

    public MyViewModel()
    {
        // ReactiveCommand
        var canSearch = this.WhenAnyValue(x => x.SearchQuery)
            .Select(q => !string.IsNullOrWhiteSpace(q));

        SearchCommand = ReactiveCommand.CreateFromTask(
            async () => await SearchAsync(SearchQuery),
            canSearch);
    }
}
```
