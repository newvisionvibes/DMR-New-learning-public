# PHASE-1 COMPLETE TESTING CHECKLIST
## ETF Relative Strength Analysis Platform - Educational Edition V7
**Status:** Live on Fly.io | **Date:** 2025-12-30 | **App URL:** `https://d-sector-etf-analyzer.fly.dev`

---

## SECTION 1: AUTHENTICATION & USER MANAGEMENT
### 1.1 Login Functionality
- [ ] **Landing Page Loads**
  - App loads without errors at `https://d-sector-etf-analyzer.fly.dev`
  - Landing page displays email/username login form
  - "Educational Edition V7" footer visible
  - Market status badge (Open/Closed) shows correctly

- [ ] **Admin Login** (Username: `admin`, Password: `Manu123!`)
  - [ ] Successfully login as admin with correct credentials
  - [ ] Redirected to admin dashboard after login
  - [ ] Session authenticated state persists during navigation
  - [ ] Sidebar shows "Admin Panel" label
  - [ ] Logout button appears in sidebar

- [ ] **Subscriber Login** (Username: `subscriber1`, Password: provided)
  - [ ] Successfully login as subscriber with correct credentials
  - [ ] Redirected to subscriber dashboard after login
  - [ ] Sidebar shows "Subscriber View" indicator
  - [ ] Access to limited tabs (no admin functions)
  - [ ] Session state matches subscriber role

- [ ] **Viewer Login** (Username: `viewer1`, Password: provided)
  - [ ] Successfully login as viewer with correct credentials
  - [ ] View-only access to dashboard (no refresh/edit buttons)
  - [ ] Sidebar shows "Viewer" label

- [ ] **Authentication Edge Cases**
  - [ ] Wrong password returns error message
  - [ ] Non-existent user returns error message
  - [ ] Inactive user (status=inactive) denied access with message
  - [ ] Empty credentials show validation error
  - [ ] Login form clears after successful authentication

### 1.2 Session Management
- [ ] **Session State Initialization**
  - [ ] `authenticated` state set to False on first load
  - [ ] After login, `authenticated` = True
  - [ ] `username` correctly stored in session
  - [ ] `user_role` correctly stored (admin/subscriber/viewer)

- [ ] **Session Persistence**
  - [ ] Session remains active across page refreshes (F5)
  - [ ] Session survives tab switching within app
  - [ ] Back button works without re-login
  - [ ] Logout clears all session state

- [ ] **Multi-Tab Session Isolation**
  - [ ] Open app in two browser tabs
  - [ ] Login in Tab 1
  - [ ] Switch to Tab 2 - should prompt re-login (or show session expired)
  - [ ] Login in Tab 2 independently

---

## SECTION 2: AUTHORIZATION & ROLE-BASED ACCESS CONTROL
### 2.1 Admin Role Permissions
- [ ] **Admin Dashboard Access**
  - [ ] "Home" tab visible and accessible
  - [ ] "Data Refresh" tab visible with analysis buttons
  - [ ] "Dashboards" tab visible with raw dataframes
  - [ ] "User Management" tab visible
  - [ ] "System Settings" tab visible

- [ ] **Admin Sidebar Controls**
  - [ ] **Angel One API Section**
    - [ ] API Key input field visible
    - [ ] Client Code input field visible
    - [ ] Password input field visible
    - [ ] TOTP input field visible
    - [ ] "Connect" button visible
    - [ ] Connection status shows (Connected/Disconnected)
  
  - [ ] **Analysis Settings Section**
    - [ ] Benchmark dropdown shows (default: Nifty 50 or selected)
    - [ ] RS Period controls visible (21, 55, 123 days)
    - [ ] Settings are interactive (can change)
    - [ ] Settings persist across refreshes
  
  - [ ] **Admin Action Buttons**
    - [ ] "Analyze All Sectors" button visible
    - [ ] "Calculate ETF RS" button visible
    - [ ] Buttons disabled if not connected to Angel One
    - [ ] Buttons enabled if API connected

- [ ] **Admin Data Refresh Capabilities**
  - [ ] Can manually trigger sector analysis
  - [ ] Can manually trigger ETF analysis
  - [ ] No rate limiting on admin refresh (or high limit like 1 refresh/min)
  - [ ] Refresh status shows timestamp when last run
  - [ ] Refresh status shows success/failure

### 2.2 Subscriber Role Permissions
- [ ] **Subscriber Dashboard Access**
  - [ ] "Home" tab visible
  - [ ] "Sector Analysis" tab visible (readonly email view)
  - [ ] "ETF Analysis" tab visible (readonly email view)
  - [ ] "Comprehensive Report" tab visible
  - [ ] "Learning Guide" tab visible

- [ ] **Subscriber Sidebar**
  - [ ] Angel One API section NOT visible
  - [ ] Analysis Settings visible but READONLY
  - [ ] Benchmark shown (e.g., "Nifty 50")
  - [ ] RS Periods shown (e.g., "21, 55, 123 days")
  - [ ] Cannot edit any settings
  - [ ] Refresh button available with 60-second cooldown

- [ ] **Subscriber Refresh Restrictions**
  - [ ] First refresh button click succeeds
  - [ ] Next 60 seconds: button becomes disabled
  - [ ] Message shows: "Next refresh allowed after HH:MM:SS IST"
  - [ ] After 60 seconds, button re-enables
  - [ ] Subsequent refreshes follow same 60-second cooldown

- [ ] **Subscriber Data Access**
  - [ ] Cannot trigger manual sector analysis
  - [ ] Cannot trigger ETF analysis
  - [ ] Cannot edit Angel One credentials
  - [ ] Cannot access User Management
  - [ ] Cannot modify system settings

### 2.3 Viewer Role Permissions
- [ ] **Viewer Dashboard Access**
  - [ ] Read-only access to all tabs
  - [ ] No edit/refresh capabilities
  - [ ] Sidebar shows minimal options
  - [ ] Cannot logout (or logout exists but view-locked)

---

## SECTION 3: SECTOR ANALYSIS & RS CALCULATION
### 3.1 Data Loading & Display
- [ ] **Sector CSV Data Loads**
  - [ ] `sector_analysis_data.csv` successfully loaded
  - [ ] Data shows 19 NIFTY sectors
  - [ ] Columns present: Sector Name, LTP, Daily Change %, RS21, RS55, RS123, TLDR, Timestamp
  - [ ] Data types correct (numeric for prices/RS, text for names/TLDR)

- [ ] **Sector Table Rendering**
  - [ ] Admin dashboard shows "Sector Analysis" raw dataframe
  - [ ] Subscriber "Sector Analysis" tab shows formatted email template
  - [ ] Table is responsive and scrollable on mobile
  - [ ] Column headers clear and readable
  - [ ] No missing or truncated data

- [ ] **Sector Metrics Accuracy**
  - [ ] Sample sector LTP matches current market (or last refresh value)
  - [ ] Daily change % calculated correctly (current LTP vs previous close)
  - [ ] RS values are numeric (0-100 range or similar)
  - [ ] TLDR messages sensible (e.g., "Gaining momentum", "Losing momentum", "Mixed")
  - [ ] Timestamps show IST timezone (e.g., "2025-12-30 16:45:00 IST")

### 3.2 RS Calculation Logic
- [ ] **RS Parameters Configuration**
  - [ ] Benchmark dropdown allows selection (Nifty 50 default)
  - [ ] RS Period 1 (21 days) editable by admin
  - [ ] RS Period 2 (55 days) editable by admin
  - [ ] RS Period 3 (123 days) editable by admin
  - [ ] Changes persist in session

- [ ] **RS Calculation Execution (Admin)**
  - [ ] Admin clicks "Analyze All Sectors" button
  - [ ] Button shows loading spinner/message
  - [ ] If Angel One connected: analysis runs without error
  - [ ] If Angel One not connected: shows informative error message
  - [ ] After completion: success message with timestamp
  - [ ] New data written to `sector_analysis_data.csv`
  - [ ] `refresh_tracker.json` updated with sectors last refresh time

- [ ] **RS Calculation Validation**
  - [ ] All 19 sectors have calculated RS values (no NaN)
  - [ ] RS values are within expected range
  - [ ] Benchmark sector (if included) shows RS ~100 (or special handling)
  - [ ] TLDR messages auto-generated based on RS trends
  - [ ] Timestamp reflects actual analysis run time

- [ ] **Top/Bottom Performers Email View**
  - [ ] Subscriber "Sector Analysis" email template shows:
    - [ ] Top 5 gaining sectors (highest RS21 or change)
    - [ ] Bottom 5 losing sectors (lowest RS21 or change)
    - [ ] Summary metrics (average daily change, avg RS)
    - [ ] Educational disclaimer footer

### 3.3 Sector Data Persistence
- [ ] **Data File Integrity**
  - [ ] `sector_analysis_data.csv` exists in appdata volume
  - [ ] File updates each time analysis runs
  - [ ] Old data not overwritten, appended with new run
  - [ ] Data persists across app restarts
  - [ ] Volume mounted correctly: `flyctl volume list` shows volume
  - [ ] File permissions allow read/write

---

## SECTION 4: ETF ANALYSIS & RS CALCULATION
### 4.1 ETF Data Loading
- [ ] **ETF List Loads**
  - [ ] `ETFs-List_updated.csv` successfully loaded
  - [ ] Shows 34-35 Indian ETFs
  - [ ] Columns: ETF Code, Name, Category, Sector, Angel One Token
  - [ ] ETF categories visible: Broad Market, Banking, Sectoral, Smart Beta, Thematic, Commodities, PSU

- [ ] **ETF RS Output Loads**
  - [ ] `etf_rs_output.csv` successfully loaded
  - [ ] Shows RS metrics for 34 ETFs (matches source list, no extra/missing)
  - [ ] Columns: ETF Code, Name, LTP, Daily Change %, RS21, RS55, RS123, TLDR, Timestamp
  - [ ] Data consistent across multiple page loads

- [ ] **ETF Table Display (Admin)**
  - [ ] Admin "Dashboards" > ETF tab shows raw dataframe
  - [ ] All 34 ETFs listed without duplicates or blanks
  - [ ] Sortable by column (if implemented)
  - [ ] Responsive layout on desktop and mobile

- [ ] **ETF Email View (Subscriber)**
  - [ ] Subscriber "ETF Analysis" tab shows formatted email template
  - [ ] Top 5 ETFs by RS (strongest momentum)
  - [ ] Bottom 5 ETFs by RS (weakest momentum)
  - [ ] Summary statistics (average LTP change, avg RS)
  - [ ] Professional HTML formatting
  - [ ] Educational disclaimer

### 4.2 ETF Calculation Execution
- [ ] **Trigger ETF Analysis (Admin)**
  - [ ] "Calculate ETF RS" button visible in sidebar
  - [ ] Button disabled if Angel One not connected
  - [ ] On click: analysis runs with loading indicator
  - [ ] Completion shows success message with timestamp
  - [ ] New data written to `etf_rs_output.csv`
  - [ ] `refresh_tracker.json` updated with etfs last refresh time

- [ ] **ETF RS Calculation Validation**
  - [ ] All 34 ETFs have RS21, RS55, RS123 values
  - [ ] No missing/NaN values in critical columns
  - [ ] RS values within expected numerical range
  - [ ] TLDR insights generated (e.g., "Strong momentum", "Avoid", "Mixed")
  - [ ] LTP and daily change reflect market data (or last cached)
  - [ ] Timestamp shows IST timezone

- [ ] **ETF Count Consistency**
  - [ ] Refresh "ETF Analysis" tab 5 consecutive times
  - [ ] ETF count remains 34 each time (validateetfdata function working)
  - [ ] No random fluctuations in count
  - [ ] Data values stable across refreshes
  - [ ] No AttributeError on refresh button click

### 4.3 ETF Categorization
- [ ] **ETF Categories Display**
  - [ ] ETFs grouped by category in email template (if implemented)
  - [ ] Broad Market: Nifty 50, Sensex 50, etc. shown
  - [ ] Banking sector ETFs grouped together
  - [ ] Commodities (Gold, Silver) clearly labeled
  - [ ] Each category has description/context

---

## SECTION 5: DATA REFRESH MECHANISM & TIMING
### 5.1 Refresh Tracker Functionality
- [ ] **Refresh Tracker JSON**
  - [ ] `refresh_tracker.json` exists in appdata
  - [ ] Contains last refresh timestamps for sectors and ETFs
  - [ ] Tracks refresh status (success/failure)
  - [ ] Records count of records processed
  - [ ] Updates automatically after each admin analysis run

- [ ] **Last Refresh Display**
  - [ ] Admin dashboard shows "Last refreshed: 2025-12-30 16:45:00 IST"
  - [ ] Subscriber views show same timestamp
  - [ ] Timestamp format consistent across all tabs
  - [ ] Timezone always shows IST (Asia/Kolkata)
  - [ ] "Fresh" or "Outdated" label appears if data is stale

### 5.2 IST Timezone Handling
- [ ] **Timestamp Accuracy**
  - [ ] All timestamps display in IST (Asia/Kolkata)
  - [ ] No UTC or system-local timezone shown
  - [ ] pytz.timezone('Asia/Kolkata') correctly applied
  - [ ] Daylight saving transitions handled (India uses IST year-round)

- [ ] **Market Hours Check**
  - [ ] Market status badge shows "Open" during 09:15-15:30 IST (Mon-Fri)
  - [ ] Market status shows "Closed" outside trading hours
  - [ ] Market status shows "Closed" on weekends (Sat-Sun)
  - [ ] Auto-refresh respects market hours (admin feature, if enabled)

### 5.3 Subscriber Refresh Cooldown
- [ ] **60-Second Cooldown Enforcement**
  - [ ] Subscriber clicks refresh button at 10:00:00
  - [ ] Data refreshes successfully
  - [ ] Refresh button immediately becomes disabled
  - [ ] Message shows: "Next refresh allowed after 10:01:00 IST"
  - [ ] Counter updates every second (if animation implemented)
  - [ ] At 10:01:00, button re-enables automatically

- [ ] **Cooldown Edge Cases**
  - [ ] Multiple refresh clicks blocked during cooldown
  - [ ] Cooldown timer resets correctly on each successful refresh
  - [ ] Cooldown persists across page refreshes (F5)
  - [ ] Cooldown timer survives tab switches
  - [ ] Logout/re-login resets cooldown timer

- [ ] **Human-Readable Timestamp**
  - [ ] Next allowed time shown as "HH:MM:SS IST"
  - [ ] Format consistent across all subscriber tabs
  - [ ] Example: "Next refresh allowed after 16:45:30 IST" ✓

---

## SECTION 6: ANGEL ONE API INTEGRATION
### 6.1 API Connection
- [ ] **Connection Setup (Admin)**
  - [ ] Sidebar shows "Connect to Angel One API" section
  - [ ] API Key input accepts text (max length reasonable)
  - [ ] Client Code input accepts alphanumeric
  - [ ] Password input accepts text (masked)
  - [ ] TOTP input accepts 6-digit code
  - [ ] "Connect" button attempts connection on click

- [ ] **Successful Connection**
  - [ ] Valid credentials → "Connected ✓" status shown
  - [ ] Session stores `admin_connector` object
  - [ ] "Analyze All Sectors" button enabled
  - [ ] "Calculate ETF RS" button enabled
  - [ ] Sidebar shows API is active/ready

- [ ] **Failed Connection**
  - [ ] Invalid API key → "Failed: Invalid credentials" message
  - [ ] Invalid TOTP → "Failed: TOTP expired or incorrect"
  - [ ] Network error → "Failed: Connection timeout"
  - [ ] Status shows "Disconnected" with error icon
  - [ ] Analysis buttons remain disabled

- [ ] **Connection Status Persistence**
  - [ ] After successful connect, status persists during session
  - [ ] Logout clears connection
  - [ ] Re-login as admin shows "Disconnected" again
  - [ ] Credentials not stored in session (security)

### 6.2 API Rate Limiting Safety
- [ ] **Safe API Usage Pattern**
  - [ ] Admin triggers sector analysis → single background fetch
  - [ ] No per-user API calls (shared data for all subscribers)
  - [ ] ETF calculation uses sequential fetch (0.2-0.3s delay between calls)
  - [ ] 34 ETFs should complete in ~10-15 seconds
  - [ ] No parallel/burst API requests

- [ ] **Refresh Frequency**
  - [ ] Admin can manually refresh sectors/ETFs without artificial delays
  - [ ] Auto-refresh (if implemented) respects market hours
  - [ ] Refresh frequency during market hours: 1-5 minute minimum interval
  - [ ] No forced refresh loops (only manual trigger or scheduled)

- [ ] **API Error Handling**
  - [ ] API timeout (>5s) shows error message, not silent failure
  - [ ] Temporary API error (rate limit) shows retry message
  - [ ] Persistent API errors trigger warning email to admin (future)
  - [ ] Failsafe mode: app continues showing cached data if API down

### 6.3 Token & Auth Management
- [ ] **Token Refresh Logic**
  - [ ] Angel One session token refreshed when expired
  - [ ] Token refresh automatic, transparent to user
  - [ ] No re-entry of credentials on token expiry
  - [ ] Failed token refresh shows connection error

- [ ] **Credential Security**
  - [ ] Passwords/API keys not logged to console
  - [ ] Credentials not displayed in error messages
  - [ ] Fly.io secrets used for production credentials
  - [ ] .env file not committed to git

---

## SECTION 7: DATA VALIDATION & ERROR HANDLING
### 7.1 Data Validation Function
- [ ] **ETF Data Validation (validateetfdata)**
  - [ ] Function checks ETF DataFrame for:
    - [ ] No duplicate rows
    - [ ] All columns present (LTP, Daily Change, RS21, RS55, RS123, TLDR, Timestamp)
    - [ ] Numeric columns are numeric (not strings)
    - [ ] RS values in valid range (0-100 or custom range)
    - [ ] LTP values > 0
    - [ ] Timestamps are valid datetime

- [ ] **Validation Logging**
  - [ ] `flyctl logs -f` shows "Validating ETF data..." messages
  - [ ] Validation results logged: "Validation passed: 34 ETFs" or errors listed
  - [ ] Type conversion logged: "Converting RS columns to numeric..."
  - [ ] Missing data reported: "Row X: missing LTP value"

- [ ] **Validation Actions on Failure**
  - [ ] Invalid data does NOT crash app
  - [ ] Error message shown to user: "Data validation failed, showing last known data"
  - [ ] Admin notified via log warning
  - [ ] Subscriber sees stale data with warning timestamp

### 7.2 Type Conversion Handling
- [ ] **Pandas Type Conversion**
  - [ ] RS21, RS55, RS123 columns explicitly converted to numeric
  - [ ] Daily Change % converted to float
  - [ ] LTP converted to float
  - [ ] LTP strings with "₹" symbol handled (if present)
  - [ ] Non-numeric values replaced with NaN, then reported

- [ ] **String/Text Handling**
  - [ ] ETF names/codes properly handled as strings
  - [ ] Sector names correctly stored as text
  - [ ] TLDR messages preserve original text
  - [ ] No unwanted whitespace trimming

### 7.3 Comprehensive Error Messages
- [ ] **User-Visible Errors**
  - [ ] Error messages clear and actionable
  - [ ] Technical jargon minimized
  - [ ] Suggested remediation provided (if applicable)
  - [ ] Example: "Angel One API currently unavailable. Please try again in 5 minutes."

- [ ] **Admin Logs (flyctl logs -f)**
  - [ ] Full error traceback visible in logs
  - [ ] Line numbers and file names included
  - [ ] Error context provided (which function, parameters)
  - [ ] No passwords/API keys in error logs

---

## SECTION 8: EMAIL BUILDER & REPORT TEMPLATES
### 8.1 Sector Email Template
- [ ] **Sector Newsletter HTML Structure**
  - [ ] Professional email-like layout
  - [ ] Header with app title "ETF Market Analysis"
  - [ ] Date/time of report generation
  - [ ] "Sector Analysis Report" section title

- [ ] **Sector Content**
  - [ ] Top 5 gaining sectors table:
    - [ ] Sector name, LTP, Daily Change %, RS21 value
    - [ ] Rows ordered by RS21 descending
    - [ ] Green highlighting for gainers
  
  - [ ] Bottom 5 losing sectors table:
    - [ ] Sector name, LTP, Daily Change %, RS21 value
    - [ ] Rows ordered by RS21 ascending
    - [ ] Red highlighting for losers
  
  - [ ] Summary metrics:
    - [ ] Average daily change %
    - [ ] Average RS21
    - [ ] Strongest sector name
    - [ ] Weakest sector name

- [ ] **Email Footer**
  - [ ] Educational disclaimer present
  - [ ] "This is analysis, not investment advice"
  - [ ] SEBI compliance note
  - [ ] Link to Terms & Conditions
  - [ ] Unsubscribe link (if email feature)
  - [ ] Last updated timestamp

- [ ] **Email Rendering (Subscriber View)**
  - [ ] Embedded in Streamlit using `st.components.v1.html()`
  - [ ] Responsive design (works on mobile)
  - [ ] Tables readable and aligned
  - [ ] Colors display correctly
  - [ ] Scrollable if content tall (height=2000px typical)

### 8.2 ETF Email Template
- [ ] **ETF Newsletter HTML Structure**
  - [ ] Similar professional layout to sector template
  - [ ] "ETF Analysis Report" section title
  - [ ] Date/time of report

- [ ] **ETF Content**
  - [ ] Top 5 ETFs by RS:
    - [ ] ETF name, category, LTP, Daily Change %, RS21
    - [ ] Sorted by RS21 descending
    - [ ] Green color indicator
  
  - [ ] Bottom 5 ETFs by RS:
    - [ ] ETF name, category, LTP, Daily Change %, RS21
    - [ ] Sorted by RS21 ascending
    - [ ] Red color indicator
  
  - [ ] Category breakdown (if implemented):
    - [ ] Broad Market ETFs section
    - [ ] Banking sector ETFs section
    - [ ] Commodities ETFs section
    - [ ] Each with top/bottom performers
  
  - [ ] Summary metrics:
    - [ ] Average daily change across all ETFs
    - [ ] Average RS values
    - [ ] Total ETF count tracked (34)

- [ ] **Email Footer**
  - [ ] Educational disclaimer
  - [ ] Risk disclosure statement
  - [ ] Contact/feedback link
  - [ ] Timestamp in IST

### 8.3 Comprehensive Email Template
- [ ] **Combined Report Structure**
  - [ ] Merged sector + ETF analysis
  - [ ] Single comprehensive report view
  - [ ] Sectors section first, then ETFs section
  - [ ] Summary metrics for both asset classes

- [ ] **Comprehensive View Requirements**
  - [ ] Requires both `sector_analysis_data.csv` and `etf_rs_output.csv` to be loaded
  - [ ] Shows warning if either file missing
  - [ ] Responsive HTML rendering
  - [ ] Professional formatting

---

## SECTION 9: STREAMLIT-SPECIFIC FIXES
### 9.1 Streamlit Version & Compatibility
- [ ] **Streamlit Version Check**
  - [ ] `pip list | grep streamlit` shows 1.27.0 or higher
  - [ ] No deprecated method errors in logs
  - [ ] App runs without AttributeError

- [ ] **st.rerun() Function**
  - [ ] Replaced `st.experimental_rerun()` with `st.rerun()`
  - [ ] Subscriber refresh button triggers rerun without error
  - [ ] After rerun, new data loads correctly
  - [ ] No "AttributeError: module 'streamlit' has no attribute 'experimental_rerun'" in logs

- [ ] **Session State Management**
  - [ ] st.session_state properly initialized at app start
  - [ ] Session keys don't cause KeyError
  - [ ] Session values persist across reruns
  - [ ] Session cleared on logout

### 9.2 Data Consistency Across Refreshes
- [ ] **Rerun Stability**
  - [ ] Refresh button works 10 times consecutively
  - [ ] No crashes or errors after any rerun
  - [ ] No memory leaks (CPU/memory stable over 10 refreshes)
  - [ ] UI remains responsive after rerun

- [ ] **Data Consistency**
  - [ ] ETF count = 34 on every refresh (not 17, 51, etc.)
  - [ ] Sector count = 19 consistently
  - [ ] Data values match previous refresh (no random changes)
  - [ ] Timestamps match when data not actually refreshed

- [ ] **validateetfdata Function**
  - [ ] Function called before data display (check logs)
  - [ ] ETF CSV checked for:
    - [ ] No blank rows at end
    - [ ] All rows have complete data
    - [ ] Type conversion successful (RS columns numeric)
    - [ ] Count matches expected (34 ETFs)
  - [ ] Validation messages appear in `flyctl logs -f`

---

## SECTION 10: SIDEBAR & NAVIGATION
### 10.1 Sidebar Structure (Admin)
- [ ] **Overall Sidebar Layout**
  - [ ] Sidebar appears on left (Streamlit default)
  - [ ] Logo/app title at top
  - [ ] Username display ("Logged in as: admin")
  - [ ] Role indicator ("Admin Panel")
  - [ ] Logout button at bottom

- [ ] **Angel One Connection Section**
  - [ ] Expandable/collapsible section
  - [ ] API Key, Client Code, Password, TOTP inputs
  - [ ] Connect button
  - [ ] Connection status indicator
  - [ ] Clear layout, no overlapping text

- [ ] **Analysis Settings Section**
  - [ ] Benchmark dropdown
  - [ ] RS Period 1/2/3 number inputs or sliders
  - [ ] Settings clearly labeled
  - [ ] Current values visible
  - [ ] Changes apply immediately

- [ ] **Admin Action Buttons**
  - [ ] "Analyze All Sectors" button
  - [ ] "Calculate ETF RS" button
  - [ ] Buttons gray/disabled if API not connected
  - [ ] Buttons blue/active if API connected
  - [ ] Loading spinner during analysis

- [ ] **Additional Admin Options**
  - [ ] Auto-refresh toggle (if implemented)
  - [ ] Audit trail toggle (if implemented)
  - [ ] Admin message/announcement area

### 10.2 Sidebar Structure (Subscriber)
- [ ] **Simplified Sidebar**
  - [ ] Username display
  - [ ] "Subscriber View" indicator
  - [ ] Analysis Settings READONLY section
  - [ ] Benchmark shown (not editable)
  - [ ] RS Periods shown (not editable)
  - [ ] Refresh button with cooldown info
  - [ ] Logout button

- [ ] **No Admin Elements**
  - [ ] No Angel One API inputs visible
  - [ ] No "Analyze All Sectors" button
  - [ ] No user management access
  - [ ] No system settings access

### 10.3 Main Content Navigation
- [ ] **Tab/Page Navigation**
  - [ ] Navigation clear and logical
  - [ ] Current tab/page highlighted
  - [ ] Smooth transitions between tabs
  - [ ] No broken links or missing pages

- [ ] **Admin Tabs**
  - [ ] Home tab accessible
  - [ ] Data Refresh tab accessible
  - [ ] Dashboards tab accessible
  - [ ] User Management tab accessible
  - [ ] System Settings tab accessible
  - [ ] Each tab loads without error

- [ ] **Subscriber Tabs**
  - [ ] Home tab accessible
  - [ ] Sector Analysis tab accessible
  - [ ] ETF Analysis tab accessible
  - [ ] Comprehensive Report tab accessible
  - [ ] Learning Guide tab accessible
  - [ ] Each tab loads without error

---

## SECTION 11: HOME & OVERVIEW PAGES
### 11.1 Home Tab Content (Admin)
- [ ] **Admin Home Page**
  - [ ] Welcome message for admin
  - [ ] Quick snapshot metrics:
    - [ ] "Sectors Tracked: 19"
    - [ ] "ETFs Analyzed: 34"
    - [ ] "Last Sector Analysis: 2025-12-30 16:45:00 IST"
    - [ ] "Last ETF Analysis: 2025-12-30 16:50:00 IST"
    - [ ] "API Status: Connected/Disconnected"
    - [ ] "Market Status: Open/Closed"

- [ ] **Navigation Guides**
  - [ ] Links to other admin sections
  - [ ] Quick action buttons (Connect API, Run Analysis)
  - [ ] Recent activity log (last 5 actions, if implemented)

- [ ] **Status Indicators**
  - [ ] Green checkmark for successful analyses
  - [ ] Red X for failed operations
  - [ ] Yellow warning for stale data
  - [ ] Blue info for neutral status

### 11.2 Home Tab Content (Subscriber)
- [ ] **Subscriber Home Page**
  - [ ] Welcome message personalized with username
  - [ ] "Your subscription is active" indicator
  - [ ] Next refresh allowed time (if in cooldown)
  - [ ] Quick access to reports
    - [ ] "View Sector Analysis" button
    - [ ] "View ETF Analysis" button
    - [ ] "View Full Report" button

- [ ] **Market Overview**
  - [ ] Current date/time in IST
  - [ ] Market status (Open/Closed/Pre-open)
  - [ ] Last data refresh timestamp
  - [ ] Freshness indicator (Fresh/1hr old/1day old/etc.)

- [ ] **Educational Content Preview**
  - [ ] Link to Learning Guide
  - [ ] One-line tip about ETF investing (rotated daily, if implemented)
  - [ ] Disclaimer reminder

---

## SECTION 12: DISCLAIMERS & LEGAL COMPLIANCE
### 12.1 Educational Edition Label
- [ ] **Visible Branding**
  - [ ] "Educational Edition V7" shown in footer
  - [ ] "Educational Edition" shown in page title
  - [ ] Visible on every page/tab
  - [ ] Not obscured or hidden

- [ ] **Educational Disclaimer**
  - [ ] "This platform provides market analysis and educational information only"
  - [ ] "Not investment advice"
  - [ ] "Users responsible for their own trading decisions"
  - [ ] Shown in footer and in reports

- [ ] **SEBI Compliance**
  - [ ] "Not SEBI registered investment advisor"
  - [ ] "No guarantee of returns"
  - [ ] "Past performance ≠ future results"
  - [ ] Disclaimer visible to subscribers

### 12.2 Email Report Disclaimers
- [ ] **Sector Email Footer**
  - [ ] Educational disclaimer present
  - [ ] Risk disclosure included
  - [ ] SEBI note included
  - [ ] Unsubscribe/manage preferences link (if email feature)

- [ ] **ETF Email Footer**
  - [ ] Same disclaimers as sector
  - [ ] Professionally formatted
  - [ ] Small but readable font

- [ ] **Comprehensive Report Footer**
  - [ ] Combined disclaimers
  - [ ] Links to full Terms & Conditions
  - [ ] Privacy policy reference

### 12.3 Risk Disclosure
- [ ] **Risk Statement Present**
  - [ ] "Investments in ETFs subject to market risks"
  - [ ] "Markets can change rapidly"
  - [ ] "Losses may occur"
  - [ ] "Consult financial advisor before investing"

---

## SECTION 13: SYSTEM SETTINGS & CONFIGURATION
### 13.1 Admin System Settings Tab
- [ ] **Configuration Display**
  - [ ] App version: "V7.0 Educational Edition"
  - [ ] Deployment info: "Fly.io"
  - [ ] Database type: "Postgres"
  - [ ] Auth type: "Postgres-backed"
  - [ ] API: "Angel One SmartAPI"

- [ ] **Data Refresh Information**
  - [ ] Last sector analysis date/time
  - [ ] Last ETF analysis date/time
  - [ ] Refresh frequency info (if scheduled refresh used)
  - [ ] Next scheduled refresh (if applicable)

- [ ] **User Statistics**
  - [ ] Total active users count
  - [ ] Admin count
  - [ ] Subscriber count
  - [ ] Viewer count
  - [ ] Inactive users count

- [ ] **System Health**
  - [ ] App uptime
  - [ ] Last error (if any)
  - [ ] Postgres connection status
  - [ ] Volume mount status
  - [ ] Available disk space

### 13.2 Feature Toggles (Admin)
- [ ] **Configurable Options**
  - [ ] Auto-refresh toggle (On/Off)
  - [ ] Auto-refresh interval (if enabled)
  - [ ] Email distribution toggle (if email feature)
  - [ ] Audit trail toggle
  - [ ] Debug logging toggle

- [ ] **Settings Persistence**
  - [ ] Settings saved across app restarts
  - [ ] Settings stored in database or config file
  - [ ] Settings editable by admin
  - [ ] Settings immediately effective

---

## SECTION 14: USER MANAGEMENT (ADMIN)
### 14.1 User List View
- [ ] **User Table Display**
  - [ ] Shows all users (admin, subscribers, viewers)
  - [ ] Columns: Username, Email, Role, Status, Created Date, Last Login
  - [ ] Sortable by column (if implemented)
  - [ ] Filterable by role (if implemented)
  - [ ] Pagination if many users (if implemented)

- [ ] **User Status Indicators**
  - [ ] Active users marked "Active" (green)
  - [ ] Inactive users marked "Inactive" (gray)
  - [ ] Recently active users marked with timestamp
  - [ ] Never logged in marked "Never logged in"

### 14.2 User Operations
- [ ] **View User Details**
  - [ ] Click on user row shows detailed view
  - [ ] Displays: username, email, role, status, dates, password hash
  - [ ] No sensitive password displayed

- [ ] **Create New User**
  - [ ] Admin can create new user (future enhancement)
  - [ ] Form fields: username, email, password, role (admin/subscriber/viewer)
  - [ ] Password validation (min 8 chars, complexity rules)
  - [ ] User added to `users_database.json`
  - [ ] Confirmation message shown

- [ ] **Edit User**
  - [ ] Admin can edit username, email, role, status
  - [ ] Cannot change password via edit (admin change password feature)
  - [ ] Changes persist in database
  - [ ] Audit log records the edit (if audit enabled)

- [ ] **Deactivate/Reactivate User**
  - [ ] Admin can set user status to "inactive"
  - [ ] Inactive users cannot login
  - [ ] Admin can reactivate user (status → "active")
  - [ ] User receives no notification of deactivation

- [ ] **Reset Password (Admin)**
  - [ ] Admin can trigger password reset for user
  - [ ] Temporary password generated (or reset link sent)
  - [ ] User prompted to change on next login (if email feature)

### 14.3 User Database Integrity
- [ ] **users_database.json File**
  - [ ] File exists in appdata volume
  - [ ] Contains JSON array of users
  - [ ] Each user object has: username, password, email, role, status, created_date
  - [ ] File updates when users added/edited
  - [ ] File persists across app restarts

- [ ] **Backup & Recovery**
  - [ ] users_database.json backed up (manual or automatic)
  - [ ] Recovery procedure documented
  - [ ] Admin can restore user list if needed

---

## SECTION 15: LOGGING & MONITORING
### 15.1 Application Logs (flyctl logs -f)
- [ ] **Log Output Monitoring**
  - [ ] Run `flyctl logs -f` in terminal
  - [ ] Live log stream visible
  - [ ] Logs show request/response activity
  - [ ] Error logs clearly marked with ERROR/WARN tags
  - [ ] Timestamp on every log line (IST)

- [ ] **Key Events Logged**
  - [ ] User login attempts (success/failure)
  - [ ] User logout events
  - [ ] Sector analysis start/completion
  - [ ] ETF analysis start/completion
  - [ ] API connection success/failure
  - [ ] Data validation results
  - [ ] File I/O operations (read/write CSV, JSON)
  - [ ] Errors and exceptions with full traceback

- [ ] **No Sensitive Data in Logs**
  - [ ] API keys not logged
  - [ ] Passwords not logged
  - [ ] Personal user data not logged
  - [ ] TOTP codes not logged

### 15.2 Fly.io Dashboard Monitoring
- [ ] **App Status Check**
  - [ ] Visit `https://fly.io` dashboard
  - [ ] Navigate to app "d-sector-etf-analyzer"
  - [ ] Status shows "Running" (green)
  - [ ] No crash/restart indicators

- [ ] **Metrics Monitoring**
  - [ ] `flyctl metrics` shows CPU usage (should be low, <50% typical)
  - [ ] Memory usage reasonable (<500MB typical)
  - [ ] Network requests/responses tracking
  - [ ] No signs of memory leak (CPU/memory stable over hours)

- [ ] **Volume Status**
  - [ ] `flyctl volume list` shows volume "data" mounted
  - [ ] Volume size: 1 GB (per deployment)
  - [ ] Volume accessible and writable

---

## SECTION 16: PERFORMANCE & LOAD TESTING
### 16.1 Response Time Benchmarks
- [ ] **Page Load Times**
  - [ ] Landing page loads in <2 seconds
  - [ ] Admin dashboard loads in <3 seconds
  - [ ] Subscriber dashboard loads in <3 seconds
  - [ ] Data Refresh page loads in <2 seconds
  - [ ] Home tab loads in <1 second

- [ ] **Action Response Times**
  - [ ] Login submission completes in <2 seconds
  - [ ] Logout completes in <1 second
  - [ ] Refresh button click processes in <3 seconds
  - [ ] Sidebar settings change applies immediately

- [ ] **Analysis Execution Times**
  - [ ] Sector analysis completes in <30 seconds (with Angel One API)
  - [ ] ETF analysis completes in <20 seconds (34 ETFs sequentially)
  - [ ] Data loading from CSV completes in <1 second
  - [ ] Email template generation completes in <2 seconds

### 16.2 Concurrent User Simulation (if load testing available)
- [ ] **Multiple Concurrent Readers**
  - [ ] 5 subscribers viewing data simultaneously (no crashes)
  - [ ] 2 subscribers refreshing with cooldown (no race condition)
  - [ ] 1 admin running analysis while subscribers viewing (stable)
  - [ ] No data corruption or lost updates

- [ ] **Database Load**
  - [ ] Postgres connection pool adequate (default 5 connections)
  - [ ] No "connection pool exhausted" errors
  - [ ] Concurrent reads don't block each other
  - [ ] Concurrent writes don't cause conflicts

### 16.3 Error Recovery Under Load
- [ ] **Graceful Degradation**
  - [ ] API timeout doesn't crash app (shows error message)
  - [ ] Database connection lost shows user message, not error page
  - [ ] File system full handled gracefully
  - [ ] Memory pressure causes appropriate action (or alert)

- [ ] **Self-Healing**
  - [ ] Brief API interruption auto-recovers
  - [ ] Brief database disconnection auto-recovers
  - [ ] No manual restart needed for transient errors
  - [ ] Health checks trigger restart if truly broken

---

## SECTION 17: SECURITY & DATA PROTECTION
### 17.1 Authentication Security
- [ ] **Password Storage**
  - [ ] Passwords hashed (not stored as plaintext, if using users.json)
  - [ ] Salt used in hashing (if applicable)
  - [ ] Hash function strong (bcrypt, Argon2, or similar)
  - [ ] Current version uses plaintext for educational purpose (noted as limitation)

- [ ] **Session Security**
  - [ ] Session token generated on login
  - [ ] Session expires after inactivity (if configured)
  - [ ] Session cannot be hijacked (no token in URL)
  - [ ] Logout destroys session immediately

- [ ] **HTTPS Encryption**
  - [ ] All traffic encrypted (Fly.io auto HTTPS)
  - [ ] URL shows "https://d-sector-etf-analyzer.fly.dev" with lock icon
  - [ ] Certificate valid and not expired
  - [ ] No mixed content warnings

### 17.2 Data Privacy
- [ ] **User Data Protection**
  - [ ] User email stored securely
  - [ ] User credentials not shared or logged
  - [ ] User activity not sold or exposed
  - [ ] Privacy policy available (if implemented)

- [ ] **API Key Protection**
  - [ ] Angel One API keys stored in Fly.io secrets (not in code)
  - [ ] API keys not visible in error messages
  - [ ] API keys not logged
  - [ ] API keys rotatable without redeployment (if implemented)

- [ ] **Data File Permissions**
  - [ ] CSV files readable only by app process
  - [ ] JSON files (users, refresh tracker) readable/writable only by app
  - [ ] No direct file access from web (files not in /public directory)

### 17.3 Input Validation & XSS Prevention
- [ ] **Login Form Validation**
  - [ ] Username/password fields validated for special characters
  - [ ] No HTML/JavaScript injection via login fields
  - [ ] Error messages don't echo user input
  - [ ] Form submitted securely (POST, not GET)

- [ ] **Admin Form Validation**
  - [ ] Benchmark dropdown shows predefined values only
  - [ ] RS Period inputs accept only numbers
  - [ ] API Key input doesn't allow code execution
  - [ ] TOTP input accepts only digits

- [ ] **Email Template XSS Prevention**
  - [ ] ETF names in email templates escaped properly
  - [ ] Sector names in email templates escaped
  - [ ] TLDR messages don't contain unescaped HTML
  - [ ] No inline JavaScript in email templates

---

## SECTION 18: MOBILE RESPONSIVENESS
### 18.1 Mobile Layout
- [ ] **Mobile Viewport**
  - [ ] App works on mobile browser (iPhone/Android)
  - [ ] Sidebar collapses/hidden on mobile
  - [ ] Main content uses full width on mobile
  - [ ] Touch-friendly button sizes (>44px)

- [ ] **Mobile Navigation**
  - [ ] Tabs accessible on mobile (scroll horizontal if many)
  - [ ] Sidebar toggle (hamburger menu) if implemented
  - [ ] Back button functions on mobile
  - [ ] No horizontal scroll for content

- [ ] **Mobile Data Rendering**
  - [ ] Tables responsive (stacked columns or scroll on mobile)
  - [ ] Charts responsive (resize to mobile width)
  - [ ] Email templates readable on mobile
  - [ ] Font sizes legible on mobile (>12px typical)

### 18.2 Mobile Functionality
- [ ] **Touch Interactions**
  - [ ] Buttons clickable with touch (not just hover)
  - [ ] Refresh button works with touch
  - [ ] Dropdowns open/close with touch
  - [ ] Scrolling smooth and responsive

- [ ] **Mobile Performance**
  - [ ] App loads quickly on mobile (bandwidth-limited)
  - [ ] No excessive data downloads
  - [ ] Images optimized or lazy-loaded
  - [ ] No full-page reloads on navigation

---

## SECTION 19: BROWSER COMPATIBILITY
### 19.1 Chrome/Chromium
- [ ] **Chrome Desktop**
  - [ ] App loads and functions correctly
  - [ ] All interactive elements work
  - [ ] No console errors (check DevTools)
  - [ ] Performance acceptable

- [ ] **Chrome Mobile**
  - [ ] App responsive and usable
  - [ ] Touch interactions work
  - [ ] Mobile layout correct

### 19.2 Firefox
- [ ] **Firefox Desktop**
  - [ ] App loads and functions
  - [ ] No Firefox-specific issues
  - [ ] Console clean (check DevTools)

### 19.3 Safari
- [ ] **Safari Desktop**
  - [ ] App loads and functions
  - [ ] CSS renders correctly
  - [ ] No Safari-specific quirks

- [ ] **Safari Mobile (iOS)**
  - [ ] App works on iPhone/iPad
  - [ ] Mobile layout responsive
  - [ ] Touch interactions smooth

### 19.4 Edge
- [ ] **Microsoft Edge**
  - [ ] App loads and functions
  - [ ] No Edge-specific issues

---

## SECTION 20: END-TO-END USER WORKFLOWS
### 20.1 Complete Admin Workflow
```
1. Navigate to app URL
2. See landing page
3. Enter admin credentials
4. Click Login
5. Sidebar shows "Admin Panel"
6. Sidebar shows "Angel One API" section
7. Enter Angel One credentials
8. Click "Connect"
9. See "Connected ✓" status
10. Click "Analyze All Sectors"
11. Wait for completion message
12. Click "Data Refresh" tab
13. See updated timestamp for sectors
14. Click "Dashboards" tab
15. See raw sector data (19 rows)
16. Click "Calculate ETF RS" button
17. Wait for completion
18. See raw ETF data (34 rows)
19. Verify data integrity (no NaNs, consistent counts)
20. Logout
```
✓ All steps completed without error

### 20.2 Complete Subscriber Workflow
```
1. Navigate to app URL
2. See landing page
3. Enter subscriber credentials
4. Click Login
5. See "Subscriber View" indication
6. Sidebar shows Analysis Settings (readonly)
7. Home tab shows welcome message
8. Click "Sector Analysis" tab
9. See formatted email template
10. See top 5 and bottom 5 sectors
11. Click "Refresh" button
12. Data loads
13. Refresh button becomes disabled
14. Message shows "Next refresh allowed after HH:MM:SS"
15. Wait 60+ seconds
16. Refresh button re-enables
17. Click "ETF Analysis" tab
18. See formatted email template
19. See top 5 and bottom 5 ETFs
20. Click "Comprehensive Report" tab
21. See combined sector + ETF report
22. Click "Learning Guide" tab
23. See educational content
24. Logout
```
✓ All steps completed without error

### 20.3 Failed Angel One Connection Recovery
```
1. Admin enters invalid API key
2. Clicks "Connect"
3. See error message "Invalid credentials"
4. Status shows "Disconnected"
5. Analysis buttons remain disabled
6. Admin re-enters correct API key
7. Clicks "Connect" again
8. See "Connected ✓" status
9. Analysis buttons now enabled
10. Click "Analyze All Sectors"
11. Analysis runs successfully
```
✓ Recovery successful

### 20.4 Subscriber Cooldown Test
```
1. Subscriber in "Sector Analysis" tab
2. Clicks "Refresh" at 10:00:00
3. Data reloads immediately
4. Refresh button disabled
5. Message: "Next refresh allowed after 10:01:00 IST"
6. Try clicking refresh again → no response (button disabled)
7. Wait until 10:01:00
8. Button automatically re-enables
9. Click refresh successfully
10. Button disabled again for new 60s
```
✓ Cooldown working correctly

---

## FINAL VERIFICATION CHECKLIST

### Critical Path (Must Pass)
- [ ] App loads without errors
- [ ] Admin login works
- [ ] Subscriber login works
- [ ] Admin can connect to Angel One (with valid credentials)
- [ ] Admin can run sector analysis successfully
- [ ] Admin can run ETF analysis successfully
- [ ] Subscriber can view sector data
- [ ] Subscriber can view ETF data
- [ ] Subscriber 60-second refresh cooldown enforces
- [ ] No AttributeError on refresh (st.rerun works)
- [ ] ETF count consistent at 34 across 5 refreshes
- [ ] IST timestamps display correctly
- [ ] Data persists in appdata volume
- [ ] No crashes in `flyctl logs -f`
- [ ] Mobile responsive (basic check)

### High Priority (Should Pass)
- [ ] All 19 sectors display correctly
- [ ] All 34 ETFs display correctly
- [ ] Comprehensive report loads (both sectors and ETFs)
- [ ] Email templates render properly
- [ ] Disclaimer visible
- [ ] User Management accessible to admin
- [ ] System Settings accessible to admin
- [ ] Sidebar properly configured
- [ ] HTTPS working (lock icon visible)

### Medium Priority (Nice to Have)
- [ ] Auto-refresh feature working (if implemented)
- [ ] Audit trail logging (if implemented)
- [ ] Browser history navigation working
- [ ] Dark mode toggle (if implemented)
- [ ] Export to CSV/PDF (if implemented)
- [ ] Advanced filtering/sorting (if implemented)

### Documentation & Compliance
- [ ] Educational Edition label visible
- [ ] Disclaimers present in all reports
- [ ] Risk disclosure statements clear
- [ ] Privacy policy accessible (if implemented)
- [ ] Terms & Conditions accessible (if implemented)
- [ ] No investment advice language used

---

## TEST RESULTS SUMMARY

| Category | Status | Notes |
|----------|--------|-------|
| Authentication | [ ] | ✓/✗/Partial |
| Authorization | [ ] | ✓/✗/Partial |
| Sector Analysis | [ ] | ✓/✗/Partial |
| ETF Analysis | [ ] | ✓/✗/Partial |
| Data Refresh | [ ] | ✓/✗/Partial |
| Angel One API | [ ] | ✓/✗/Partial |
| Email Templates | [ ] | ✓/✗/Partial |
| User Management | [ ] | ✓/✗/Partial |
| Mobile Responsive | [ ] | ✓/✗/Partial |
| Security | [ ] | ✓/✗/Partial |
| Performance | [ ] | ✓/✗/Partial |
| Error Handling | [ ] | ✓/✗/Partial |

---

## KNOWN LIMITATIONS & NOTES

1. **Password Storage:** Current version stores passwords in plaintext in `users_database.json` (educational only, not production-ready)
2. **Email Distribution:** Email sending not yet implemented (Phase 2 feature)
3. **User Creation UI:** Admin UI for creating users not yet implemented (manual JSON edit currently)
4. **Auto-Refresh:** Auto-refresh feature is optional, may not be enabled
5. **Rate Limiting:** Angel One API rate limits not yet enforced in code (manual refresh management)
6. **Webhooks:** Cashfree payment webhook integration not yet active
7. **Error Email Alerts:** Automated error notification to admin not yet implemented

---

**Date Tested:** [YYYY-MM-DD]  
**Tester Name:** ___________________  
**Overall Status:** ✓ PASS / ✗ FAIL / 🟡 PARTIAL  
**Critical Issues:** [List any blocking issues]  
**Next Steps:** [Recommendations for Phase 2]

