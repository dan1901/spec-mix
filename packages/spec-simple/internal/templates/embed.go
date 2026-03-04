package templates

import "embed"

//go:embed commands/* docs/*
var FS embed.FS
