package main

import (
	"time"
)

type Context struct {
	Id         string      `json:"id"`
	TimeSlices []TimeSlice `json:"time_slices"`
}

func (c *Context) Start() {
	if len(c.TimeSlices) > 0 {
		latest := c.TimeSlices[len(c.TimeSlices)-1]
		if latest.End == nil {
			return
		}
	}
	now := time.Now()
	c.TimeSlices = append(c.TimeSlices, TimeSlice{&now, nil})
}

func (c *Context) Stop() {
	if c.IsStopped() {
		return
	}

	now := time.Now()
	latest := &c.TimeSlices[len(c.TimeSlices)-1]
	latest.End = &now
}

func (c *Context) IsStopped() bool {
	if len(c.TimeSlices) == 0 {
		return true
	}

	latest := &c.TimeSlices[len(c.TimeSlices)-1]
	if latest.End != nil {
		return true
	}

	return false
}

func (c *Context) GetTotalDuration() time.Duration {
	duration := time.Duration(0)
	for _, timeSlice := range c.TimeSlices {
		if timeSlice.IsComplete() {
			duration += *timeSlice.Duration()
		} else {
			duration += time.Now().Sub(*timeSlice.Start)
		}
	}
	return duration
}
