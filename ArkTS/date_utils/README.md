# Date Utilities for ArkTS

A comprehensive date/time manipulation utility module for ArkTS/HarmonyOS with zero external dependencies.

## Features

- **Date Creation & Parsing**: Create dates from components, timestamps, or parse date strings
- **Date Formatting**: Flexible format strings with support for localized month/day names
- **Date Arithmetic**: Add/subtract milliseconds, seconds, minutes, hours, days, weeks, months, years
- **Date Boundary Operations**: Get start/end of day, week, month, quarter, year, hour, minute
- **Date Comparison**: Before/after/same checks, between validation, past/future detection
- **Date Difference**: Calculate differences in various units (ms, sec, min, hour, day, week, month, year)
- **Relative Time**: Format as "2 hours ago", "in 3 days" (English and Chinese)
- **Validation**: Check if dates/values are valid
- **Utility Functions**: Age calculation, business days, nth weekday of month, date ranges
- **Class-based API**: Chainable DateUtils class for fluent operations

## Installation

Copy the `date_utils` folder into your HarmonyOS project.

## Usage

### Basic Date Operations

```typescript
import { now, today, createDate, format } from './date_utils/mod';

// Get current date and timestamp
const currentTime = now();
const currentTimestamp = timestamp();
const todayDate = today();

// Create dates
const date = createDate(2024, 3, 15, 10, 30, 0);
const fromTs = fromTimestamp(1709424000000);

// Format dates
console.log(format(date, 'YYYY-MM-DD HH:mm:ss')); // "2024-03-15 10:30:00"
console.log(format(date, 'MMMM DD, YYYY')); // "March 15, 2024"
console.log(format(date, 'dddd')); // "Friday"
```

### Date Parsing

```typescript
import { parseDate, parseISO } from './date_utils/mod';

// Parse various formats
const date1 = parseDate('2024-03-15');
const date2 = parseDate('2024/03/15');
const date3 = parseISO('2024-03-15T10:30:00Z');
```

### Date Arithmetic

```typescript
import { addDays, addMonths, addYears, subtractDays } from './date_utils/mod';

const date = createDate(2024, 1, 15);

const tomorrow = addDays(date, 1);
const lastMonth = subtractMonths(date, 1);
const nextYear = addYears(date, 1);
const inTwoWeeks = addWeeks(date, 2);
```

### Date Boundaries

```typescript
import { startOfDay, endOfDay, startOfMonth, endOfMonth } from './date_utils/mod';

const date = createDate(2024, 3, 15, 14, 30);

const midnight = startOfDay(date); // 2024-03-15 00:00:00
const endOfDay = endOfDay(date); // 2024-03-15 23:59:59.999
const firstDay = startOfMonth(date); // 2024-03-01 00:00:00
const lastDay = endOfMonth(date); // 2024-03-31 23:59:59.999
```

### Date Comparison

```typescript
import { isBefore, isAfter, isSameDay, isToday, isWeekend } from './date_utils/mod';

const date1 = createDate(2024, 1, 1);
const date2 = createDate(2024, 6, 1);

console.log(isBefore(date1, date2)); // true
console.log(isSameDay(date1, date1)); // true
console.log(isToday(new Date())); // true
console.log(isWeekend(createDate(2024, 3, 16))); // true (Saturday)
```

### Date Difference

```typescript
import { diff, diffInDays, diffInMonths } from './date_utils/mod';

const date1 = createDate(2024, 1, 1);
const date2 = createDate(2024, 6, 15);

const difference = diff(date1, date2);
console.log(difference.days); // ~165
console.log(difference.months); // ~5

console.log(diffInDays(date1, date2)); // 165
console.log(diffInMonths(date1, date2)); // 5
```

### Relative Time

```typescript
import { fromNow, formatDistanceToNow } from './date_utils/mod';

const pastDate = subtractDays(new Date(), 3);
console.log(fromNow(pastDate)); // "3 days ago"

// Chinese format
console.log(formatDistanceToNow(pastDate, 'cn')); // "3天前"
```

### Utility Functions

```typescript
import { 
  getAge, 
  countBusinessDays, 
  addBusinessDays,
  getNthDayOfMonth,
  getDatesInRange 
} from './date_utils/mod';

// Calculate age
const birthDate = createDate(1990, 6, 15);
const age = getAge(birthDate); // Current age

// Business days
const start = createDate(2024, 3, 18); // Monday
const end = createDate(2024, 3, 22); // Friday
console.log(countBusinessDays(start, end)); // 5

const friday = createDate(2024, 3, 22);
const nextBusinessDay = addBusinessDays(friday, 1); // Monday (skips weekend)

// Find nth day of month (e.g., 2nd Monday of March)
const secondMonday = getNthDayOfMonth(2024, 3, 1, 2); // March 11

// Get all dates in range
const dates = getDatesInRange(start, end); // Array of 5 dates
```

### Class-based API (Chainable)

```typescript
import { DateUtils } from './date_utils/mod';

const result = DateUtils.create(2024, 1, 15)
  .addDays(5)
  .addMonths(1)
  .startOfDay()
  .toDate();

console.log(DateUtils.now()
  .subtractHours(2)
  .fromNow()); // "2 hours ago"
```

## Format Tokens

| Token | Output | Example |
|-------|--------|---------|
| YYYY | 4-digit year | 2024 |
| YY | 2-digit year | 24 |
| MM | 2-digit month | 03 |
| M | month | 3 |
| DD | 2-digit day | 15 |
| D | day | 15 |
| HH | 24-hour hour | 14 |
| H | hour | 14 |
| hh | 12-hour hour | 02 |
| h | hour | 2 |
| mm | 2-digit minute | 30 |
| m | minute | 30 |
| ss | 2-digit second | 45 |
| s | second | 45 |
| SSS | milliseconds | 500 |
| A | AM/PM | PM |
| a | am/pm | pm |
| dddd | day name | Friday |
| ddd | short day name | Fri |
| MMMM | month name | March |
| MMM | short month name | Mar |

## Constants

```typescript
import { 
  MILLIS_PER_SECOND, 
  MILLIS_PER_MINUTE, 
  MILLIS_PER_HOUR,
  MILLIS_PER_DAY,
  MILLIS_PER_WEEK,
  MONTH_NAMES_EN,
  DAY_NAMES_EN,
  MONTH_NAMES_CN,
  DAY_NAMES_CN
} from './date_utils/mod';

console.log(MILLIS_PER_DAY); // 86400000
console.log(MONTH_NAMES_EN[0]); // "January"
console.log(MONTH_NAMES_CN[0]); // "一月"
```

## API Reference

### Date Creation
- `now()` - Current date
- `timestamp()` - Current timestamp in ms
- `createDate(year, month, day, hour?, minute?, second?, ms?)` - Create from components
- `fromTimestamp(ms)` - Create from timestamp
- `clone(date)` - Clone a date
- `today()` - Today at midnight
- `tomorrow()` - Tomorrow at midnight
- `yesterday()` - Yesterday at midnight

### Date Parsing
- `parseDate(dateStr, format?)` - Parse date string
- `parseISO(isoString)` - Parse ISO string

### Date Formatting
- `format(date, formatStr)` - Format with format string
- `toISO(date)` - Convert to ISO string
- `toISODate(date)` - YYYY-MM-DD
- `toISOTime(date)` - HH:mm:ss
- `toISODatetime(date)` - YYYY-MM-DD HH:mm:ss

### Date Component Getters
- `getYear(date)` - Year
- `getMonth(date)` - Month (1-12)
- `getDay(date)` - Day of month (1-31)
- `getDayOfWeek(date)` - Day of week (0-6, Sunday=0)
- `getISODayOfWeek(date)` - ISO day of week (1-7, Monday=1)
- `getHour(date)` - Hour (0-23)
- `getMinute(date)` - Minute (0-59)
- `getSecond(date)` - Second (0-59)
- `getMillisecond(date)` - Millisecond (0-999)
- `getDayOfYear(date)` - Day of year (1-366)
- `getWeekOfYear(date)` - Week of year
- `getQuarter(date)` - Quarter (1-4)
- `getDaysInMonth(date)` - Days in month
- `isLeapYear(date)` - Check leap year

### Date Arithmetic
- `addMilliseconds(date, amount)` - Add ms
- `addSeconds(date, amount)` - Add seconds
- `addMinutes(date, amount)` - Add minutes
- `addHours(date, amount)` - Add hours
- `addDays(date, amount)` - Add days
- `addWeeks(date, amount)` - Add weeks
- `addMonths(date, amount)` - Add months
- `addYears(date, amount)` - Add years
- `subtractX(date, amount)` - Subtract (each has a subtract variant)

### Date Boundary Operations
- `startOfDay(date)` - Midnight
- `endOfDay(date)` - 23:59:59.999
- `startOfWeek(date, startOnSunday?)` - First day of week
- `endOfWeek(date, endOnSaturday?)` - Last day of week
- `startOfMonth(date)` - First day of month
- `endOfMonth(date)` - Last day of month
- `startOfYear(date)` - January 1
- `endOfYear(date)` - December 31
- `startOfQuarter(date)` - First day of quarter
- `endOfQuarter(date)` - Last day of quarter
- `startOfHour(date)` - Beginning of hour
- `endOfHour(date)` - End of hour
- `startOfMinute(date)` - Beginning of minute
- `endOfMinute(date)` - End of minute

### Date Comparison
- `isBefore(date, dateToCompare)` - Check if before
- `isAfter(date, dateToCompare)` - Check if after
- `isSame(date, dateToCompare)` - Check if exactly same
- `isSameDay(date, dateToCompare)` - Check if same day
- `isSameMonth(date, dateToCompare)` - Check if same month
- `isSameYear(date, dateToCompare)` - Check if same year
- `isBetween(date, start, end, inclusive?)` - Check if between
- `isToday(date)` - Check if today
- `isYesterday(date)` - Check if yesterday
- `isTomorrow(date)` - Check if tomorrow
- `isPast(date)` - Check if in past
- `isFuture(date)` - Check if in future
- `isWeekend(date)` - Check if weekend
- `isWeekday(date)` - Check if weekday
- `min(date1, date2)` - Minimum of two dates
- `max(date1, date2)` - Maximum of two dates

### Date Difference
- `diff(date1, date2)` - Full difference object
- `diffInMilliseconds(date1, date2)` - Difference in ms
- `diffInSeconds(date1, date2)` - Difference in seconds
- `diffInMinutes(date1, date2)` - Difference in minutes
- `diffInHours(date1, date2)` - Difference in hours
- `diffInDays(date1, date2)` - Difference in days
- `diffInWeeks(date1, date2)` - Difference in weeks
- `diffInMonths(date1, date2)` - Difference in months
- `diffInYears(date1, date2)` - Difference in years

### Relative Time
- `fromNow(date, locale?)` - Format relative to now
- `formatDistanceToNow(date, locale)` - Format distance to now

### Validation
- `isValid(date)` - Check if valid Date
- `isValidDateString(dateStr)` - Check if valid date string
- `isLeapYearNum(year)` - Check if leap year
- `getDaysInMonthNum(year, month)` - Get days in month
- `isValidDate(year, month, day)` - Validate date components

### Utility Functions
- `getAge(birthDate, referenceDate?)` - Calculate age
- `getNextDayOfWeek(date, dayOfWeek)` - Next occurrence of day
- `getPreviousDayOfWeek(date, dayOfWeek)` - Previous occurrence
- `getNthDayOfMonth(year, month, dayOfWeek, n)` - Nth weekday of month
- `getDatesInRange(start, end)` - All dates in range
- `countBusinessDays(start, end)` - Count business days
- `addBusinessDays(date, amount)` - Add business days

## Test

Run the test suite:

```typescript
import './date_utils_test';
```

## License

MIT

## Version

1.0.0 - 2026-04-25