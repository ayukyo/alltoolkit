using System;
using System.Text;

namespace AllToolkit
{
    public static class Base64Utils
    {
        public static string Encode(string input, Encoding encoding = null)
        {
            if (input == null)
                throw new ArgumentNullException(nameof(input));
            encoding = encoding ?? Encoding.UTF8;
            byte[] bytes = encoding.GetBytes(input);
            return Convert.ToBase64String(bytes);
        }

        public static string Encode(byte[] data)
        {
            if (data == null)
                throw new ArgumentNullException(nameof(data));
            return Convert.ToBase64String(data);
        }

        public static string EncodeUrlSafe(string input, Encoding encoding = null, bool padding = true)
        {
            if (input == null)
                throw new ArgumentNullException(nameof(input));
            string base64 = Encode(input, encoding);
            return ToUrlSafe(base64, padding);
        }

        public static string EncodeUrlSafe(byte[] data, bool padding = true)
        {
            if (data == null)
                throw new ArgumentNullException(nameof(data));
            string base64 = Encode(data);
            return ToUrlSafe(base64, padding);
        }

        public static string Decode(string base64, Encoding encoding = null)
        {
            if (base64 == null)
                throw new ArgumentNullException(nameof(base64));
            encoding = encoding ?? Encoding.UTF8;
            byte[] bytes = Convert.FromBase64String(base64);
            return encoding.GetString(bytes);
        }

        public static byte[] DecodeToBytes(string base64)
        {
            if (base64 == null)
                throw new ArgumentNullException(nameof(base64));
            return Convert.FromBase64String(base64);
        }

        public static string DecodeUrlSafe(string base64Url, Encoding encoding = null)
        {
            if (base64Url == null)
                throw new ArgumentNullException(nameof(base64Url));
            string standard = FromUrlSafe(base64Url);
            return Decode(standard, encoding);
        }

        public static byte[] DecodeUrlSafeToBytes(string base64Url)
        {
            if (base64Url == null)
                throw new ArgumentNullException(nameof(base64Url));
            string standard = FromUrlSafe(base64Url);
            return DecodeToBytes(standard);
        }

        public static string TryDecode(string base64, Encoding encoding = null)
        {
            if (base64 == null || !IsValid(base64))
                return null;
            try { return Decode(base64, encoding); }
            catch { return null; }
        }

        public static byte[] TryDecodeToBytes(string base64)
        {
            if (base64 == null || !IsValid(base64))
                return null;
            try { return DecodeToBytes(base64); }
            catch { return null; }
        }

        public static string ToUrlSafe(string base64, bool padding = true)
        {
            if (base64 == null)
                throw new ArgumentNullException(nameof(base64));
            string result = base64.Replace('+', '-').Replace('/', '_');
            if (!padding)
                result = result.TrimEnd('=');
            return result;
        }

        public static string FromUrlSafe(string base64Url)
        {
            if (base64Url == null)
                throw new ArgumentNullException(nameof(base64Url));
            string result = base64Url.Replace('-', '+').Replace('_', '/');
            int padding = 4 - (result.Length % 4);
            if (padding != 4)
                result += new string('=', padding);
            return result;
        }

        public static bool IsValid(string base64)
        {
            if (string.IsNullOrEmpty(base64))
                return false;
            try
            {
                Convert.FromBase64String(base64);
                return true;
            }
            catch
            {
                return false;
            }
        }

        public static bool IsValidUrlSafe(string base64Url)
        {
            if (string.IsNullOrEmpty(base64Url))
                return false;
            try
            {
                string standard = FromUrlSafe(base64Url);
                Convert.FromBase64String(standard);
                return true;
            }
            catch
            {
                return false;
            }
        }

        public static int GetEncodedLength(int inputLength, bool padding = true)
        {
            int result = (int)Math.Ceiling(inputLength * 4.0 / 3.0);
            if (padding && result % 4 != 0)
                result += 4 - (result % 4);
            return result;
        }

        public static int GetDecodedMaxLength(int base64Length)
        {
            return base64Length * 3 / 4;
        }
    }
}
