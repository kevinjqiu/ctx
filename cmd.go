package main

import (
	"encoding/json"
	"fmt"
	"github.com/codegangsta/cli"
	"io/ioutil"
	"os"
	"time"
)

func stopContext(c *cli.Context) {
	ctxFileName := os.ExpandEnv(c.GlobalString("ctxfile"))

	slices, errDeserialize := deserialize(ctxFileName)
	if errDeserialize != nil {
		fmt.Printf("%s", errDeserialize)
		return
	}

	if len(slices) == 0 {
		fmt.Println("You must start a context first")
		return
	}

	slice := &slices[len(slices)-1]
	now := time.Now()
	slice.End = &now

	if errSerialize := serialize(ctxFileName, slices); errSerialize != nil {
		fmt.Printf("%s", errSerialize)
		return
	}
}

func switchContext(c *cli.Context) {
	ctxFileName := os.ExpandEnv(c.GlobalString("ctxfile"))

	slices, errDeserialize := deserialize(ctxFileName)
	if errDeserialize != nil {
		slices = make([]TimeSlice, 0)
	}

	now := time.Now()
	slice := TimeSlice{
		Start: &now,
		End:   nil,
	}

	slices = append(slices, slice)

	if errSerialize := serialize(ctxFileName, slices); errSerialize != nil {
		fmt.Printf("%s", errSerialize)
		return
	}

	fmt.Printf("You're working on %s", ctxFileName)
}

func info(c *cli.Context) {
	ctxFileName := os.ExpandEnv(c.GlobalString("ctxfile"))

	slices, err := deserialize(ctxFileName)
	if err != nil {
		fmt.Printf("%s", err)
		return
	}

	if len(slices) == 0 {
		fmt.Println("You have not started a context")
		return
	}

	var duration time.Duration

	for _, slice := range slices {
		if slice.IsComplete() {
			duration += slice.Duration()
		}
	}

	lastSlice := slices[len(slices)-1]
	if !lastSlice.IsComplete() {
		now := time.Now()
		duration += now.Sub(*lastSlice.Start)
	}

	fmt.Println(duration)
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
