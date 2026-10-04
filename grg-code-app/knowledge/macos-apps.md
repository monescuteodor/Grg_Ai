# macOS apps (native)

## Stack
- **SwiftUI** (declarative, modern) — default for new apps. AppKit for advanced/legacy controls.
- Xcode is required to build/sign/ship. Language: Swift.

## Quickstart
- Xcode -> new App -> SwiftUI lifecycle. Or Swift Package for logic.
```swift
import SwiftUI
@main struct MyApp: App {
  var body: some Scene { WindowGroup { ContentView() } }
}
struct ContentView: View {
  @State var n = 0
  var body: some View { VStack { Text("\(n)"); Button("Add"){ n += 1 } }.padding() }
}
```

## State & data
- `@State`, `@Binding`, `@Observable` (Observation) / `ObservableObject`.
- Persistence: `UserDefaults`, `SwiftData` (modern) or Core Data.

## Ship
- Signing: Developer ID cert. **Notarize** (`xcrun notarytool submit`) then staple, or ship via the App Store.
- Distribute a `.dmg` (create-dmg) or `.pkg`. Sandbox + entitlements for App Store.

## Tips
- Menu bar app: `MenuBarExtra`. Background: launch agents.
- Universal binary (Apple Silicon + Intel): build for `arm64` + `x86_64`.
