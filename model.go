package main

import (
	"encoding/json"
	"io/ioutil"
	"os"
	"time"
)

const InvalidDuration = time.Duration(-1)

const Version = "1.0"

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

func (c *Context) Start() {
}

func (c *Context) Stop() {
}

func (c *Context) Resume() {
}

type Storage struct {
	CurrentContextId string    `json:"current_context_id"`
	Contexts         []Context `json:"contexts"`
	FileName         string    `json:"file_name"`
	Version          string    `json:"version"`
}

func (s *Storage) GetContextById(contextId string) *Context {
	for _, context := range s.Contexts {
		if context.Id == contextId {
			return &context
		}
	}
	return nil
}

func NewStorage(fileName string) (*Storage, error) {
	storage := Storage{
		FileName: fileName,
		Version:  Version,
	}

	content, errReadFile := ioutil.ReadFile(fileName)
	if errReadFile != nil {
		if os.IsNotExist(errReadFile) {
			storage.Save()
		} else {
			return nil, errReadFile
		}
	}

	if errUnmarshal := json.Unmarshal(content, &storage); errUnmarshal != nil {
		return nil, errUnmarshal
	}

	return &storage, nil
}

func (s *Storage) Save() error {
	marshalled, errMarshal := json.Marshal(s)
	if errMarshal != nil {
		return errMarshal
	}

	if errWriteFile := ioutil.WriteFile(s.FileName, marshalled, 0644); errWriteFile != nil {
		return errWriteFile
	}

	return nil
}

func (s *Storage) SwitchContext(contextId string) error {
	if s.CurrentContextId == contextId {
		currentContext := s.GetContextById(s.CurrentContextId)
		if currentContext != nil {
			currentContext.Resume()
		} else {
			context := Context{
				Id: contextId,
			}
			context.Start()
			s.Contexts = append(s.Contexts, context)
		}
	} else {
		currentContext := s.GetContextById(s.CurrentContextId)
		currentContext.Stop()
		context := Context{
			Id: contextId,
		}
		context.Start()
		s.Contexts = append(s.Contexts, context)
	}

	s.CurrentContextId = contextId
	err := s.Save()
	return err
}

func deserialize(ctxFileName string) ([]TimeSlice, error) {
	content, errReadFile := ioutil.ReadFile(ctxFileName)
	if errReadFile != nil {
		return nil, errReadFile
	}

	var slices []TimeSlice
	if errUnmarshal := json.Unmarshal(content, &slices); errUnmarshal != nil {
		return nil, errUnmarshal
	}

	return slices, nil
}

func serialize(ctxFileName string, slices []TimeSlice) error {
	slicesJson, errMarshal := json.Marshal(slices)
	if errMarshal != nil {
		return errMarshal
	}

	if errWriteFile := ioutil.WriteFile(ctxFileName, slicesJson, 0644); errWriteFile != nil {
		return errWriteFile
	}

	return nil
}
