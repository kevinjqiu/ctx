package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
	"time"
)

func TestTimeSliceIsNotComplete(t *testing.T) {
	start := time.Unix(1439347110, 0)
	timeSlice := TimeSlice{&start, nil}
	assert.False(t, timeSlice.IsComplete())
}

func TestTimeSliceIsComplete(t *testing.T) {
	start := time.Unix(1439347110, 0)
	end := time.Unix(1439347115, 0)
	timeSlice := TimeSlice{&start, &end}
	assert.True(t, timeSlice.IsComplete())
}

func TestTimeSliceDurationInvalid(t *testing.T) {
	var timeSlice TimeSlice

	someTime := time.Unix(1439347115, 0)

	timeSlice = TimeSlice{nil, &someTime}
	assert.Nil(t, timeSlice.Duration())

	timeSlice = TimeSlice{&someTime, nil}
	assert.Nil(t, timeSlice.Duration())

	timeSlice = TimeSlice{nil, nil}
	assert.Nil(t, timeSlice.Duration())
}

func TestTimeSliceDuration(t *testing.T) {
	start := time.Unix(1439347115, 0)
	end := time.Unix(1439347125, 0)

	timeSlice := TimeSlice{&start, &end}
	assert.Equal(t, 10, timeSlice.Duration().Seconds())
}
