# iOS native (SwiftUI) — deep

Needs a Mac + Xcode. For cross-platform JS, see `mobile-ios-android` (Expo/React Native).

## App skeleton
```swift
import SwiftUI
@main struct MyApp: App { var body: some Scene { WindowGroup { RootView() } } }
struct RootView: View {
  @State private var items: [String] = []
  var body: some View {
    NavigationStack {
      List(items, id: \.self) { Text($0) }
        .navigationTitle("Items")
        .toolbar { Button("Add") { items.append("Item \(items.count+1)") } }
    }
  }
}
```

## Essentials
- State: `@State`, `@Binding`, `@Observable` model + `@Environment`.
- Networking: `URLSession` with `async/await`; decode with `Codable`.
- Persistence: `SwiftData` (`@Model`) or Core Data; small prefs in `@AppStorage`.
- Navigation: `NavigationStack` + value-based `navigationDestination`.

## Ship to App Store
- Bump bundle id + version/build. Signing via Xcode automatic signing (needs Apple Developer account, $99/yr).
- Archive -> Distribute -> App Store Connect -> TestFlight -> review.
- Respect App Review: privacy nutrition labels, ATT for tracking, no private APIs.

## Tips
- Previews (`#Preview`) for fast iteration. Use `Instruments` for performance.
- Accessibility: `.accessibilityLabel`, Dynamic Type, VoiceOver.
