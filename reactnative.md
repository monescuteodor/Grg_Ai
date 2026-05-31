# React Native Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH REACT NATIVE


## Remarks

React Native is a framework for building native mobile applications using JavaScript and React. Created by Facebook (Meta) in 2015. It uses native components instead of web views, giving near-native performance. Supports iOS and Android from a single codebase.

Tools: `react-native` CLI, `expo` (managed workflow), Metro bundler, Android Studio/Xcode.


## Hello World

```jsx
// App.jsx
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function App() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Hello, World!</Text>
      <Text style={styles.subtitle}>Hello, React Native!</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
  },
  subtitle: {
    fontSize: 18,
    color: '#666',
    marginTop: 10,
  },
});
```

```bash
# Expo (recommended for beginners)
npx create-expo-app MyApp
cd MyApp
npx expo start         # opens QR code, scan with Expo Go

# React Native CLI
npx react-native init MyApp
cd MyApp
npx react-native run-android
npx react-native run-ios
```


---

# CHAPTER 2: CORE COMPONENTS


## Built-in Components

```jsx
import React, { useState } from 'react';
import {
  View, Text, TouchableOpacity, TextInput,
  ScrollView, FlatList, Image, Switch,
  ActivityIndicator, Modal, Alert,
  StyleSheet, Platform
} from 'react-native';

// === VIEW (like div) ===
function ViewExample() {
  return (
    <View style={{ flex: 1, padding: 20 }}>
      <View style={{ backgroundColor: 'blue', height: 100 }} />
      <View style={{ flexDirection: 'row', gap: 10 }}>
        <View style={{ flex: 1, backgroundColor: 'red', height: 50 }} />
        <View style={{ flex: 2, backgroundColor: 'green', height: 50 }} />
      </View>
    </View>
  );
}

// === TEXT ===
function TextExample() {
  return (
    <View>
      <Text style={{ fontSize: 24, fontWeight: 'bold' }}>Heading</Text>
      <Text style={{ color: '#666', lineHeight: 24 }}>
        Paragraph text with{' '}
        <Text style={{ color: 'blue' }}>nested</Text>
        {' '}inline text.
      </Text>
      <Text numberOfLines={2} ellipsizeMode="tail">
        Long text that gets truncated after two lines...
      </Text>
    </View>
  );
}

// === TOUCHABLE / PRESSABLE ===
function ButtonExample() {
  const [count, setCount] = useState(0);
  return (
    <View>
      {/* TouchableOpacity - fades on press */}
      <TouchableOpacity
        style={styles.btn}
        onPress={() => setCount(count + 1)}
        onLongPress={() => Alert.alert('Long press!')}
        activeOpacity={0.7}
      >
        <Text style={styles.btnText}>Pressed {count} times</Text>
      </TouchableOpacity>

      {/* Pressable - more control */}
      <Pressable
        style={({ pressed }) => [styles.btn, pressed && { opacity: 0.5 }]}
        onPress={() => console.log('press')}
      >
        <Text>Pressable</Text>
      </Pressable>
    </View>
  );
}

// === TEXT INPUT ===
function InputExample() {
  const [text, setText] = useState('');
  return (
    <TextInput
      value={text}
      onChangeText={setText}
      placeholder="Type here..."
      placeholderTextColor="#999"
      style={styles.input}
      keyboardType="default"   // numeric, email-address, phone-pad
      autoCapitalize="none"
      autoCorrect={false}
      secureTextEntry={false}  // true for passwords
      multiline={false}
      maxLength={100}
      onSubmitEditing={() => console.log('submitted:', text)}
    />
  );
}

// === IMAGE ===
function ImageExample() {
  return (
    <View>
      {/* Local image */}
      <Image
        source={require('./assets/logo.png')}
        style={{ width: 100, height: 100 }}
        resizeMode="contain"  // cover, stretch, repeat, center
      />
      {/* Remote image */}
      <Image
        source={{ uri: 'https://example.com/image.jpg' }}
        style={{ width: 200, height: 150 }}
      />
    </View>
  );
}

// === SWITCH ===
function SwitchExample() {
  const [enabled, setEnabled] = useState(false);
  return (
    <Switch
      value={enabled}
      onValueChange={setEnabled}
      trackColor={{ false: '#ccc', true: '#007AFF' }}
      thumbColor={enabled ? '#fff' : '#f4f3f4'}
    />
  );
}

const styles = StyleSheet.create({
  btn: { backgroundColor: '#007AFF', padding: 12, borderRadius: 8 },
  btnText: { color: '#fff', textAlign: 'center', fontSize: 16 },
  input: {
    borderWidth: 1, borderColor: '#ddd', borderRadius: 8,
    padding: 12, fontSize: 16
  },
});
```


---

# CHAPTER 3: LISTS AND SCROLL


## FlatList and ScrollView

```jsx
import React from 'react';
import {
  FlatList, SectionList, ScrollView,
  View, Text, StyleSheet, RefreshControl
} from 'react-native';

// === FLATLIST (virtualized, performant) ===
const DATA = [
  { id: '1', title: 'Item One',   subtitle: 'First item' },
  { id: '2', title: 'Item Two',   subtitle: 'Second item' },
  { id: '3', title: 'Item Three', subtitle: 'Third item' },
];

function Item({ item }) {
  return (
    <View style={styles.item}>
      <Text style={styles.title}>{item.title}</Text>
      <Text style={styles.subtitle}>{item.subtitle}</Text>
    </View>
  );
}

function FlatListExample() {
  const [refreshing, setRefreshing] = React.useState(false);

  const onRefresh = React.useCallback(() => {
    setRefreshing(true);
    setTimeout(() => setRefreshing(false), 2000);
  }, []);

  return (
    <FlatList
      data={DATA}
      renderItem={({ item }) => <Item item={item} />}
      keyExtractor={item => item.id}
      ItemSeparatorComponent={() => <View style={styles.separator} />}
      ListHeaderComponent={<Text style={styles.header}>My List</Text>}
      ListFooterComponent={<Text style={styles.footer}>End</Text>}
      ListEmptyComponent={<Text>No items</Text>}
      numColumns={1}         // grid: numColumns={2}
      horizontal={false}     // horizontal scrolling
      showsVerticalScrollIndicator={false}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
      onEndReached={() => console.log('reached end')}
      onEndReachedThreshold={0.5}
      initialNumToRender={10}
      maxToRenderPerBatch={10}
      windowSize={5}
    />
  );
}

// === SECTIONLIST ===
const SECTIONS = [
  { title: 'Fruits', data: ['Apple', 'Banana', 'Cherry'] },
  { title: 'Vegetables', data: ['Carrot', 'Broccoli', 'Spinach'] },
];

function SectionListExample() {
  return (
    <SectionList
      sections={SECTIONS}
      keyExtractor={(item, idx) => item + idx}
      renderItem={({ item }) => <Text style={styles.item}>{item}</Text>}
      renderSectionHeader={({ section: { title } }) => (
        <Text style={styles.sectionHeader}>{title}</Text>
      )}
    />
  );
}

// === SCROLLVIEW (for small content) ===
function ScrollViewExample() {
  return (
    <ScrollView
      style={{ flex: 1 }}
      contentContainerStyle={{ padding: 20 }}
      showsVerticalScrollIndicator={false}
      scrollEventThrottle={16}
      onScroll={({ nativeEvent }) => {
        console.log(nativeEvent.contentOffset.y);
      }}
    >
      {Array.from({ length: 20 }, (_, i) => (
        <Text key={i} style={{ padding: 10 }}>Item {i + 1}</Text>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  item: { padding: 15, backgroundColor: '#fff' },
  title: { fontSize: 16, fontWeight: 'bold' },
  subtitle: { fontSize: 14, color: '#666' },
  separator: { height: 1, backgroundColor: '#eee' },
  header: { fontSize: 20, fontWeight: 'bold', padding: 15 },
  footer: { padding: 15, textAlign: 'center', color: '#999' },
  sectionHeader: {
    fontSize: 18, fontWeight: 'bold',
    backgroundColor: '#f0f0f0', padding: 10
  },
});
```


---

# CHAPTER 4: NAVIGATION


## React Navigation

```bash
npm install @react-navigation/native
npm install @react-navigation/stack
npm install @react-navigation/bottom-tabs
npm install @react-navigation/drawer
npx expo install react-native-screens react-native-safe-area-context
```

```jsx
import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

// === STACK NAVIGATOR ===
const Stack = createStackNavigator();

function HomeScreen({ navigation, route }) {
  return (
    <View style={styles.screen}>
      <Text style={styles.title}>Home Screen</Text>
      <Button
        title="Go to Details"
        onPress={() => navigation.navigate('Details', { id: 42 })}
      />
      <Button
        title="Go Back"
        onPress={() => navigation.goBack()}
      />
    </View>
  );
}

function DetailsScreen({ navigation, route }) {
  const { id } = route.params;
  return (
    <View style={styles.screen}>
      <Text style={styles.title}>Details (ID: {id})</Text>
      <Button title="Back" onPress={() => navigation.goBack()} />
      <Button
        title="Replace with Profile"
        onPress={() => navigation.replace('Profile')}
      />
    </View>
  );
}

function StackApp() {
  return (
    <Stack.Navigator
      initialRouteName="Home"
      screenOptions={{
        headerStyle: { backgroundColor: '#007AFF' },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: 'bold' },
      }}
    >
      <Stack.Screen
        name="Home"
        component={HomeScreen}
        options={{ title: 'My App' }}
      />
      <Stack.Screen
        name="Details"
        component={DetailsScreen}
        options={({ route }) => ({ title: `Item ${route.params.id}` })}
      />
    </Stack.Navigator>
  );
}

// === BOTTOM TABS ===
const Tab = createBottomTabNavigator();

function TabApp() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          // Return icon component based on route.name
          return <Text style={{ color, fontSize: size }}>
            {route.name === 'Home' ? '🏠' : '⚙️'}
          </Text>;
        },
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: 'gray',
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Settings" component={DetailsScreen} />
    </Tab.Navigator>
  );
}

// === MAIN APP ===
export default function App() {
  return (
    <NavigationContainer>
      <StackApp />
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
});
```


---

# CHAPTER 5: STATE AND HOOKS


## State Management

```jsx
import React, { useState, useEffect, useCallback,
  useMemo, useRef, useContext, createContext, useReducer } from 'react';
import { View, Text, Button } from 'react-native';

// === USESTATE ===
function Counter() {
  const [count, setCount] = useState(0);
  return (
    <View>
      <Text>{count}</Text>
      <Button title="+" onPress={() => setCount(c => c + 1)} />
      <Button title="-" onPress={() => setCount(c => c - 1)} />
    </View>
  );
}

// === USEREDUCER ===
const initialState = { count: 0, loading: false, error: null };

function reducer(state, action) {
  switch (action.type) {
    case 'INCREMENT': return { ...state, count: state.count + 1 };
    case 'DECREMENT': return { ...state, count: state.count - 1 };
    case 'RESET':     return initialState;
    default: throw new Error('Unknown action');
  }
}

function CounterWithReducer() {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <View>
      <Text>Count: {state.count}</Text>
      <Button title="+" onPress={() => dispatch({ type: 'INCREMENT' })} />
      <Button title="-" onPress={() => dispatch({ type: 'DECREMENT' })} />
      <Button title="Reset" onPress={() => dispatch({ type: 'RESET' })} />
    </View>
  );
}

// === USECONTEXT (global state) ===
const ThemeContext = createContext({ dark: false, toggle: () => {} });

function ThemeProvider({ children }) {
  const [dark, setDark] = useState(false);
  const toggle = useCallback(() => setDark(d => !d), []);
  return (
    <ThemeContext.Provider value={{ dark, toggle }}>
      {children}
    </ThemeContext.Provider>
  );
}

function ThemedComponent() {
  const { dark, toggle } = useContext(ThemeContext);
  return (
    <View style={{ backgroundColor: dark ? '#000' : '#fff', padding: 20 }}>
      <Text style={{ color: dark ? '#fff' : '#000' }}>
        {dark ? 'Dark' : 'Light'} Mode
      </Text>
      <Button title="Toggle" onPress={toggle} />
    </View>
  );
}

// === USEEFFECT ===
function DataFetcher({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);

    fetch(`https://api.example.com/users/${userId}`)
      .then(r => r.json())
      .then(data => {
        if (!cancelled) {
          setUser(data);
          setLoading(false);
        }
      })
      .catch(err => {
        if (!cancelled) setLoading(false);
      });

    return () => { cancelled = true; };  // cleanup
  }, [userId]);  // re-run when userId changes

  if (loading) return <Text>Loading...</Text>;
  if (!user)   return <Text>Not found</Text>;
  return <Text>{user.name}</Text>;
}

// === USEMEMO / USECALLBACK ===
function Expensive({ data, onPress }) {
  const processed = useMemo(() => {
    return data.filter(x => x > 0).map(x => x * 2);
  }, [data]);

  const handlePress = useCallback(() => {
    onPress(processed);
  }, [processed, onPress]);

  return <Button title={`${processed.length} items`} onPress={handlePress} />;
}
```


---

# CHAPTER 6: NETWORKING AND STORAGE


## Data Persistence

```jsx
import React, { useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

// === FETCH API ===
async function fetchUsers() {
  try {
    const response = await fetch('https://jsonplaceholder.typicode.com/users');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

async function postData(url, body) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer TOKEN',
    },
    body: JSON.stringify(body),
  });
  return response.json();
}

// === ASYNC STORAGE ===
// npm install @react-native-async-storage/async-storage

const storage = {
  async set(key, value) {
    await AsyncStorage.setItem(key, JSON.stringify(value));
  },
  async get(key) {
    const val = await AsyncStorage.getItem(key);
    return val ? JSON.parse(val) : null;
  },
  async remove(key) {
    await AsyncStorage.removeItem(key);
  },
  async clear() {
    await AsyncStorage.clear();
  },
  async keys() {
    return AsyncStorage.getAllKeys();
  },
};

// === CUSTOM HOOK FOR DATA FETCHING ===
function useAPI(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!url) return;
    setLoading(true);
    setError(null);

    fetch(url)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading, error };
}

// Usage:
// const { data, loading, error } = useAPI('https://api.example.com/items');

// === REACT QUERY (recommended) ===
// npm install @tanstack/react-query
// import { useQuery, useMutation } from '@tanstack/react-query';

// const { data, isLoading, error } = useQuery({
//   queryKey: ['users'],
//   queryFn: fetchUsers,
// });

// const mutation = useMutation({
//   mutationFn: (newUser) => postData('/users', newUser),
//   onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
// });
```


---

# CHAPTER 7: STYLING AND ANIMATIONS


## Layout and Animation

```jsx
import React, { useRef } from 'react';
import { Animated, Easing, StyleSheet, View, Button } from 'react-native';

// === FLEXBOX LAYOUT ===
const layoutStyles = StyleSheet.create({
  // Main axis (default: column)
  row: { flexDirection: 'row' },
  column: { flexDirection: 'column' },  // default
  
  // Main axis alignment
  start: { justifyContent: 'flex-start' },
  end: { justifyContent: 'flex-end' },
  center: { justifyContent: 'center' },
  between: { justifyContent: 'space-between' },
  around: { justifyContent: 'space-around' },
  evenly: { justifyContent: 'space-evenly' },
  
  // Cross axis alignment
  alignStart: { alignItems: 'flex-start' },
  alignCenter: { alignItems: 'center' },
  alignStretch: { alignItems: 'stretch' },  // default
  
  // Flex sizing
  flex1: { flex: 1 },
  flex2: { flex: 2 },
});

// === ANIMATED API ===
function FadeInView({ children }) {
  const opacity = useRef(new Animated.Value(0)).current;

  React.useEffect(() => {
    Animated.timing(opacity, {
      toValue: 1,
      duration: 500,
      useNativeDriver: true,
    }).start();
  }, []);

  return (
    <Animated.View style={{ opacity }}>
      {children}
    </Animated.View>
  );
}

function BouncingButton() {
  const scale = useRef(new Animated.Value(1)).current;

  const bounce = () => {
    Animated.sequence([
      Animated.timing(scale, { toValue: 1.2, duration: 100, useNativeDriver: true }),
      Animated.spring(scale, { toValue: 1, useNativeDriver: true }),
    ]).start();
  };

  return (
    <Animated.View style={{ transform: [{ scale }] }}>
      <Button title="Bounce!" onPress={bounce} />
    </Animated.View>
  );
}

// === REANIMATED 2 (high performance) ===
// npm install react-native-reanimated
// import Animated, { useSharedValue, useAnimatedStyle,
//   withTiming, withSpring } from 'react-native-reanimated';

// function SpringBox() {
//   const offset = useSharedValue(0);
//   const animatedStyle = useAnimatedStyle(() => ({
//     transform: [{ translateX: offset.value }],
//   }));
//   return (
//     <Animated.View style={[{ width: 80, height: 80, backgroundColor: 'blue' }, animatedStyle]}>
//       <Button title="Move" onPress={() => { offset.value = withSpring(offset.value + 50); }} />
//     </Animated.View>
//   );
// }
```


---

# CHAPTER 8: NATIVE MODULES AND DEPLOYMENT


## Platform Integration and Build

```jsx
import {
  Platform, Dimensions, PermissionsAndroid,
  NativeModules, BackHandler, AppState,
} from 'react-native';

// === PLATFORM DETECTION ===
const { OS, Version } = Platform;
const isIOS = Platform.OS === 'ios';
const isAndroid = Platform.OS === 'android';

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.select({
      ios: 44,        // iOS status bar height
      android: 24,    // Android status bar height
    }),
    ...Platform.select({
      ios: { shadowColor: '#000', shadowOpacity: 0.3 },
      android: { elevation: 4 },
    }),
  },
});

// === SCREEN DIMENSIONS ===
const { width, height } = Dimensions.get('window');
const CARD_WIDTH = width * 0.9;

// Listen for changes (orientation):
const [dimensions, setDimensions] = React.useState(Dimensions.get('window'));
React.useEffect(() => {
  const sub = Dimensions.addEventListener('change', ({ window }) => {
    setDimensions(window);
  });
  return () => sub?.remove();
}, []);

// === PERMISSIONS (Android) ===
async function requestCameraPermission() {
  try {
    const granted = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.CAMERA,
      {
        title: 'Camera Permission',
        message: 'App needs access to your camera',
        buttonNeutral: 'Ask Me Later',
        buttonNegative: 'Cancel',
        buttonPositive: 'OK',
      },
    );
    return granted === PermissionsAndroid.RESULTS.GRANTED;
  } catch (err) {
    return false;
  }
}

// === BACK HANDLER (Android) ===
React.useEffect(() => {
  const backAction = () => {
    Alert.alert('Hold on!', 'Are you sure you want to go back?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'YES', onPress: () => BackHandler.exitApp() },
    ]);
    return true;  // prevent default
  };
  const backHandler = BackHandler.addEventListener('hardwareBackPress', backAction);
  return () => backHandler.remove();
}, []);

// === APP STATE ===
const appState = React.useRef(AppState.currentState);
React.useEffect(() => {
  const sub = AppState.addEventListener('change', nextState => {
    if (appState.current.match(/inactive|background/) && nextState === 'active') {
      console.log('App came to foreground');
    }
    appState.current = nextState;
  });
  return () => sub.remove();
}, []);

// === BUILD AND DEPLOYMENT ===
// Android:
//   cd android && ./gradlew assembleRelease
//   Generate signed APK/AAB in android/app/build/outputs/

// iOS:
//   Open ios/MyApp.xcworkspace in Xcode
//   Product > Archive > Distribute App

// Expo:
//   eas build -p android   # builds APK/AAB via EAS
//   eas build -p ios       # builds IPA via EAS
//   eas submit -p android  # submit to Play Store
//   eas submit -p ios      # submit to App Store
```
