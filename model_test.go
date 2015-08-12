package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
	"time"
)

func newTimeSlice(start time.Time, end time.Time) TimeSlice {
	return TimeSlice{&start, &end}
}

func TestContextStartOnNewContext(t *testing.T) {
	ctx := Context{Id: "id"}
	ctx.Start()

	assert.Equal(t, 1, len(ctx.TimeSlices))
	assert.NotNil(t, ctx.TimeSlices[0].Start)
	assert.Nil(t, ctx.TimeSlices[0].End)
}

func TestContextStartOnExistingPausedContext(t *testing.T) {
	ctx := Context{
		Id: "id",
		TimeSlices: []TimeSlice{
			newTimeSlice(time.Unix(1439347110, 0), time.Unix(1439347115, 0)),
		},
	}

	ctx.Start()

	assert.Equal(t, 2, len(ctx.TimeSlices))
	assert.NotNil(t, ctx.TimeSlices[1].Start)
	assert.Nil(t, ctx.TimeSlices[1].End)
}

func TestContextStartOnExistingStillRunningContext(t *testing.T) {
	start := time.Unix(1439347110, 0)
	ctx := Context{
		Id: "id",
		TimeSlices: []TimeSlice{
			TimeSlice{&start, nil},
		},
	}

	ctx.Start()

	assert.Equal(t, 1, len(ctx.TimeSlices))
	assert.Equal(t, start, *ctx.TimeSlices[0].Start)
	assert.Nil(t, ctx.TimeSlices[0].End)
}
