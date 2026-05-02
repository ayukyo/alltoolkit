# fake_data_utils

Generate realistic fake/mock data for testing and development. Zero external dependencies - uses only Python stdlib.

## Features

- **Person Data**: Names, genders, ages, birthdays
- **Contact Data**: Emails, phone numbers, addresses
- **Internet Data**: URLs, IPs, MAC addresses, user agents
- **Business Data**: Companies, job titles, salaries
- **Product Data**: Products, prices, SKUs, barcodes
- **Date/Time**: Dates, times, timestamps, timezones
- **Text Data**: Sentences, paragraphs, titles
- **ID Data**: UUIDs, order IDs, transaction IDs
- **File Data**: Filenames, paths, MIME types
- **Complete Objects**: Users, orders, API responses
- **Batch Generation**: Generate multiple records at once

## Quick Start

```python
from fake_data_utils import mod as fake

# Person data
name = fake.fake_name()  # "John Smith"
name_zh = fake.fake_name('zh')  # "王伟"
email = fake.fake_email()  # "john.smith1234@gmail.com"
phone = fake.fake_phone('US')  # "(212) 555-1234"

# Internet data
url = fake.fake_url()  # "https://example.com/api/users"
ip = fake.fake_ipv4()  # "192.168.1.1"
ua = fake.fake_user_agent()  # "Mozilla/5.0 ..."

# Business data
company = fake.fake_company()  # "Global Technologies Inc."
job = fake.fake_job_title()  # "Software Engineer"

# Complete objects
user = fake.fake_user()  # Full user profile
order = fake.fake_order()  # Complete order with items
```

## API Reference

### Person Data

| Function | Description | Returns |
|----------|-------------|---------|
| `fake_name(lang, gender)` | Full name | str |
| `fake_first_name(lang, gender)` | First name | str |
| `fake_last_name(lang)` | Last name | str |
| `fake_gender()` | Random gender | str |
| `fake_age(min, max)` | Random age | int |
| `fake_birthday(min_age, max_age)` | Birthday (YYYY-MM-DD) | str |

### Contact Data

| Function | Description | Returns |
|----------|-------------|---------|
| `fake_email(domain)` | Email address | str |
| `fake_phone(country)` | Phone number | str |
| `fake_address(lang)` | Address dict | Dict |
| `fake_full_address(lang)` | Address string | str |

### Internet Data

| Function | Description | Returns |
|----------|-------------|---------|
| `fake_url(secure, domain, path)` | URL | str |
| `fake_domain()` | Domain name | str |
| `fake_ipv4(private)` | IPv4 address | str |
| `fake_ipv6()` | IPv6 address | str |
| `fake_mac_address()` | MAC address | str |
| `fake_user_agent()` | User-Agent header | str |
| `fake_http_method()` | HTTP method | str |
| `fake_http_status()` | Status code + desc | Tuple |
| `fake_api_path()` | API endpoint path | str |

### Business Data

| Function | Description | Returns |
|----------|-------------|---------|
| `fake_company(lang)` | Company name | str |
| `fake_job_title()` | Job title | str |
| `fake_industry()` | Industry | str |
| `fake_salary(min, max)` | Annual salary | int |
| `fake_department()` | Department | str |

### Product Data

| Function | Description | Returns |
|----------|-------------|---------|
| `fake_product(category)` | Product dict | Dict |
| `fake_product_name(category)` | Product name | str |
| `fake_price(min, max, currency)` | Price string | str |
| `fake_sku(prefix)` | SKU code | str |
| `fake_barcode()` | EAN-13 barcode | str |

### Date/Time Data

| Function | Description | Returns |
|----------|-------------|---------|
| `fake_date(start_year, end_year)` | Date (YYYY-MM-DD) | str |
| `fake_time()` | Time (HH:MM:SS) | str |
| `fake_datetime()` | Datetime | str |
| `fake_timestamp()` | Unix timestamp | int |
| `fake_timezone()` | Timezone | str |

### Text Data

| Function | Description | Returns |
|----------|-------------|---------|
| `fake_sentence(min_words, max_words)` | Lorem sentence | str |
| `fake_paragraph(min_sentences, max_sentences)` | Lorem paragraph | str |
| `fake_text(paragraphs)` | Multi-paragraph text | str |
| `fake_word()` | Single word | str |
| `fake_title(min_words, max_words)` | Title | str |
| `fake_chinese_sentence(min_chars, max_chars)` | Chinese text | str |

### ID Data

| Function | Description | Returns |
|----------|-------------|---------|
| `fake_uuid()` | UUID | str |
| `fake_id(prefix, length)` | Custom ID | str |
| `fake_order_id()` | Order ID | str |
| `fake_transaction_id()` | Transaction ID | str |
| `fake_tracking_number()` | Tracking number | str |

### File Data

| Function | Description | Returns |
|----------|-------------|---------|
| `fake_filename(category, ext)` | Filename | str |
| `fake_file_size(min_kb, max_kb)` | Size string | str |
| `fake_file_path(depth, category)` | File path | str |
| `fake_mime_type(category)` | MIME type | str |

### Complete Objects

| Function | Description | Returns |
|----------|-------------|---------|
| `fake_user(lang, country)` | Complete user profile | Dict |
| `fake_product_full()` | Full product info | Dict |
| `fake_order(lang)` | Order with items | Dict |
| `fake_api_response(status, data)` | API response | Dict |

### Batch Generation

| Function | Description | Returns |
|----------|-------------|---------|
| `fake_users(count, lang)` | Multiple users | List[Dict] |
| `fake_products(count)` | Multiple products | List[Dict] |
| `fake_orders(count, lang)` | Multiple orders | List[Dict] |

## Examples

See `examples/` directory for more usage examples.

## License

MIT License - Part of AllToolkit