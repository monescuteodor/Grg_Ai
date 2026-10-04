# Mobile app building — iOS & Android

## Pick the stack
- **React Native + Expo** (recommended default): one codebase → iOS + Android + web. Fastest to ship, huge ecosystem, OTA updates. Use TypeScript.
- **Flutter** (Dart): great performance + polished UI, single codebase. Good when you want pixel-perfect custom UI.
- **Native**: iOS = Swift + SwiftUI; Android = Kotlin + Jetpack Compose. Use when you need deep platform features or max performance.

## React Native + Expo
- Scaffold: `npx create-expo-app@latest my-app -t` (TS template). Run: `npx expo start` (Expo Go app or dev build). Build: **EAS** — `eas build -p ios` / `-p android`; submit: `eas submit`.
- Routing: **expo-router** (file-based, like Next.js) — `app/index.tsx`, `app/(tabs)/…`, `app/[id].tsx`.
- Core UI: `View`, `Text`, `Pressable`, `FlatList` (virtualized lists — never `.map` big lists), `SafeAreaView`. Style via `StyleSheet.create` or NativeWind (Tailwind for RN).
- State/data: Zustand or Redux Toolkit; server state with TanStack Query. Storage: `expo-secure-store` (secrets), `AsyncStorage` (prefs).
- Native APIs via Expo modules: `expo-camera`, `expo-image-picker`, `expo-notifications`, `expo-location`, `expo-av`. Permissions: request at point of use; declare in `app.json`.
- Navigation patterns: stack + bottom tabs; deep links via expo-router.

## Flutter
- `flutter create my_app`; run `flutter run`; build `flutter build apk` / `flutter build ipa`.
- Widgets everything; `StatelessWidget`/`StatefulWidget`; state mgmt: Riverpod or Bloc. Navigation: `go_router`. HTTP: `dio`.

## Native quick refs
- **SwiftUI**: `struct ContentView: View { var body: some View { … } }`; state `@State`/`@Observable`; navigation `NavigationStack`. Xcode + simulator; distribute via App Store Connect / TestFlight.
- **Jetpack Compose**: `@Composable fun Screen() { … }`; state `remember { mutableStateOf() }`; navigation `NavHost`. Android Studio + emulator; distribute via Play Console.

## Shipping (both stores)
- iOS: Apple Developer account ($99/yr), bundle id, signing/provisioning, App Store Connect, TestFlight for beta, review guidelines.
- Android: Google Play Console ($25 once), signed AAB (`app bundle`), internal testing track → production.
- Icons/splash: `expo-splash-screen` + app icon sets; version + build number bumps each release.

## UX for mobile
- Touch targets ≥ 44pt; respect safe areas/notches; support light/dark; handle keyboard avoidance; test on small + large devices; offline states; fast lists (virtualized).
