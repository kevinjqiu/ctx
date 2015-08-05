package main

import (
	"fmt"
	"github.com/codegangsta/cli"
	"io/ioutil"
	"os"
	"strconv"
	"time"
)

func newContext(c *cli.Context) {
	localFileName := os.ExpandEnv("${HOME}/.ctx")
	now := time.Now()
	ioutil.WriteFile(localFileName, []byte(strconv.FormatInt(now.UnixNano(), 10)), 0644)
}

func info(c *cli.Context) {
	localFileName := os.ExpandEnv("${HOME}/.ctx")
	now := time.Now()
	content, e1 := ioutil.ReadFile(localFileName)
	if e1 != nil {
		fmt.Printf("Cannot read %s", localFileName)
		return
	}

	then, e2 := strconv.ParseUint(string(content), 10, 64)
	if e2 != nil {
		fmt.Printf("Cannot convert %s to a timestamp", content)
		return
	}

	duration := time.Duration(uint64(now.UnixNano()) - then)

	fmt.Println(duration)
}

func main() {
	app := cli.NewApp()
	app.Name = "ctx"
	app.Usage = "CLI command to manage your working context"
	app.Commands = []cli.Command{
		{
			Name:    "new",
			Aliases: []string{"n"},
			Action:  newContext,
		},
		{
			Name:    "info",
			Aliases: []string{"i"},
			Action:  info,
		},
	}
	app.Run(os.Args)
}
