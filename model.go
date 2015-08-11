package main

import (
	"time"
)

const InvalidDuration = time.Duration(-1)

type TimeSlice struct {
	Start *time.Time `json:"start"`
	End   *time.Time `json:"end"`
}

func (timeSlice *TimeSlice) Duration() time.Duration {
	if timeSlice.Start == nil || timeSlice.End == nil {
		return InvalidDuration
	}

	return timeSlice.End.Sub(*timeSlice.Start)
}

func (timeSlice *TimeSlice) IsComplete() bool {
	return timeSlice.End != nil
}

type Context struct {
	Id         string      `json:"id"`
	TimeSlices []TimeSlice `json:"time_slices"`
}

type Storage struct {
	CurrentContextId string    `json:"current_context_id"`
	Contexts         []Context `json:"contexts"`
}
