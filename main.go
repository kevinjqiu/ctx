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
	ctxFileName := os.ExpandEnv(c.GlobalString("ctxfile"))
	now := time.Now()
	ioutil.WriteFile(ctxFileName, []byte(strconv.FormatInt(now.UnixNano(), 10)), 0644)
}

func info(c *cli.Context) {
	ctxFileName := os.ExpandEnv(c.GlobalString("ctxfile"))
	now := time.Now()

	content, errReadFile := ioutil.ReadFile(ctxFileName)
	if errReadFile != nil {
		fmt.Printf("Cannot read %s", ctxFileName)
		return
	}

	then, errParseInt := strconv.ParseUint(string(content), 10, 64)
	if errParseInt != nil {
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
	app.Flags = []cli.Flag{
		cli.StringFlag{
			Name:  "ctxfile,f",
			Value: "${HOME}/.ctx",
			Usage: "Path to the context file",
		},
	}

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
