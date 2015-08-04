package main

import (
	_ "github.com/codegangsta/cli"
)

func startServer(c *cli.Context) {
}

func newContext(c *cli.Context) {
}

func info(c *cli.Context) {
}

func main() {
	app := cli.NewApp()
	app.Name = "ctx"
	app.Usage = "CLI command to manage your working context"
	app.Commands = []cli.Command{
		{
			Name:    "start",
			Aliases: []string{"s"},
			Action:  startServer,
		},
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
}
