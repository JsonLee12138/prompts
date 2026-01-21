package responder

import (
	"encoding/json"
	"net/http"
	"time"
)

// Response represents the standard Strapi-style API response
type Response struct {
	Data  interface{} `json:"data"`
	Error *Error      `json:"error,omitempty"`
	Meta  *Meta       `json:"meta,omitempty"`
}

// Error represents the error structure
type Error struct {
	Code    int         `json:"code,omitempty"`
	Status  int         `json:"status,omitempty"`
	Name    string      `json:"name,omitempty"`
	Message string      `json:"message"`
	Details interface{} `json:"details,omitempty"`
}

// Meta represents metadata for the response
type Meta struct {
	Pagination *Pagination `json:"pagination,omitempty"`
	TraceID    string      `json:"traceId,omitempty"`
	Took       int64       `json:"took,omitempty"`
}

// Pagination represents pagination information
type Pagination struct {
	Page       int  `json:"page"`
	PageSize   int  `json:"pageSize"`
	Total      int  `json:"total"`
	TotalPages int  `json:"totalPages"`
	HasMore    bool `json:"hasMore"`
}

// Responder is the main response builder
type Responder struct {
	w      http.ResponseWriter
	r      *http.Request
	start  time.Time
}

// NewResponder creates a new responder for the given request
func NewResponder(w http.ResponseWriter, r *http.Request) *Responder {
	return &Responder{
		w:     w,
		r:     r,
		start: time.Now(),
	}
}

// Write writes a successful response
func (res *Responder) Write(statusCode int, data interface{}) {
	response := Response{
		Data:  data,
		Error: nil,
		Meta:  res.buildMeta(),
	}

	res.w.Header().Set("Content-Type", "application/json")
	res.w.WriteHeader(statusCode)
	json.NewEncoder(res.w).Encode(response)
}

// WriteError writes an error response
func (res *Responder) WriteError(statusCode int, err Error) {
	response := Response{
		Data:  nil,
		Error: &err,
		Meta:  res.buildMeta(),
	}

	res.w.Header().Set("Content-Type", "application/json")
	res.w.WriteHeader(statusCode)
	json.NewEncoder(res.w).Encode(response)
}

// WriteList writes a list response with pagination
func (res *Responder) WriteList(data interface{}, pagination *Pagination) {
	response := Response{
		Data:  data,
		Error: nil,
		Meta: &Meta{
			Pagination: pagination,
			TraceID:    res.getTraceID(),
			Took:       res.getDuration(),
		},
	}

	res.w.Header().Set("Content-Type", "application/json")
	res.w.WriteHeader(http.StatusOK)
	json.NewEncoder(res.w).Encode(response)
}

// buildMeta builds the meta information
func (res *Responder) buildMeta() *Meta {
	return &Meta{
		TraceID: res.getTraceID(),
		Took:    res.getDuration(),
	}
}

// getTraceID gets or generates a trace ID
func (res *Responder) getTraceID() string {
	// In production, use a proper tracing system
	// For now, return empty string (can be enhanced with middleware)
	return ""
}

// getDuration calculates the request duration in milliseconds
func (res *Responder) getDuration() int64 {
	return time.Since(res.start).Milliseconds()
}

// Error constructors

func NewError(message string) Error {
	return Error{
		Message: message,
	}
}

func NewBadRequestError(message string) Error {
	return Error{
		Status:  http.StatusBadRequest,
		Code:    4001,
		Message: message,
		Name:    "BadRequestError",
	}
}

func NewNotFoundError(message string) Error {
	return Error{
		Status:  http.StatusNotFound,
		Code:    4041,
		Message: message,
		Name:    "NotFoundError",
	}
}

func NewInternalServerError(message string) Error {
	return Error{
		Status:  http.StatusInternalServerError,
		Code:    5000,
		Message: message,
		Name:    "InternalServerError",
	}
}

func NewValidationError(field string, message string) Error {
	return Error{
		Status:  http.StatusBadRequest,
		Code:    4001,
		Message: "Validation failed",
		Name:    "ValidationError",
		Details: map[string]string{
			field: message,
		},
	}
}

// Helper function to create paginated response
func NewPagination(page, pageSize, total int) *Pagination {
	totalPages := total / pageSize
	if total%pageSize != 0 {
		totalPages++
	}
	hasMore := page < totalPages

	return &Pagination{
		Page:       page,
		PageSize:   pageSize,
		Total:      total,
		TotalPages: totalPages,
		HasMore:    hasMore,
	}
}

// ResponderFactory creates responders for each request
type ResponderFactory struct {
	panicFn func(http.ResponseWriter, *http.Request, interface{})
}

// NewResponderFactory creates a new factory
func NewResponderFactory(panicFn func(http.ResponseWriter, *http.Request, interface{})) *ResponderFactory {
	return &ResponderFactory{
		panicFn: panicFn,
	}
}

// FromRequest creates a responder from an HTTP request
func (f *ResponderFactory) FromRequest(w http.ResponseWriter, r *http.Request) *Responder {
	return NewResponder(w, r)
}

// DefaultPanicFn is the default panic handler
func DefaultPanicFn(w http.ResponseWriter, r *http.Request, err interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusInternalServerError)

	response := Response{
		Data:  nil,
		Error: &Error{
			Status:  http.StatusInternalServerError,
			Code:    5000,
			Message: "Internal server error",
			Name:    "InternalServerError",
		},
		Meta: nil,
	}

	json.NewEncoder(w).Encode(response)
}
