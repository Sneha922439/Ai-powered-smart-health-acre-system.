
# MediQR Health Card – App Overview

## 1. Core Navigation  
The app exposes two persistent tabs at the bottom:  
- **Card** – digital identity view  
- **Profile** – medical-document hub  

---

## 2. Card Section (Digital Identity)

### 2.1 Front Side  
- Metallic-finish card  
- QR code (public identifier)  
- Patient name, DOB, blood group, emergency contact  

### 2.2 Back Side  
- Flip gesture reveals unique patient number (encrypted)  
- No other data; keeps sensitive info minimal  

---

## 3. Profile Section (Medical Hub)

### 3.1 Header  
- Hamburger icon (top-left) opens a sliding drawer:  
  - User photo (tap to open “Edit Profile” pop-up)  
  - User name  
  - Menu items:  
    1. User Information – major demographics & insurance  
    2. Doctor Information – primary consultant & contact  
    3. Patient History – chronic conditions, allergy list, special medications  

### 3.2 Report Timeline  
- Vertical, date-sorted, scrollable list of report cards  
- Only the latest dated report is visible by default (auto-filter)  
- Floating “+” button (bottom-right) triggers:  
  1. Camera/Gallery picker  
  2. Preview screen – confirm or retake  
  3. Metadata screen – add caption, date, doctor name, tags  
  4. Save – uploads, timestamps, becomes new “latest” report  

---

## 4. Interaction Flow Summary  
Card → Tap → Flip for ID number  
Profile → Hamburger → Drawer options  
Profile → Tap photo → Edit pop-up  
Profile → “+” → Capture → Preview → Metadata → Save → New latest report

> **Data Persistence Note:**  
> When the app is closed, all local data is erased.  
> On next launch the user must scan the QR code once to restore the profile and all previously uploaded reports.  
> Any new or edited details are automatically synced to the backend and will re-appear after the QR scan.

[QR Scan] → token extracted → API call → user + reports fetched → Redux store → display on ProfileScreen

When closed:
App lifecycle hook triggers → clear Redux + AsyncStorage cache


Onboarding → QR Scanner → Fetch profile & reports
     ↓
Profile Screen → Reports List → Report Detail / Upload Report
     ↓
Edit Profile
     ↓
Close App → All Data Cleared
