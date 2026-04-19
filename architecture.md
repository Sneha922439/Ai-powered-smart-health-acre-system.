MediQR/
│
├── App.tsx
├── package.json
├── tsconfig.json
├── app.json
│
├── src/
│   ├── navigation/
│   │   ├── RootNavigator.tsx        # Handles overall screen navigation
│   │   ├── AuthNavigator.tsx        # For onboarding/QR scanning flow
│   │   ├── MainNavigator.tsx        # After successful QR scan (main UI)
│   │
│   ├── screens/
│   │   ├── Onboarding/
│   │   │   └── InstructionsScreen.tsx
│   │   ├── QR/
│   │   │   ├── QRScannerScreen.tsx  # Scans QR → fetches user data
│   │   │   └── QRInfoScreen.tsx     # Optional: show scanned data
│   │   ├── Profile/
│   │   │   ├── ProfileScreen.tsx    # Displays profile + reports
│   │   │   ├── EditProfileScreen.tsx
│   │   ├── Reports/
│   │   │   ├── ReportsListScreen.tsx # Date-sorted reports
│   │   │   ├── ReportDetailScreen.tsx
│   │   │   └── UploadReportScreen.tsx # Camera/gallery upload
│   │
│   ├── components/
│   │   ├── QRScannerView.tsx
│   │   ├── ReportCard.tsx
│   │   ├── ProfileCard.tsx
│   │   ├── Button.tsx
│   │   └── InputField.tsx
│   │
│   ├── services/
│   │   ├── api.ts                   # Axios instance for backend calls
│   │   ├── qrService.ts             # QR parsing + validation logic
│   │   ├── profileService.ts        # Get / update profile
│   │   ├── reportService.ts         # Fetch / upload reports
│   │
│   ├── store/
│   │   ├── index.ts                 # Redux/Zustand store
│   │   ├── userSlice.ts
│   │   ├── profileSlice.ts
│   │   └── reportSlice.ts
│   │
│   ├── utils/
│   │   ├── date.ts                  # Format/sort report dates
│   │   ├── storage.ts               # Temporary cache, clears on exit
│   │   └── permissions.ts           # Camera/gallery permissions
│   │
│   ├── hooks/
│   │   ├── useProfile.ts
│   │   ├── useReports.ts
│   │   └── useAppLifecycle.ts       # Handles data clear on app close
│   │
│   ├── constants/
│   │   ├── colors.ts
│   │   ├── fonts.ts
│   │   ├── config.ts                # API base URLs, app constants
│   │
│   └── assets/
│       ├── icons/
│       ├── images/
│       └── fonts/
│
└── README.md
