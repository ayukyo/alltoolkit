package jwt_utils

import "errors"

var (
	// ErrInvalidTokenFormat indicates the token format is invalid
	ErrInvalidTokenFormat = errors.New("jwt: invalid token format")
	
	// ErrUnsupportedAlgorithm indicates the algorithm is not supported
	ErrUnsupportedAlgorithm = errors.New("jwt: unsupported algorithm")
	
	// ErrInvalidSignature indicates the signature is invalid
	ErrInvalidSignature = errors.New("jwt: invalid signature")
	
	// ErrTokenExpired indicates the token has expired
	ErrTokenExpired = errors.New("jwt: token has expired")
	
	// ErrTokenNotValidYet indicates the token is not yet valid
	ErrTokenNotValidYet = errors.New("jwt: token is not valid yet")
)