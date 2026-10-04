# Android native (Jetpack Compose) — deep

Language: Kotlin. IDE: Android Studio. For cross-platform JS, see `mobile-ios-android`.

## App skeleton
```kotlin
class MainActivity : ComponentActivity() {
  override fun onCreate(b: Bundle?) { super.onCreate(b)
    setContent { MaterialTheme { Screen() } } }
}
@Composable fun Screen() {
  var n by remember { mutableStateOf(0) }
  Column(Modifier.padding(16.dp)) {
    Text("Count: $n")
    Button(onClick = { n++ }) { Text("Add") }
  }
}
```

## Essentials
- UI: Jetpack Compose + Material 3. State: `remember`/`mutableStateOf`, `ViewModel` + `StateFlow`.
- Async: Kotlin coroutines (`viewModelScope.launch`), `suspend` funcs.
- Networking: Retrofit + OkHttp + kotlinx.serialization/Moshi.
- Persistence: Room (SQLite) or DataStore (prefs).
- DI: Hilt.

## Ship to Play Store
- `./gradlew bundleRelease` -> signed **.aab** (App Bundle). Manage signing key (keep it safe / Play App Signing).
- Play Console: create app, upload aab, fill data safety + content rating, staged rollout.

## Tips
- Min SDK ~24+, target the latest SDK. Test on multiple screen sizes.
- Use `Modifier` order intentionally; hoist state; keep composables pure.
