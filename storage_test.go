package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
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
		Contexts: []Context{
			context1, context2,
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
		Contexts: []Context{
			context1, context2,
		},
	}

	assert.Equal(t, context1, *storage.GetCurrentContext())
}
