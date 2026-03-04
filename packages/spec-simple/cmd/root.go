package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var version = "dev"

var rootCmd = &cobra.Command{
	Use:   "spec-simple",
	Short: "Simplified SDD toolkit for Claude Code",
	Long:  "spec-simple — A single-binary CLI that bootstraps Spec-Driven Development projects for Claude Code.",
}

func init() {
	rootCmd.AddCommand(versionCmd)
}

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Print the version number",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("spec-simple", version)
	},
}

func Execute() {
	rootCmd.Version = version
	rootCmd.SetVersionTemplate("spec-simple {{.Version}}\n")
	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}
