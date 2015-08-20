package main

import (
	"github.com/fatih/color"
)

var green func(a ...interface{}) string

var red func(a ...interface{}) string

func init() {
	green = color.New(color.FgGreen).SprintFunc()
	red = color.New(color.FgRed).SprintFunc()
}
