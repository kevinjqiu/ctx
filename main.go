package main

import (
	"os"

	"github.com/codegangsta/cli"
)

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
			Aliases: []string{"s, sw, start"},
			Action:  switchContext,
		},
		{
			Name:    "info",
			Aliases: []string{"i"},
			Action:  info,
		},
		{
			Name:    "title",
			Aliases: []string{"t"},
			Action:  editTitle,
		},
		{
			Name:    "stop",
			Aliases: []string{"st"},
			Action:  stopContext,
		},
		{
			Name:    "list",
			Aliases: []string{"l"},
			Action:  list,
		},
	}
	app.Run(os.Args)
}
