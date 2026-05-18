const isbn = @import("isbn.zig");

pub const Isbn = isbn.Isbn;
pub const IsbnType = isbn.IsbnType;
pub const IsbnError = isbn.IsbnError;
pub const isValidIsbn = isbn.isValidIsbn;
pub const detectIsbnType = isbn.detectIsbnType;
pub const calculateIsbn10CheckDigit = isbn.calculateIsbn10CheckDigit;
pub const calculateIsbn13CheckDigit = isbn.calculateIsbn13CheckDigit;

test {
    _ = @import("isbn.zig");
}