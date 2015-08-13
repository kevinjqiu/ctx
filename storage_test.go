package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
	"time"
)

func TestGetContextById(t *testing.T) {
	context1 := Context{
		Id: "ID1",
	}

	context2 := Context{
		Id: "ID2",
	}

	storage := Storage{
		CurrentContextId: "ID1",
		Contexts: []*Context{
			&context1, &context2,
		},
	}

	assert.Equal(t, context1, *storage.GetContextById("ID1"))
	assert.Equal(t, context2, *storage.GetContextById("ID2"))
	assert.Nil(t, storage.GetContextById("ID3"))
}

func TestGetCurrentContext(t *testing.T) {
	context1 := Context{
		Id: "ID1",
	}

	context2 := Context{
		Id: "ID2",
	}

	storage := Storage{
		CurrentContextId: "ID1",
		Contexts: []*Context{
			&context1, &context2,
		},
	}

	assert.Equal(t, context1, *storage.GetCurrentContext())
}

func TestSwitchContextNewContext(t *testing.T) {
	storage := Storage{
		CurrentContextId: "",
	}
	storage.SwitchContext("ID")
	assert.Equal(t, 1, len(storage.Contexts))
	assert.Equal(t, 1, len(storage.Contexts[0].TimeSlices))
	assert.NotNil(t, storage.Contexts[0].TimeSlices[0].Start)
	assert.Nil(t, storage.Contexts[0].TimeSlices[0].End)
}

func TestSwitchContextExistingContext(t *testing.T) {
	storage := Storage{
		CurrentContextId: "ID",
		Contexts: []*Context{
			&Context{
				Id: "ID",
				TimeSlices: []TimeSlice{
					newIncompleteTimeSlice(time.Unix(1439347110, 0)),
				},
			},
		},
	}
	storage.SwitchContext("ID2")

	assert.Equal(t, 2, len(storage.Contexts))

	assert.Equal(t, 1, len(storage.Contexts[0].TimeSlices))
	assert.NotNil(t, storage.Contexts[0].TimeSlices[0].Start)
	assert.NotNil(t, storage.Contexts[0].TimeSlices[0].End)

	assert.Equal(t, 1, len(storage.Contexts[1].TimeSlices))
	assert.NotNil(t, storage.Contexts[1].TimeSlices[0].Start)
	assert.Nil(t, storage.Contexts[1].TimeSlices[0].End)
}

func TestSwitchContextOnCurrentContext(t *testing.T) {
	storage := Storage{
		CurrentContextId: "ID",
		Contexts: []*Context{
			&Context{
				Id: "ID",
				TimeSlices: []TimeSlice{
					newIncompleteTimeSlice(time.Unix(1439347110, 0)),
				},
			},
		},
	}
	storage.SwitchContext("ID")

	assert.Equal(t, 1, len(storage.Contexts))

	assert.Equal(t, 1, len(storage.Contexts[0].TimeSlices))
	assert.NotNil(t, storage.Contexts[0].TimeSlices[0].Start)
	assert.Nil(t, storage.Contexts[0].TimeSlices[0].End)
}

func TestListContextsNoContext(t *testing.T) {
	storage := Storage{
		CurrentContextId: "",
		Contexts:         []*Context{},
	}
	contexts := storage.ListContexts()

	assert.Equal(t, 0, len(contexts))
}

func TestListContextsWithContexts(t *testing.T) {
	storage := Storage{
		CurrentContextId: "ID-1",
		Contexts: []*Context{
			&Context{
				Id: "ID-1",
			},
			&Context{
				Id: "ID-2",
			},
		},
	}
	contexts := storage.ListContexts()

	assert.Equal(t, []string{"ID-1", "ID-2"}, contexts)
}
