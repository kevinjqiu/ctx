package main

import (
	"fmt"
	"github.com/codegangsta/cli"
	"os"
	"strconv"
	"time"
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

	fmt.Printf("You're working on %s", green(contextId))
}

func fmtDuration(duration time.Duration) string {
	return fmt.Sprintf("%sm", strconv.FormatInt(int64(duration/time.Minute), 10))
}

func info(c *cli.Context) {
	storage := getRequestedStorage(c)
	context := storage.GetCurrentContext()

	fmt.Printf("%10s    %5s    %10s", context.Id, fmtDuration(context.GetTotalDuration()), contextStatusString(context))
}

func list(c *cli.Context) {
	storage := getRequestedStorage(c)
	for _, contextId := range storage.GetContextIds() {
		context := storage.GetContextById(contextId)
		fmt.Printf("%s    %s\n", contextId, contextStatusString(context))
	}
}

func contextStatusString(context *Context) string {
	if context.IsStopped() {
		return red("Stopped")
	} else {
		return green("Active")
	}
}
