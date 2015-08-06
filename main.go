package main

import (
	"encoding/json"
	"fmt"
	"github.com/codegangsta/cli"
	"io/ioutil"
	"os"
	"time"
)

type TimeSlice struct {
	Start *time.Time `json:"start"`
	End   *time.Time `json:"end"`
}

const InvalidDuration = time.Duration(-1)

func (timeSlice *TimeSlice) Duration() time.Duration {
	if timeSlice.Start == nil {
		return InvalidDuration
	}
	if timeSlice.End == nil {
		return InvalidDuration
	}

	return timeSlice.End.Sub(*timeSlice.Start)
}

func (timeSlice *TimeSlice) IsComplete() bool {
	return timeSlice.End != nil
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

func switchContext(c *cli.Context) {
	ctxFileName := os.ExpandEnv(c.GlobalString("ctxfile"))

	now := time.Now()
	slice := TimeSlice{
		Start: &now,
		End:   nil,
	}
	sliceJson, errMarshal := json.Marshal(slice)
	if errMarshal != nil {
		fmt.Println("Cannot serialize to JSON: %s", errMarshal)
		return
	}

	err := ioutil.WriteFile(ctxFileName, sliceJson, 0644)

	if err != nil {
		fmt.Println("Cannot write %s: %s", ctxFileName, err)
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

func main() {
	app := cli.NewApp()
	app.Name = "ctx"
	app.Usage = "CLI command to manage your working context"
	app.Flags = []cli.Flag{
		cli.StringFlag{
			Name:  "ctxfile,f",
			Value: "${HOME}/.ctx",
			Usage: "Path to the context file",
		},
	}

	app.Commands = []cli.Command{
		{
			Name:    "switch",
			Aliases: []string{"s"},
			Action:  switchContext,
		},
		{
			Name:    "info",
			Aliases: []string{"i"},
			Action:  info,
		},
	}
	app.Run(os.Args)
}
