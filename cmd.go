package main

import (
	"fmt"
	"github.com/codegangsta/cli"
	"os"
)

func getRequestedStorage(c *cli.Context) *Storage {
	storage, err := NewStorage(os.ExpandEnv(c.GlobalString("ctxfile")))

	if err != nil {
		panic(err)
	}
	return storage
}

func stopContext(c *cli.Context) {
	storage := getRequestedStorage(c)

	currentContext := storage.GetCurrentContext()

	if currentContext == nil {
		fmt.Println("No current context. Start a context first!")
		return
	}

	currentContext.Stop()
	storage.Save()
}

func switchContext(c *cli.Context) {
	if len(c.Args()) != 1 {
		fmt.Println("You must provide the id of the context")
		return
	}

	contextId := c.Args()[0]
	storage := getRequestedStorage(c)

	err := storage.SwitchContext(contextId)

	if err != nil {
		fmt.Printf("%s", err)
		return
	}

	fmt.Printf("You're working on %s", contextId)
}

func info(c *cli.Context) {
	storage := getRequestedStorage(c)
	context := storage.GetCurrentContext()
	fmt.Printf("%s\t%s", context.Id, context.GetTotalDuration().String())
}
