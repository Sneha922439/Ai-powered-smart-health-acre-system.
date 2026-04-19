# MediQR - React Native (Expo) TypeScript Project Scaffold

This single document contains the main files for a working starter project for the mobile app architecture we discussed. Each file is presented with a header showing its path. Copy these files into your project directory `MediQR/` (or download them from the canvas viewer) and run `yarn install` / `npm install` and `expo start`.

---

```package.json
{
  "name": "mediqr",
  "version": "0.1.0",
  "private": true,
  "main": "node_modules/expo/AppEntry.js",
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web",
    "lint": "eslint --ext .ts,.tsx src"
  },
  "dependencies": {
    "expo": "~48.0.0",
    "expo-barcode-scanner": "~12.0.0",
    "expo-camera": "~13.0.0",
    "expo-secure-store": "~12.0.0",
    "expo-status-bar": "~1.4.0",
    "react": "18.2.0",
    "react-native": "0.72.0",
    "@react-navigation/native": "^6.1.6",
    "@react-navigation/stack": "^6.3.16",
    "@react-native-async-storage/async-storage": "^1.17.11",
    "axios": "^1.4.0",
    "@reduxjs/toolkit": "^1.9.5",
    "react-redux": "^8.1.2",
    "react-native-qrcode-svg": "^6.1.2"
  },
  "devDependencies": {
    "typescript": "^5.0.4",
    "@types/react": "^18.0.0",
    "@types/react-native": "^0.72.0",
    "eslint": "^8.0.0",
    "prettier": "^2.8.0"
  }
}
```

---

```ts
// App.tsx
import React from 'react';
import { Provider } from 'react-redux';
import { NavigationContainer } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { RootNavigator } from './src/navigation/RootNavigator';
import store from './src/store';

export default function App() {
  return (
    <Provider store={store}>
      <SafeAreaProvider>
        <NavigationContainer>
          <RootNavigator />
        </NavigationContainer>
        <StatusBar style="auto" />
      </SafeAreaProvider>
    </Provider>
  );
}
```

---

```ts
// src/navigation/RootNavigator.tsx
import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import AuthNavigator from './AuthNavigator';
import MainNavigator from './MainNavigator';
import { useAppSelector } from '../store/hooks';

export type RootStackParamList = {
  Auth: undefined;
  Main: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();

export const RootNavigator: React.FC = () => {
  const profile = useAppSelector(s => s.profile.profile);

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {!profile ? (
        <Stack.Screen name="Auth" component={AuthNavigator} />
      ) : (
        <Stack.Screen name="Main" component={MainNavigator} />
      )}
    </Stack.Navigator>
  );
};

export default RootNavigator;
```

---

```ts
// src/navigation/AuthNavigator.tsx
import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import InstructionsScreen from '../screens/Onboarding/InstructionsScreen';
import QRScannerScreen from '../screens/QR/QRScannerScreen';

const Stack = createStackNavigator();

const AuthNavigator = () => (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    <Stack.Screen name="Instructions" component={InstructionsScreen} />
    <Stack.Screen name="QRScanner" component={QRScannerScreen} />
  </Stack.Navigator>
);

export default AuthNavigator;
```

---

```ts
// src/navigation/MainNavigator.tsx
import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import ProfileScreen from '../screens/Profile/ProfileScreen';
import EditProfileScreen from '../screens/Profile/EditProfileScreen';
import ReportsListScreen from '../screens/Reports/ReportsListScreen';
import ReportDetailScreen from '../screens/Reports/ReportDetailScreen';
import UploadReportScreen from '../screens/Reports/UploadReportScreen';

const Stack = createStackNavigator();

const MainNavigator = () => (
  <Stack.Navigator>
    <Stack.Screen name="Profile" component={ProfileScreen} />
    <Stack.Screen name="Reports" component={ReportsListScreen} />
    <Stack.Screen name="ReportDetail" component={ReportDetailScreen} />
    <Stack.Screen name="UploadReport" component={UploadReportScreen} />
    <Stack.Screen name="EditProfile" component={EditProfileScreen} />
  </Stack.Navigator>
);

export default MainNavigator;
```

---

```tsx
// src/screens/Onboarding/InstructionsScreen.tsx
import React from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';

const InstructionsScreen: React.FC<any> = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to MediQR</Text>
      <Text style={styles.text}>
        This app keeps no local data on close. Scan your QR to fetch your profile and reports.
      </Text>
      <Button title="Scan QR" onPress={() => navigation.navigate('QRScanner')} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 22, fontWeight: '600', marginBottom: 12 },
  text: { fontSize: 16, textAlign: 'center', marginBottom: 20 },
});

export default InstructionsScreen;
```

---

```tsx
// src/screens/QR/QRScannerScreen.tsx
import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, Button, Alert } from 'react-native';
import { BarCodeScanner } from 'expo-barcode-scanner';
import { useDispatch } from 'react-redux';
import { setProfile } from '../../store/profileSlice';
import { fetchProfileFromQR } from '../../services/qrService';

const QRScannerScreen: React.FC<any> = ({ navigation }) => {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [scanned, setScanned] = useState(false);
  const dispatch = useDispatch();

  useEffect(() => {
    (async () => {
      const { status } = await BarCodeScanner.requestPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const handleBarCodeScanned = async ({ data }: { data: string }) => {
    setScanned(true);
    try {
      const payload = await fetchProfileFromQR(data);
      // payload expected: { profile, reports }
      if (payload?.profile) {
        dispatch(setProfile(payload.profile));
      }
    } catch (err) {
      Alert.alert('Invalid QR', 'Could not fetch profile from QR code.');
      setScanned(false);
    }
  };

  if (hasPermission === null) return <Text>Requesting camera permission...</Text>;
  if (hasPermission === false) return <Text>No access to camera</Text>;

  return (
    <View style={styles.container}>
      <BarCodeScanner
        onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
        style={StyleSheet.absoluteFillObject}
      />
      <View style={styles.footer}>
        <Button title={scanned ? 'Tap to Scan Again' : 'Scanning...'} onPress={() => setScanned(false)} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1 },
  footer: { position: 'absolute', bottom: 40, left: 20, right: 20 },
});

export default QRScannerScreen;
```

---

```tsx
// src/screens/Profile/ProfileScreen.tsx
import React from 'react';
import { View, Text, StyleSheet, Button, FlatList } from 'react-native';
import { useAppSelector } from '../../store/hooks';
import ReportCard from '../../components/ReportCard';

const ProfileScreen: React.FC<any> = ({ navigation }) => {
  const profile = useAppSelector(s => s.profile.profile);
  const reports = useAppSelector(s => s.reports.reports);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{profile?.name || 'Profile'}</Text>
      <Button title="Edit Profile" onPress={() => navigation.navigate('EditProfile')} />
      <Text style={styles.section}>Latest Reports</Text>
      <FlatList
        data={reports}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <ReportCard report={item} onPress={() => navigation.navigate('ReportDetail', { report: item })} />
        )}
      />
      <Button title="Upload Report" onPress={() => navigation.navigate('UploadReport')} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  title: { fontSize: 20, fontWeight: '700' },
  section: { marginTop: 12, marginBottom: 8, fontWeight: '600' },
});

export default ProfileScreen;
```

---

```tsx
// src/screens/Profile/EditProfileScreen.tsx
import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, Button } from 'react-native';
import { useAppSelector, useAppDispatch } from '../../store/hooks';
import { updateProfile } from '../../services/profileService';
import { setProfile } from '../../store/profileSlice';

const EditProfileScreen: React.FC<any> = ({ navigation }) => {
  const profile = useAppSelector(s => s.profile.profile);
  const dispatch = useAppDispatch();
  const [name, setName] = useState(profile?.name || '');

  const save = async () => {
    try {
      const updated = await updateProfile(profile.id, { name });
      dispatch(setProfile(updated));
      navigation.goBack();
    } catch (err) {
      console.warn(err);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Name</Text>
      <TextInput style={styles.input} value={name} onChangeText={setName} />
      <Button title="Save" onPress={save} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  label: { fontSize: 16, marginBottom: 8 },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 8, marginBottom: 16 },
});

export default EditProfileScreen;
```

---

```tsx
// src/screens/Reports/ReportsListScreen.tsx
import React from 'react';
import { View, FlatList, StyleSheet } from 'react-native';
import { useAppSelector } from '../../store/hooks';
import ReportCard from '../../components/ReportCard';

const ReportsListScreen: React.FC<any> = ({ navigation }) => {
  const reports = useAppSelector(s => s.reports.reports);

  return (
    <View style={styles.container}>
      <FlatList
        data={reports}
        keyExtractor={i => i.id}
        renderItem={({ item }) => (
          <ReportCard report={item} onPress={() => navigation.navigate('ReportDetail', { report: item })} />
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({ container: { flex: 1, padding: 16 } });

export default ReportsListScreen;
```

---

```tsx
// src/screens/Reports/ReportDetailScreen.tsx
import React from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';

const ReportDetailScreen: React.FC<any> = ({ route }) => {
  const { report } = route.params;
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{report.title || 'Report'}</Text>
      {report.fileUrl ? <Image source={{ uri: report.fileUrl }} style={styles.image} /> : null}
      <Text>{report.notes}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  title: { fontSize: 20, fontWeight: '700', marginBottom: 12 },
  image: { width: '100%', height: 400, marginBottom: 12 },
});

export default ReportDetailScreen;
```

---

```tsx
// src/screens/Reports/UploadReportScreen.tsx
import React, { useState } from 'react';
import { View, Button, Image, StyleSheet, Text } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { uploadReport } from '../../services/reportService';
import { useAppSelector } from '../../store/hooks';

const UploadReportScreen: React.FC<any> = ({ navigation }) => {
  const profile = useAppSelector(s => s.profile.profile);
  const [image, setImage] = useState<string | null>(null);

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ImagePicker.MediaTypeOptions.Images, quality: 0.7 });
    if (!result.canceled) setImage(result.assets[0].uri);
  };

  const takePhoto = async () => {
    const result = await ImagePicker.launchCameraAsync({ quality: 0.7 });
    if (!result.canceled) setImage(result.assets[0].uri);
  };

  const submit = async () => {
    if (!image) return;
    await uploadReport(profile.id, { uri: image, fileName: 'report.jpg' });
    navigation.goBack();
  };

  return (
    <View style={styles.container}>
      <Button title="Pick Image" onPress={pickImage} />
      <Button title="Take Photo" onPress={takePhoto} />
      {image ? <Image source={{ uri: image }} style={styles.preview} /> : <Text>No image selected</Text>}
      <Button title="Upload" onPress={submit} disabled={!image} />
    </View>
  );
};

const styles = StyleSheet.create({ container: { flex: 1, padding: 16 }, preview: { width: '100%', height: 300, marginVertical: 12 } });

export default UploadReportScreen;
```

---

```tsx
// src/components/ReportCard.tsx
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

const ReportCard: React.FC<any> = ({ report, onPress }) => (
  <TouchableOpacity style={styles.card} onPress={() => onPress(report)}>
    <Text style={styles.title}>{report.title || 'Report'}</Text>
    <Text style={styles.date}>{new Date(report.createdAt).toLocaleString()}</Text>
  </TouchableOpacity>
);

const styles = StyleSheet.create({
  card: { padding: 12, borderWidth: 1, borderColor: '#eee', borderRadius: 8, marginBottom: 8 },
  title: { fontWeight: '600' },
  date: { color: '#666', marginTop: 6 },
});

export default ReportCard;
```

---

```ts
// src/services/api.ts
import axios from 'axios';

const API_BASE = 'https://api.example.com'; // replace with your backend

const api = axios.create({ baseURL: API_BASE, timeout: 15000 });

export default api;
```

---

```ts
// src/services/qrService.ts
import api from './api';

export async function fetchProfileFromQR(token: string) {
  // token could be a UUID or signed token. Backend resolves it to profile + reports
  const res = await api.get(`/qr/${encodeURIComponent(token)}`);
  return res.data;
}
```

---

```ts
// src/services/profileService.ts
import api from './api';

export async function updateProfile(id: string, data: any) {
  const res = await api.put(`/profiles/${id}`, data);
  return res.data;
}
```

---

```ts
// src/services/reportService.ts
import api from './api';

export async function fetchReports(profileId: string) {
  const res = await api.get(`/profiles/${profileId}/reports?sort=desc`);
  return res.data;
}

export async function uploadReport(profileId: string, file: { uri: string; fileName: string }) {
  // simple example: backend returns signed URL
  const { data } = await api.post('/reports', { profileId, fileName: file.fileName });
  const { uploadUrl, report } = data;

  // upload binary to uploadUrl
  const blob = await (await fetch(file.uri)).blob();
  await fetch(uploadUrl, { method: 'PUT', body: blob });

  // confirm upload
  await api.post(`/reports/${report.id}/confirm`);
  return report;
}
```

---

```ts
// src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import profileReducer from './profileSlice';
import reportReducer from './reportSlice';

const store = configureStore({
  reducer: { profile: profileReducer, reports: reportReducer },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
```

---

```ts
// src/store/hooks.ts
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from './index';

export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

---

```ts
// src/store/profileSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

type Profile = any;

const slice = createSlice({
  name: 'profile',
  initialState: { profile: null as Profile | null },
  reducers: {
    setProfile(state, action: PayloadAction<Profile>) {
      state.profile = action.payload;
    },
    clearProfile(state) {
      state.profile = null;
    },
  },
});

export const { setProfile, clearProfile } = slice.actions;
export default slice.reducer;
```

---

```ts
// src/store/reportSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'reports',
  initialState: { reports: [] as any[] },
  reducers: {
    setReports(state, action: PayloadAction<any[]>) {
      state.reports = action.payload;
    },
    addReport(state, action: PayloadAction<any>) {
      state.reports = [action.payload, ...state.reports];
    },
    clearReports(state) {
      state.reports = [];
    },
  },
});

export const { setReports, addReport, clearReports } = slice.actions;
export default slice.reducer;
```

---

```ts
// src/utils/storage.ts
import AsyncStorage from '@react-native-async-storage/async-storage';

const TRANSIENT_PREFIX = 'transient:';

export async function setTransient(key: string, value: any) {
  await AsyncStorage.setItem(TRANSIENT_PREFIX + key, JSON.stringify(value));
}
export async function getTransient(key: string) {
  const v = await AsyncStorage.getItem(TRANSIENT_PREFIX + key);
  return v ? JSON.parse(v) : null;
}
export async function clearTransient() {
  const keys = await AsyncStorage.getAllKeys();
  const transientKeys = keys.filter(k => k.startsWith(TRANSIENT_PREFIX));
  if (transientKeys.length) await AsyncStorage.multiRemove(transientKeys);
}
```

---

```ts
// src/hooks/useAppLifecycle.ts
import { useEffect } from 'react';
import { AppState } from 'react-native';
import { clearTransient } from '../utils/storage';
import store from '../store';
import { clearProfile } from '../store/profileSlice';
import { clearReports } from '../store/reportSlice';

export default function useAppLifecycle() {
  useEffect(() => {
    const sub = AppState.addEventListener('change', state => {
      if (state === 'background' || state === 'inactive') {
        // clear transient storage and redux profile/reports
        clearTransient();
        store.dispatch(clearProfile());
        store.dispatch(clearReports());
      }
    });
    return () => sub.remove();
  }, []);
}
```

---

```ts
// src/models/types.ts
export type Profile = {
  id: string;
  name?: string;
  age?: number;
  gender?: string;
};

export type Report = {
  id: string;
  profileId: string;
  title?: string;
  notes?: string;
  fileUrl?: string;
  createdAt: string;
};
```

---

```md
# README.md

MediQR - Mobile (React Native + Expo)

## Quick start
1. Install dependencies: `yarn` or `npm install`
2. Start Expo: `expo start`
3. Use Expo Go or a simulator to run the app.

## Notes
- Replace `API_BASE` in `src/services/api.ts` with your backend.
- Backend endpoints expected:
  - `GET /qr/:token` → returns `{ profile, reports }`
  - `PUT /profiles/:id` → update profile
  - `POST /reports` → returns `{ uploadUrl, report }` for signed upload
  - `POST /reports/:id/confirm` → confirm upload

## Behavior
- The app clears all transient data when moved to background or closed. Scanning QR re-populates the in-memory profile and reports.
```

---

End of scaffold.
