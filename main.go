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
	Start time.Time `json:"start"`
	End   time.Time `json:"end"`
}

func switchContext(c *cli.Context) {
	ctxFileName := os.ExpandEnv(c.GlobalString("ctxfile"))
	now := time.Now()
	slice := TimeSlice{
		Start: now,
		End:   time.Time{},
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

	content, errReadFile := ioutil.ReadFile(ctxFileName)
	if errReadFile != nil {
		fmt.Printf("Cannot read %s", ctxFileName)
		return
	}

	var slice TimeSlice
	if errUnmarshal := json.Unmarshal(content, &slice); errUnmarshal != nil {
		fmt.Printf("%s", errUnmarshal)
		return
	}

	now := time.Now()
	duration := now.Sub(slice.Start)
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
