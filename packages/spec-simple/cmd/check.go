package cmd

import (
	"fmt"
	"os"
	"os/exec"

	"github.com/fatih/color"
	"github.com/spf13/cobra"
)

func init() {
	rootCmd.AddCommand(checkCmd)
}

var checkCmd = &cobra.Command{
	Use:   "check",
	Short: "Check required tools are installed",
	RunE:  runCheck,
}

func runCheck(cmd *cobra.Command, args []string) error {
	green := color.New(color.FgGreen).SprintFunc()
	red := color.New(color.FgRed).SprintFunc()
	dim := color.New(color.Faint).SprintFunc()
	bold := color.New(color.Bold).SprintFunc()

	fmt.Println(bold("spec-simple prerequisites"))
	fmt.Println()

	type tool struct {
		name string
		desc string
	}

	tools := []tool{
		{"git", "Version control"},
		{"claude", "Claude Code CLI"},
	}

	allOk := true
	for _, t := range tools {
		path, err := exec.LookPath(t.name)
		if err == nil {
			fmt.Printf("  %s %s — %s %s\n", green("✓"), t.name, t.desc, dim("("+path+")"))
		} else {
			fmt.Printf("  %s %s — %s %s\n", red("✗"), t.name, t.desc, red("(not found)"))
			allOk = false
		}
	}

	fmt.Println()
	if allOk {
		fmt.Println(green("All prerequisites met."))
	} else {
		fmt.Println(color.YellowString("Some tools are missing."))
		os.Exit(1)
	}
	return nil
}
