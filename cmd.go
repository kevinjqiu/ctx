package main

import (
	"fmt"
	"github.com/codegangsta/cli"
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
	contextId := c.Args()[0]
	// TODO: error if arg not provided
	storage, err := NewStorage(os.ExpandEnv(c.GlobalString("ctxfile")))

	if err != nil {
		// TODO: nicer error message
		panic(err)
	}

	// now := time.Now()
	// slice := TimeSlice{
	//     Start: &now,
	//     End:   nil,
	// }

	err = storage.SwitchContext(contextId)

	// slices = append(slices, slice)

	// if errSerialize := serialize(ctxFileName, slices); errSerialize != nil {
	//     fmt.Printf("%s", errSerialize)
	//     return
	// }

	if err != nil {
		fmt.Printf("%s", err)
		return
	}

	fmt.Printf("You're working on %s", contextId)
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
