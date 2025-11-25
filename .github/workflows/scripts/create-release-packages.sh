#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh (workflow-local)
# Build Spec Kit template release archives for each supported AI assistant and script type.
# Usage: .github/workflows/scripts/create-release-packages.sh <version>
#   Version argument should include leading 'v'.
#   Optionally set AGENTS and/or SCRIPTS env vars to limit what gets built.
#     AGENTS  : space or comma separated subset of: claude gemini copilot cursor-agent qwen opencode windsurf codex amp (default: all)
#     SCRIPTS : space or comma separated subset of: sh ps (default: both)
#   Examples:
#     AGENTS=claude SCRIPTS=sh $0 v0.2.0
#     AGENTS="copilot,gemini" $0 v0.2.0
#     SCRIPTS=ps $0 v0.2.0

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version-with-v-prefix>" >&2
  exit 1
fi
NEW_VERSION="$1"
# Support semantic versioning with pre-release tags (e.g., v1.0.0-alpha.1, v1.0.0-beta, v1.0.0-rc.1)
if [[ ! $NEW_VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?(\+[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?$ ]]; then
  echo "Version must look like v0.0.0 or v0.0.0-alpha.1 (semantic versioning)" >&2
  exit 1
fi

echo "Building release packages for $NEW_VERSION"

# Create and use .genreleases directory for all build artifacts
GENRELEASES_DIR=".genreleases"
mkdir -p "$GENRELEASES_DIR"
rm -rf "$GENRELEASES_DIR"/* || true

rewrite_paths() {
  sed -E \
    -e 's@(/?)scripts/@.spec-mix/scripts/@g' \
    -e 's@(/?)templates/@.spec-mix/templates/@g'
}

generate_commands() {
  local agent=$1 ext=$2 arg_format=$3 output_dir=$4 script_variant=$5
  mkdir -p "$output_dir"

  # Try new mission structure first, fall back to old structure
  local command_dir=""
  if [[ -d "src/specmix/locales/en/missions/software-dev/commands" ]]; then
    command_dir="src/specmix/locales/en/missions/software-dev/commands"
  elif [[ -d "templates/commands" ]]; then
    command_dir="templates/commands"
  else
    echo "Warning: No command directory found" >&2
    return
  fi

  for template in "$command_dir"/*.md; do
    [[ -f "$template" ]] || continue
    local name description script_command agent_script_command body
    name=$(basename "$template" .md)
    
    # Normalize line endings
    file_content=$(tr -d '\r' < "$template")
    
    # Extract description and script command from YAML frontmatter
    description=$(printf '%s\n' "$file_content" | awk '/^description:/ {sub(/^description:[[:space:]]*/, ""); print; exit}')
    script_command=$(printf '%s\n' "$file_content" | awk -v sv="$script_variant" '/^[[:space:]]*'"$script_variant"':[[:space:]]*/ {sub(/^[[:space:]]*'"$script_variant"':[[:space:]]*/, ""); print; exit}')
    
    if [[ -z $script_command ]]; then
      echo "Warning: no script command found for $script_variant in $template" >&2
      script_command="(Missing script command for $script_variant)"
    fi
    
    # Extract agent_script command from YAML frontmatter if present
    agent_script_command=$(printf '%s\n' "$file_content" | awk '
      /^agent_scripts:$/ { in_agent_scripts=1; next }
      in_agent_scripts && /^[[:space:]]*'"$script_variant"':[[:space:]]*/ {
        sub(/^[[:space:]]*'"$script_variant"':[[:space:]]*/, "")
        print
        exit
      }
      in_agent_scripts && /^[a-zA-Z]/ { in_agent_scripts=0 }
    ')
    
    # Replace {SCRIPT} placeholder with the script command
    body=$(printf '%s\n' "$file_content" | sed "s|{SCRIPT}|${script_command}|g")
    
    # Replace {AGENT_SCRIPT} placeholder with the agent script command if found
    if [[ -n $agent_script_command ]]; then
      body=$(printf '%s\n' "$body" | sed "s|{AGENT_SCRIPT}|${agent_script_command}|g")
    fi
    
    # Remove the scripts: and agent_scripts: sections from frontmatter while preserving YAML structure
    body=$(printf '%s\n' "$body" | awk '
      /^---$/ { print; if (++dash_count == 1) in_frontmatter=1; else in_frontmatter=0; next }
      in_frontmatter && /^scripts:$/ { skip_scripts=1; next }
      in_frontmatter && /^agent_scripts:$/ { skip_scripts=1; next }
      in_frontmatter && /^[a-zA-Z].*:/ && skip_scripts { skip_scripts=0 }
      in_frontmatter && skip_scripts && /^[[:space:]]/ { next }
      { print }
    ')
    
    # Apply other substitutions
    body=$(printf '%s\n' "$body" | sed "s/{ARGS}/$arg_format/g" | sed "s/__AGENT__/$agent/g" | rewrite_paths)
    
    # Check if name already starts with spec-mix.
    if [[ "$name" == spec-mix.* ]]; then
      output_filename="$name.$ext"
    else
      output_filename="spec-mix.$name.$ext"
    fi

    case $ext in
      toml)
        body=$(printf '%s\n' "$body" | sed 's/\\/\\\\/g')
        { echo "description = \"$description\""; echo; echo "prompt = \"\"\""; echo "$body"; echo "\"\"\""; } > "$output_dir/$output_filename" ;;
      md)
        echo "$body" > "$output_dir/$output_filename" ;;
      prompt.md)
        echo "$body" > "$output_dir/$output_filename" ;;
    esac
  done
}

build_variant() {
  local agent=$1 script=$2
  local base_dir="$GENRELEASES_DIR/sdd-${agent}-package-${script}"
  echo "Building $agent ($script) package..."
  mkdir -p "$base_dir"
  
  # Copy base structure but filter scripts by variant
  SPEC_DIR="$base_dir/.spec-mix"
  mkdir -p "$SPEC_DIR"

  # Only copy the relevant script variant directory
  if [[ -d scripts ]]; then
    mkdir -p "$SPEC_DIR/scripts"
    case $script in
      sh)
        [[ -d scripts/bash ]] && { cp -r scripts/bash "$SPEC_DIR/scripts/"; echo "Copied scripts/bash -> .spec-mix/scripts"; }
        # Copy any script files that aren't in variant-specific directories
        find scripts -maxdepth 1 -type f -exec cp {} "$SPEC_DIR/scripts/" \; 2>/dev/null || true
        ;;
      ps)
        [[ -d scripts/powershell ]] && { cp -r scripts/powershell "$SPEC_DIR/scripts/"; echo "Copied scripts/powershell -> .spec-mix/scripts"; }
        # Copy any script files that aren't in variant-specific directories
        find scripts -maxdepth 1 -type f -exec cp {} "$SPEC_DIR/scripts/" \; 2>/dev/null || true
        ;;
    esac
  fi
  
  # Copy templates from mission structure or old structure
  if [[ -d "src/specmix/locales/en/missions/software-dev/templates" ]]; then
    mkdir -p "$SPEC_DIR/active-mission/templates"
    cp src/specmix/locales/en/missions/software-dev/templates/*.md "$SPEC_DIR/active-mission/templates/" 2>/dev/null || true
    echo "Copied mission templates -> .spec-mix/active-mission/templates"

    # Also copy mission constitution if exists
    if [[ -d "src/specmix/locales/en/missions/software-dev/constitution" ]]; then
      mkdir -p "$SPEC_DIR/active-mission/constitution"
      cp -r src/specmix/locales/en/missions/software-dev/constitution/* "$SPEC_DIR/active-mission/constitution/" 2>/dev/null || true
    fi

    # Set active mission
    echo "software-dev" > "$SPEC_DIR/active-mission.txt"
  elif [[ -d templates ]]; then
    mkdir -p "$SPEC_DIR/templates"
    find templates -type f -not -path "templates/commands/*" -not -name "vscode-settings.json" -exec cp --parents {} "$SPEC_DIR"/ \;
    echo "Copied templates -> .spec-mix/templates"
  fi
  
  # NOTE: We substitute {ARGS} internally. Outward tokens differ intentionally:
  #   * Markdown/prompt (claude, copilot, cursor-agent, opencode): $ARGUMENTS
  #   * TOML (gemini, qwen): {{args}}
  # This keeps formats readable without extra abstraction.

  # Generate commands in active-mission directory first
  mkdir -p "$SPEC_DIR/active-mission/commands"
  generate_commands generic md "\$ARGUMENTS" "$SPEC_DIR/active-mission/commands" "$script"

  case $agent in
    claude)
      mkdir -p "$base_dir/.claude/commands"
      # Copy from active-mission instead of regenerating
      cp "$SPEC_DIR/active-mission/commands"/*.md "$base_dir/.claude/commands/" 2>/dev/null || true ;;
    gemini)
      mkdir -p "$base_dir/.gemini/commands"
      # Gemini supports .md format same as claude
      cp "$SPEC_DIR/active-mission/commands"/*.md "$base_dir/.gemini/commands/" 2>/dev/null || true
      [[ -f agent_templates/gemini/GEMINI.md ]] && cp agent_templates/gemini/GEMINI.md "$base_dir/GEMINI.md" ;;
    copilot)
      mkdir -p "$base_dir/.github/prompts"
      generate_commands copilot prompt.md "\$ARGUMENTS" "$base_dir/.github/prompts" "$script"
      # Create VS Code workspace settings
      mkdir -p "$base_dir/.vscode"
      [[ -f templates/vscode-settings.json ]] && cp templates/vscode-settings.json "$base_dir/.vscode/settings.json"
      ;;
    cursor-agent)
      mkdir -p "$base_dir/.cursor/commands"
      cp "$SPEC_DIR/active-mission/commands"/*.md "$base_dir/.cursor/commands/" 2>/dev/null || true ;;
    qwen)
      mkdir -p "$base_dir/.qwen/commands"
      generate_commands qwen toml "{{args}}" "$base_dir/.qwen/commands" "$script"
      [[ -f agent_templates/qwen/QWEN.md ]] && cp agent_templates/qwen/QWEN.md "$base_dir/QWEN.md" ;;
    opencode)
      mkdir -p "$base_dir/.opencode/command"
      cp "$SPEC_DIR/active-mission/commands"/*.md "$base_dir/.opencode/command/" 2>/dev/null || true ;;
    windsurf)
      mkdir -p "$base_dir/.windsurf/workflows"
      cp "$SPEC_DIR/active-mission/commands"/*.md "$base_dir/.windsurf/workflows/" 2>/dev/null || true ;;
    codex)
      mkdir -p "$base_dir/.codex/prompts"
      cp "$SPEC_DIR/active-mission/commands"/*.md "$base_dir/.codex/prompts/" 2>/dev/null || true ;;
    kilocode)
      mkdir -p "$base_dir/.kilocode/workflows"
      cp "$SPEC_DIR/active-mission/commands"/*.md "$base_dir/.kilocode/workflows/" 2>/dev/null || true ;;
    auggie)
      mkdir -p "$base_dir/.augment/commands"
      cp "$SPEC_DIR/active-mission/commands"/*.md "$base_dir/.augment/commands/" 2>/dev/null || true ;;
    roo)
      mkdir -p "$base_dir/.roo/commands"
      cp "$SPEC_DIR/active-mission/commands"/*.md "$base_dir/.roo/commands/" 2>/dev/null || true ;;
    codebuddy)
      mkdir -p "$base_dir/.codebuddy/commands"
      cp "$SPEC_DIR/active-mission/commands"/*.md "$base_dir/.codebuddy/commands/" 2>/dev/null || true ;;
    amp)
      mkdir -p "$base_dir/.agents/commands"
      cp "$SPEC_DIR/active-mission/commands"/*.md "$base_dir/.agents/commands/" 2>/dev/null || true ;;
    q)
      mkdir -p "$base_dir/.amazonq/prompts"
      cp "$SPEC_DIR/active-mission/commands"/*.md "$base_dir/.amazonq/prompts/" 2>/dev/null || true ;;
    antigravity)
      mkdir -p "$base_dir/.agent/workflows"
      cp "$SPEC_DIR/active-mission/commands"/*.md "$base_dir/.agent/workflows/" 2>/dev/null || true ;;
  esac
  ( cd "$base_dir" && zip -r "../spec-mix-template-${agent}-${script}-${NEW_VERSION}.zip" . )
  echo "Created $GENRELEASES_DIR/spec-mix-template-${agent}-${script}-${NEW_VERSION}.zip"
}

# Determine agent list
ALL_AGENTS=(claude gemini copilot cursor-agent qwen opencode windsurf codex kilocode auggie roo codebuddy amp q antigravity)
ALL_SCRIPTS=(sh ps)

norm_list() {
  # convert comma+space separated -> space separated unique while preserving order of first occurrence
  tr ',\n' '  ' | awk '{for(i=1;i<=NF;i++){if(!seen[$i]++){printf((out?" ":"") $i)}}}END{printf("\n")}'
}

validate_subset() {
  local type=$1; shift; local -n allowed=$1; shift; local items=("$@")
  local ok=1
  for it in "${items[@]}"; do
    local found=0
    for a in "${allowed[@]}"; do [[ $it == "$a" ]] && { found=1; break; }; done
    if [[ $found -eq 0 ]]; then
      echo "Error: unknown $type '$it' (allowed: ${allowed[*]})" >&2
      ok=0
    fi
  done
  return $ok
}

if [[ -n ${AGENTS:-} ]]; then
  mapfile -t AGENT_LIST < <(printf '%s' "$AGENTS" | norm_list)
  validate_subset agent ALL_AGENTS "${AGENT_LIST[@]}" || exit 1
else
  AGENT_LIST=("${ALL_AGENTS[@]}")
fi

if [[ -n ${SCRIPTS:-} ]]; then
  mapfile -t SCRIPT_LIST < <(printf '%s' "$SCRIPTS" | norm_list)
  validate_subset script ALL_SCRIPTS "${SCRIPT_LIST[@]}" || exit 1
else
  SCRIPT_LIST=("${ALL_SCRIPTS[@]}")
fi

echo "Agents: ${AGENT_LIST[*]}"
echo "Scripts: ${SCRIPT_LIST[*]}"

for agent in "${AGENT_LIST[@]}"; do
  for script in "${SCRIPT_LIST[@]}"; do
    build_variant "$agent" "$script"
  done
done

echo "Archives in $GENRELEASES_DIR:"
ls -1 "$GENRELEASES_DIR"/spec-mix-template-*-"${NEW_VERSION}".zip

