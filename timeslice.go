package main

import (
	"time"
)

type TimeSlice struct {
	Start *time.Time `json:"start"`
	End   *time.Time `json:"end"`
}

func (timeSlice *TimeSlice) Duration() *time.Duration {
	if timeSlice.Start == nil || timeSlice.End == nil {
		return nil
	}

	result := timeSlice.End.Sub(*timeSlice.Start)
	return &result
}

func (timeSlice *TimeSlice) IsComplete() bool {
	return timeSlice.End != nil
}
