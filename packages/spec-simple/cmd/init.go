package cmd

import (
	"encoding/json"
	"fmt"
	"io/fs"
	"os"
	"os/exec"
	"path/filepath"

	"github.com/fatih/color"
	"github.com/letsur/spec-kit/packages/spec-simple/internal/templates"
	"github.com/spf13/cobra"
)

var (
	flagHere  bool
	flagNoGit bool
	flagForce bool
)

func init() {
	initCmd.Flags().BoolVar(&flagHere, "here", false, "Initialize in current directory (same as '.')")
	initCmd.Flags().BoolVar(&flagNoGit, "no-git", false, "Skip git initialization")
	initCmd.Flags().BoolVarP(&flagForce, "force", "f", false, "Overwrite existing files")
	rootCmd.AddCommand(initCmd)
}

var initCmd = &cobra.Command{
	Use:   "init [project-name]",
	Short: "Initialize a new spec-simple project",
	Long:  "Initialize a new spec-simple project with slash commands and templates.",
	Args:  cobra.MaximumNArgs(1),
	RunE:  runInit,
}

func runInit(cmd *cobra.Command, args []string) error {
	green := color.New(color.FgGreen).SprintFunc()
	red := color.New(color.FgRed).SprintFunc()
	yellowFn := color.New(color.FgYellow).SprintFunc()
	bold := color.New(color.Bold).SprintFunc()
	dim := color.New(color.Faint).SprintFunc()

	// Determine project name
	projectName := "."
	if len(args) > 0 {
		projectName = args[0]
	}

	// Determine target directory
	var targetDir string
	if flagHere || projectName == "." {
		cwd, err := os.Getwd()
		if err != nil {
			return fmt.Errorf("failed to get current directory: %w", err)
		}
		targetDir = cwd
	} else {
		if filepath.IsAbs(projectName) {
			targetDir = projectName
		} else {
			cwd, err := os.Getwd()
			if err != nil {
				return fmt.Errorf("failed to get current directory: %w", err)
			}
			targetDir = filepath.Join(cwd, projectName)
		}

		// Check if directory exists and is not empty
		if !flagForce {
			entries, err := os.ReadDir(targetDir)
			if err == nil && len(entries) > 0 {
				fmt.Fprintf(os.Stderr, "%s Directory '%s' already exists and is not empty. Use --force to overwrite.\n", red("✗"), projectName)
				os.Exit(1)
			}
		}
		if err := os.MkdirAll(targetDir, 0755); err != nil {
			return fmt.Errorf("failed to create directory: %w", err)
		}
	}

	// Check for existing .spec-simple
	specDir := filepath.Join(targetDir, ".spec-simple")
	if !flagForce {
		if _, err := os.Stat(specDir); err == nil {
			fmt.Fprintf(os.Stderr, "%s Project already initialized. Use --force to reinitialize.\n", red("✗"))
			os.Exit(1)
		}
	}

	// Copy slash commands to .claude/commands/
	claudeCmdsDir := filepath.Join(targetDir, ".claude", "commands")
	if err := os.MkdirAll(claudeCmdsDir, 0755); err != nil {
		return fmt.Errorf("failed to create .claude/commands: %w", err)
	}
	if err := copyEmbedDir(templates.FS, "commands", claudeCmdsDir); err != nil {
		return fmt.Errorf("failed to copy commands: %w", err)
	}

	// Copy doc templates to .spec-simple/templates/
	specTemplatesDir := filepath.Join(specDir, "templates")
	if err := os.MkdirAll(specTemplatesDir, 0755); err != nil {
		return fmt.Errorf("failed to create .spec-simple/templates: %w", err)
	}
	if err := copyEmbedDir(templates.FS, "docs", specTemplatesDir); err != nil {
		return fmt.Errorf("failed to copy templates: %w", err)
	}

	// Write config.json
	config := map[string]string{"version": version}
	configBytes, _ := json.MarshalIndent(config, "", "  ")
	if err := os.WriteFile(filepath.Join(specDir, "config.json"), append(configBytes, '\n'), 0644); err != nil {
		return fmt.Errorf("failed to write config.json: %w", err)
	}

	// Create specs directory
	if err := os.MkdirAll(filepath.Join(targetDir, "specs"), 0755); err != nil {
		return fmt.Errorf("failed to create specs/: %w", err)
	}

	// Git init
	gitOk := false
	if !flagNoGit {
		gitOk = initGit(targetDir, yellowFn)
	}

	// Summary
	displayName := projectName
	if projectName == "." {
		displayName = filepath.Base(targetDir)
	}

	fmt.Println()
	fmt.Println(green("╭─") + " " + bold("spec-simple"))
	fmt.Println(green("│"))
	fmt.Println(green("│") + "  " + bold("Project initialized: "+displayName))
	fmt.Println(green("│"))
	fmt.Println(green("│") + "  " + green("✓") + " .claude/commands/  (3 slash commands)")
	fmt.Println(green("│") + "  " + green("✓") + " .spec-simple/      (config + templates)")
	fmt.Println(green("│") + "  " + green("✓") + " specs/              (feature specs)")
	if gitOk {
		fmt.Println(green("│") + "  " + green("✓") + " .git/               (initialized)")
	}
	fmt.Println(green("│"))
	fmt.Println(green("│") + "  " + dim("Next: Run /spec-simple.specify in Claude Code"))
	fmt.Println(green("╰─"))
	fmt.Println()

	return nil
}

func copyEmbedDir(embedFS fs.FS, srcDir, destDir string) error {
	return fs.WalkDir(embedFS, srcDir, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if d.IsDir() {
			return nil
		}
		data, err := fs.ReadFile(embedFS, path)
		if err != nil {
			return err
		}
		destPath := filepath.Join(destDir, d.Name())
		return os.WriteFile(destPath, data, 0644)
	})
}

func initGit(targetDir string, yellowFn func(a ...interface{}) string) bool {
	_, err := exec.LookPath("git")
	if err != nil {
		fmt.Println(yellowFn("⚠") + " git not found, skipping git init")
		return false
	}

	gitDir := filepath.Join(targetDir, ".git")
	if _, err := os.Stat(gitDir); err == nil {
		return true
	}

	gitCmd := exec.Command("git", "init")
	gitCmd.Dir = targetDir
	gitCmd.Stdout = nil
	gitCmd.Stderr = nil
	if err := gitCmd.Run(); err != nil {
		fmt.Println(yellowFn("⚠") + " git init failed")
		return false
	}
	return true
}
