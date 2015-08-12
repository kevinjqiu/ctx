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

func TestContextStopOnExistingPausedContext(t *testing.T) {
	start := time.Unix(1439347110, 0)
	end := time.Unix(1439347115, 0)
	ctx := Context{
		Id: "id",
		TimeSlices: []TimeSlice{
			newTimeSlice(start, end),
		},
	}

	ctx.Stop()

	assert.Equal(t, 1, len(ctx.TimeSlices))
	assert.Equal(t, start, *ctx.TimeSlices[0].Start)
	assert.Equal(t, end, *ctx.TimeSlices[0].End)
}

func TestContextStopOnRunningContext(t *testing.T) {
	start := time.Unix(1439347110, 0)
	ctx := Context{
		Id: "id",
		TimeSlices: []TimeSlice{
			TimeSlice{&start, nil},
		},
	}

	ctx.Stop()

	assert.Equal(t, 1, len(ctx.TimeSlices))
	assert.Equal(t, start, *ctx.TimeSlices[0].Start)
	assert.NotNil(t, ctx.TimeSlices[0].End)
}

func TestGetTotalDurationWithNoTimeSlices(t *testing.T) {
	ctx := Context{Id: "id"}
	assert.Equal(t, 0, ctx.GetTotalDuration())
}

func TestGetTotalDurationWithNoCompleteTimeSlices(t *testing.T) {
	start := time.Unix(1439347110, 0)
	ctx := Context{
		Id: "id",
		TimeSlices: []TimeSlice{
			TimeSlice{&start, nil},
		},
	}
	assert.Equal(t, 0, ctx.GetTotalDuration())
}

func TestGetTotalDurationWithCompleteTimeSlices(t *testing.T) {
	ctx := Context{
		Id: "id",
		TimeSlices: []TimeSlice{
			newTimeSlice(time.Unix(1439347110, 0), time.Unix(1439347115, 0)),
			newTimeSlice(time.Unix(1439347120, 0), time.Unix(1439347125, 0)),
		},
	}

	assert.Equal(t, 10, ctx.GetTotalDuration().Seconds())
}

func TestGetTotalDurationWithSomeIncompleteTimeSlices(t *testing.T) {
	start2 := time.Unix(1439347120, 0)
	ctx := Context{
		Id: "id",
		TimeSlices: []TimeSlice{
			newTimeSlice(time.Unix(1439347110, 0), time.Unix(1439347115, 0)),
			TimeSlice{&start2, nil},
		},
	}

	assert.Equal(t, 5, ctx.GetTotalDuration().Seconds())
}
