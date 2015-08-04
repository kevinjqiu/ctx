package main

import (
	"github.com/codegangsta/cli"
	"net/http"
	"os"
)

func handler(w http.ResponseWriter, r *http.Request) {
}

func startServer(c *cli.Context) {
	http.HandleFunc("/", handler)
	http.ListenAndServe(":8080", nil)
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
	app.Run(os.Args)
}
