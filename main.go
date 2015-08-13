package main

import (
	"github.com/codegangsta/cli"
	"os"
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
			Aliases: []string{"s"},
			Action:  switchContext,
		},
		{
			Name:    "info",
			Aliases: []string{"i"},
			Action:  info,
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
