---
name: antigravity-docs
description: "Google Antigravity docs — agentic dev platform: desktop app 2.0, CLI, SDK, IDE, subagents, artifacts, permissions, skills, MCP, hooks, rules, workflows, sidecars, Agent Manager, Browser, enterprise plans, settings, FAQ. Triggers — antigravity, google antigravity, antigravity docs, antigravity 2.0, antigravity cli, antigravity sdk, antigravity ide, antigravity subagents, antigravity artifacts, antigravity permissions, antigravity mcp, antigravity hooks, antigravity skills, antigravity rules, antigravity workflows, antigravity sidecars, antigravity agent manager, antigravity browser, antigravity enterprise, antigravity settings, antigravity faq, antigravity install, antigravity worktree, antigravity slash commands, antigravity keyboard shortcuts."
---

## Home

# Welcome to Google Antigravity

## Choose Your Surface

Google Antigravity offers multiple product surfaces tailored to your specific development workflow. Select the interface that best fits your needs:

### Antigravity 2.0

Your standalone desktop command center for your agents. Start agents inside Projects, work across multiple workspaces and worktrees, and orchestrate complex tasks using parallel local subagents.

* **Key Features**: Asynchronous task management, Scheduled Tasks (Cron sidecars), and voice transcription.  
* **Get Started**: Read the [Getting Started Guide](/docs/getting-started)

### Antigravity CLI

The lightweight, keyboard-centric Terminal User Interface surface. It brings the same core agentic capabilities as the desktop app directly to your terminal workflow, making it perfect for fast interactions and SSH sessions.

* **Key Features**: High-speed prompt shortcuts, custom keybindings, and parallel subagent management.  
* **Get Started**: Explore the [CLI Quick Overview](/docs/cli-overview)

### Antigravity SDK

A programmatic Python framework for researchers and developers who want complete control over their agent deployments. Custom build an agent, register custom tools, and implement lifecycle hooks, all on top of the Antigravity Harness.

* **Key Features**: Declarative safety policies, inspect/decide/transform hooks, and programmatic subagent spawning.  
* **Get Started**: Review the [SDK Overview](/docs/sdk-overview)

### Antigravity IDE 

The fully-featured, AI-powered developer environment. Standardize your daily coding with powerful tightly integrated coding agents, deep context awareness, tools like MCP and skills, and more.

* **Get Started**: Read the [IDE Getting Started Guide](/docs/ide-getting-started)

### Core Agent Capabilities

Every Antigravity surface runs on a shared, highly-optimized agent harness co-trained with Gemini models:

* **Gemini 3.5 Flash**: Powering all local agents with SOTA speed, reasoning, and context window capacity.  
* **[Asynchronous Subagents](/docs/subagents)**: Allows the main agent to delegate parallel background tasks to concurrent subagents without blocking your flow.  
* **[Visual Artifacts](/docs/artifacts)**: Track and verify agent output (plans, code diffs, browser recordings) with high-fidelity visual reports, keeping you informed every step of the way.  
* **[Security by Design](/docs/permissions)**: Secure local execution via safe defaults, local proxying, and granular tool approval gates.  
* **[Google Integrations](/docs/build-with-google)**: We partner with product teams across Google to provide curated bundles of skills, MCP servers, and extensions that make building on Google platforms frictionless.  
  * **Android**: Editor extension, CLI integrations, and Android developer skills.  
  * **Firebase**: Curated skills for Firebase Firestore, Cloud Functions, and more.  
  * **Web**: Chrome and Web MCP servers for autonomous browser research.  
  * **Science**: Specialized DeepMind biology and chemistry skills to accelerate scientific workflows.  
  * **AGY SDK**: Skills that optimize your agent’s ability to use the Antigravity SDK to build custom AI agents tailored to your workflow.

---

## Antigravity 2.0

# Antigravity 2.0

## Overview

As we go deeper into the agent-first era, Antigravity is evolving to further empower developers. Introducing Antigravity 2.0, a standalone desktop application tailored for managing AI agents that execute complex knowledge and coding tasks.

### What is Antigravity 2.0?

Antigravity 2.0 serves as your AI agents' central command center, providing a unified platform to launch, monitor, and orchestrate their activities. Unlike its predecessor, the Agent Manager, Antigravity 2.0 is a standalone application that functions independently of an IDE.

Within this interface, you can orchestrate agents both synchronously and asynchronously to:

* Execute system commands  
* Perform file read/write operations  
* Conduct web searches  
* Integrate with external tools via skills and MCP servers  
* Manage subagents  
* Interact with Chrome  
* Create artifacts / implementation plans

Whether you are performing deep research or building new applications, Antigravity offers a streamlined interface for all types of knowledge work.

![Antigravity 2.0 UI](assets/image/docs/AGY2.0-Home.png)

### Getting Started

Ready to dive in? Check out the **[Getting Started](/docs/getting-started)** guide to install Antigravity 2.0 and start your first project.

---

# Getting Started with Antigravity 2.0

### Download 

Visit [antigravity.google/download](https://antigravity.google/download) to download Google Antigravity 2.0. 

* **macOS**: macOS versions with Apple security update support. This is typically the current and two previous versions. Min Version 12 (Monterey), X86 is not supported.
* **Windows**: Windows 10 (64 bit)
* **Linux**: glibc >= 2.28, glibcxx >= 3.4.25 (e.g. Ubuntu 20, Debian 10, Fedora 36, RHEL 8)

### Installation

You may get a notification asking whether you want to “Keep Both” or “Replace” Antigravity, select “Replace.” You will be prompted to re-install the IDE during installation, should you choose to. If you do not install it now and would like to re-download it later, you can do so [here](/download).

### Creating a Project

Agents work within Projects, which define the boundaries of the folders and repositories they can access.

1. Click the **folder with a "+" icon** in the **left sidebar**.
2. Click on **"New Project"**.
3. Click **Add Folder** to associate one or more local folders or Git repositories. Adding multiple folders provides your agent with full cross-repository context.
4. Click **Create**.
5. *(Optional)* Configure your Project's settings. Each Project maintains its own isolated settings and security policies that the agent respects.


### Starting an Agent

Once your Project is created, you can spawn an agent to start working on tasks.

1. Type your goal or instruction in the chat input (e.g., "Help me add a new feature") and press **Enter**.
2. Choose a **Mode** in the setup modal to boot up your agent:
   * **Local Mode**: The agent operates directly in your active folders.
   * **New Worktree Mode**: The agent operates in an isolated Git worktree.

### Basic Navigation

| Action | macOS | Windows / Linux |
| :--- | :--- | :--- |
| **Open Conversation Picker** | `⌘K` | `Ctrl + K` |
| **Open File Search** | `⌘P` | `Ctrl + P` |
| **Focus Input** | `⌘L` | `Ctrl + L` |
| **New Conversation** | `⌘N` | `Ctrl + N` |
| **Next/Previous Conversation** | `⌥ Up / Down` | `Alt + Up / Down` |

### Slash Commands

* `/goal`: Run until the specified task is completely finished, not asking for intermediate input from the user.  
* `/grill-me`: Before starting to implement, ask questions back to align on the specific details of the plan.  
* `/schedule`: Run an instruction as a one-time timer in the future or on some recurring schedule (via Scheduled Tasks)  
* `/browser`: We heard the feedback that the agents were still not capable enough to determine exactly when to be using the browser. So for now, we’ve made it such that an explicit slash command controls these behaviors. When used, the agent diligently uses the browser primitives. This requires both Google Chrome and the user to provide permission in Google Chrome to start a debugging session.

---

# Build with Google

Antigravity 2.0 makes it seamless to build with popular Google technology stacks. We have partnered with teams across Google to create curated bundles of primitives, including Skills, MCP servers, and Editor extensions, that are pre-configured for specific ecosystems.

Instead of searching for individual tools, you can enable these bundles to instantly empower your agents with deep knowledge of Google platforms.

### How to Enable

You can enable "Build with Google" integrations at two points:

* **During Onboarding**: Select the checkboxes for the stacks you plan to use.  
* **In Settings**: Navigate to `Settings > Customizations > Build with Google Plugins` to add or remove integrations at any time.

### Available Bundles

### Modern Web Guidance

Keep your coding agent up to date with the latest web best practices.

* **What’s Included**: Package of evergreen and expert-vetted skills for modern web  
  * **Key Capabilities**: Agent can build accessible, performant, and secure web experiences using injected guidance  
  * **Learn more**: [Read the Modern Web Guidance](http://goo.gle/modern-web-guidance)

### Firebase Bundle

Transform your AI coding agent into a specialized Firebase expert that can write code, configure Firebase Security Rules, and manage live resources.

* **What's Included**:  
  * Package of agent skills for core Firebase services, including Firestore, Authentication, App Hosting, and more  
* **Key Capabilities**:  
  * **Take action**: Do more than just write code. Your agent can initialize services, manage Authentication users, deploy new Firebase Security Rules, and work directly with your Cloud Firestore data.  
  * **Stay up-to-date**: Use official, version-aware prompts to guide your agent through setup tasks.  
  * **Improve accuracy**: Access your project's environment and schemas to provide more relevant and accurate help.  
* **Learn More**: [Explore the Firebase Agent Skills Guide](https://firebase.google.com/docs/ai-assistance/agent-skills) 

### Google Antigravity SDK

Using the Antigravity Python SDK to build AI agents

* **What’s Included**:  
  * An agent skill containing architecture references, getting-started examples, and configuration guides for the Antigravity Python SDK (google-antigravity)  
* **Key Capabilities**:  
  * **Build agents**: Your agent can scaffold new Antigravity agents, configure models, register custom Python tools, and connect MCP servers using SDK best practices.  
  * **Stay safe**: Use official guidance to implement declarative safety policies, including deny-by-default templates and argument-level predicates.  
  * **Go deeper**: Access reference material for lifecycle hooks, multi-agent delegation, structured output, multimodal input, and token usage observability.  
* **Learn more**: [Visit the Antigravity SDK Repository](https://github.com/google-antigravity/antigravity-sdk-python)

### Android CLI

Core tools and knowledge required to develop for Android  

* **What’s included**: Android CLI and Android skills for core development tasks including making your UI edge-to-edge and adaptive, creating a testing framework, analyzing your R8 configuration to optimize performance, and more.  
* **Key capabilities**:  
  * Enable the agent of your choice to build high-quality Android apps   
  * Create new projects   
  * Deploy your app on an Android virtual device  
  * Test your app using natural language instructions   
  * Migrate to the latest versions of libraries and plugins  
* **Learn more**: [Explore the Android Agent Developer Tools](http://developer.android.com/tools/agents) 

### Science

Curated collection of agent skills for science.

* **What’s Included**: A high quality curated bundle of scientific skills   
* **Key Capabilities**: Improve agent capabilities on scientific workflows.  
* **Learn more**: [Review the DeepMind Science Skills Repository](https://github.com/google-deepmind/science-skills) 

### Chrome DevTools

Reliable automation, in-depth debugging, and performance analysis in Chrome using Chrome DevTools and Puppeteer

* **What’s Included**: Package of agent skills for Chrome DevTools and Puppeteer  
* **Key Capabilities**: Debugging accessibility (a11y) issues, auditing Core Web Vitals (LCP/INP), running visual automation tests, and diagnosing memory leaks.  
* **Learn more**: [Explore the Chrome DevTools Skills Repository](https://github.com/google/chrome-devtools-skills)

---

# Antigravity 2.0 Features

### Projects  

In Antigravity 2.0, agents work in **Projects** (previously in Agent Manager, agents were strictly mapped to a single workspace folder).

* **Worktree Support**: Projects natively support Git worktrees, allowing agents to operate in isolated background folders.  
* **Scoped Settings**: Settings are scoped, allowing you to have different security settings per project. This means you can have a more permissive setting for a trusted project and a more restrictive security setting for an untrusted folder. The main three presets are "Default", "Full machine" and "Unrestricted" (see the settings tab for the full list).  
* **Scoped Permissions**: Attach permission grants to projects to control what the agents are allowed to access. Permissions manually granted during a conversation can persist, allowing the agent to learn trusted actions and enabling a more seamless experience over time.  
* **Multi-Folder Access**: A project can be configured to work in multiple folders, allowing agents to operate across different codebases within the same conversation.  

### Conversations outside of projects

Start quick, one-off conversations outside of any Project. These sessions run in an isolated local scratch folder. They have their own settings, and they also have their own permissions in addition to inheriting from global permissions.

### Scheduled Tasks 

We’re introducing scheduled tasks, allowing users to plan ahead with their projects. Utilizing the newest Gemini 3.5 Flash model, users can schedule messages to be sent to their agents while they’re away.  

* **Repeatable**: Set up time-based triggers to start conversations periodically.  
* Tasks will be set to repeat on the minute you’ve set them.

### Secure by Default

We put you in the driver's seat with robust security controls:

* **Interactive Approvals**: By default, agents will request your explicit permission before running any terminal commands.  
* **Bounded Access**: By default, your agent can only read and write within the provided folders of a project. If you change your security preset to “Full Machine” or “Unrestricted”, the agent will have read and write access over your full machine.

### Voice transcription

Antigravity features a built-in live voice transcription, allowing you to prompt agents and leave feedback using natural speech.

**How to Use**:

* **Start/Stop**: Click the mic button next to the text input box to start recording, click it again to stop.  
* **Live View**: As you speak, your words are transcribed in real-time directly into the input field.  
* **Shortcut**: You can start recording by pressing `Ctrl + M`. Once you’re done, press `Ctrl + M` to stop recording.

**Key Features**

* **Smart Cleanup**: Speak naturally without worrying about pauses or perfect phrasing. Once you stop recording, the system automatically cleans up the transcription, resolving self-corrections, repetitions, and filler words into a cohesive prompt.  
* **Conversational Awareness**: The model will have context to your conversation, you can use project-specific terminology and expect accurate results. 

**Availability**  
Voice input is available across all primary interaction surfaces:

* **Agent Input**: For starting conversations and sending prompt updates.  
* **Artifact Comments**: For leaving precise, inline feedback on plans, code diffs, and deliverables.

### JSON Hooks

JSON Hooks allow you to execute custom local shell scripts at critical stages of an Antigravity agent's execution cycle. You can intercept and control the agent's behavior before tool calls, after model responses, or at loop stopping conditions—configured globally or per-workspace via simple JSON files.

[Explore the JSON Hooks & Rules Documentation](/docs/hooks)

### Browser

We reworked the browser subagent in Antigravity 2.0.

* **On-demand**: Can be invoked through the `/browser` command.  
* **Chrome DevTools integration**: The browser subagent also integrates natively with Chrome DevTools MCP.  
* **Video recording**: Now supports recordings as webm videos.

---

## Antigravity CLI

# Antigravity CLI Overview

The Antigravity CLI is the lightweight Terminal User Interface (TUI) surface of Antigravity. It brings the same core agentic capabilities as Antigravity 2.0—including multi-step reasoning, multi-file editing, tool calling, and conversation history—directly to your terminal.

The CLI is the ideal tool for keyboard-centric developers and remote SSH workflows, optimized for speed and low resource overhead.

### Philosophical Split: CLI vs. Antigravity 2.0

Antigravity CLI complements Antigravity 2.0 as a terminal-first alternative.

* **CLI**: Optimized for speed, keyboard efficiency, and low overhead.  
* **Antigravity 2.0**: Optimized for comprehensiveness, visual orchestration, and project management.

**Integration Features**

* **Shared Agent Harness**: Both products run on the same core agent engine. Any improvements to reasoning or tool use automatically apply to both.  
* **Shared Settings**: Core preferences and permissions are shared. Changing a setting in the CLI updates it in the Antigravity, and vice versa.  
* **Conversation Export**: While conversations are separate by default, you can easily export a CLI conversation to Antigravity 2.0 to continue with the agent-first interface.

### Getting Started & Migration

To install the CLI, follow the [Installation Guide](/docs/cli-getting-started).

### Migrating from Gemini CLI

If you are transitioning from Gemini CLI, the onboarding process supports a one-time import to automatically migrate your existing Gemini CLI extensions, skills, and settings. To learn more, read [Migrating from Gemini CLI](/docs/gcli-migration).

### Deep Dives & References

For detailed instructions on specific features, refer to the following guides:

* **[Getting Started](/docs/cli-getting-started)**: Details on silent keyring sign-in and remote SSH session auth.  
* **[Using AGY CLI](/docs/cli-using)**: Learn about slash commands, configuration settings, and default keybindings.  
* **[Features](/docs/cli-features)**: Learn how the agent delegates parallel background tasks, how to use fast-path approvals, and other advanced capabilities.  
* **[Tools & Extensions](/docs/plugins)**: Reference for installing, enabling, and managing third-party skills and MCP servers.

---

# Getting Started with Antigravity CLI

### Installation 

**Mac/Linux:**

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

**Windows PowerShell:**

```powershell
irm https://antigravity.google/cli/install.ps1 | iex
```

**Windows CMD:**

```cmd
curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd
```

### Authentication 

Antigravity CLI attempts to authenticate you silently using your operating system's secure keyring. If no saved session is found, it will fall back to a browser-based Google Sign-In.

* **Local Machine**: The CLI will automatically open your default browser to the Google Sign-In page.  
* **Remote / SSH Session**: The CLI will detect that you are in an SSH session and print a secure authorization URL. Copy this URL into your local browser to sign in, and then paste the resulting authorization code back into the CLI prompt.  
* **Logging Out**: To terminate your session and remove saved credentials, run the command `/logout`.

To login with your enterprise credentials, connect your GCP project as you onboard. For more information, visit the [Enterprise Documentation Page](/docs/enterprise).

---

# Using AGY CLI

### Settings 

Antigravity CLI provides a flexible configuration system to customize workspace behavior, safety restrictions, editor preferences, visual style, and performance.

* **Configuration File**: Stored in a plain JSON file `~/.gemini/antigravity-cli/settings.json`.  
* **Settings Panel**: Type `/config` or `/settings` to open a full-screen overlay menu listing all available options.  
  * Select a setting to open its list of options or a text input field.  
  * Immediately save your selection to the disk and return to the main list.  
* **Overrides**: Certain settings can be overridden at launch via CLI flags (e.g., `--sandbox` or `--dangerously-skip-permissions`).  
  * The settings menu will display an indicator showing where the override came from (e.g., *Sandbox Mode on overridden by `--sandbox`*).  
  * You can still edit the persistent setting on disk, but the current session will enforce the command-line override until restarted.

### Quick Tips 

| Action/Feature | Tip/Command |
| :--- | :--- |
| **Auto-complete to file paths** | `@` will trigger path suggestions |
| **Clear Prompt** | Type `esc esc` to clear your prompt box (when no streaming is active) |
| **Terminal Commands** | Use `!` at the start of your prompt to run terminal commands directly |
| **Help** | Type `?` to get help and list all slash commands |
| **Reduce Noise from Tool Calls** | Set verbosity to **low** in `/config` to minimize outputs from numerous tool calls |
| **Manage Permissions** | Control permissions via `/config` or `/permissions` |
| **Go Back in Conversation** | Use `/rewind` or `/undo` to rewind the conversation history |
| **Fork Conversation** | Use `/fork` to spin up a separate workspace and branch the conversation from an earlier point |
| **Clear Conversation** | Use `/clear` to clear the prompt and start a new conversation session |
| **Resume Conversation** | Use `/resume` to list and resume previous conversation logs |
| **Auto-Save Resume** | When you close the CLI, it automatically prints the exact command needed to resume that specific session |

### Keybindings 

AGY CLI allows for custom keybindings. You can edit them by typing `/keybindings` or modifying the JSON file directly.

* **File Location**: `~/.gemini/antigravity-cli/keybindings.json`.  
* **Reset**: To reset to default, delete the `keybindings.json` file.  

**Default Keybindings**

| Action/Command | Keys | Purpose |
| :--- | :--- | :--- |
| **Clear TUI Screen** | `ctrl+l` | Clear terminal output |
| **Enter / Submit** | `enter` | Submit prompts or choices |
| **Escape / Cancel** | `ctrl+c`, `esc` | Stop stream, close menus, or clear prompt |
| **Exit CLI** | `ctrl+d` | Terminate CLI TUI session |
| **Suspend CLI** | `ctrl+z` | Push CLI session to terminal background |
| **Edit Command** | `e` | Open editor to edit proposed terminal command |
| **Confirm No** | `n` | Decline terminal command execution |
| **Confirm Yes** | `y` | Approve terminal command execution |
| **Open Editor** | `ctrl+g` | Edit prompt inside your default shell editor |
| **Paste Text** | `ctrl+v` | Paste text from your clipboard |
| **Redo Text Edit** | `ctrl+shift+z` | Redo last undone text change |
| **Undo Text Edit** | `ctrl+_`, `ctrl+shift+-` | Undo last text change |
| **Yank (Copy)** | `ctrl+y` | Yank/copy selected text |
| **Navigate Down** | `down` | Scroll down in menu lists |
| **Go to Bottom** | `ctrl+end` | Jump TUI view directly to the bottom |
| **Go to Top** | `ctrl+home` | Jump TUI view directly to the top |
| **Navigate Left** | `left` | Move prompt cursor left |
| **Page Down** | `pgdown`, `shift+down` | Scroll TUI page down |
| **Page Up** | `pgup`, `shift+up` | Scroll TUI page up |
| **Navigate Right** | `right` | Move prompt cursor right |
| **Tab / Focus** | `tab` | Auto-complete choices or switch component focus |
| **Navigate Up** | `up` | Scroll up in menu lists |
| **Insert Newline** | `alt+enter`, `ctrl+j`, `shift+enter` | Add newline to prompt without submitting |

You can map a single action to many keybindings in the JSON file. To disable keybindings, set the list to empty (e.g., `[]`). If the file is malformed, the CLI will use the valid parts and fall back to defaults for the broken actions.  

<Announcement>
icon: warning
iconColor: var(--theme-primary)
color: var(--theme-surface-surface-container)
text: **Important**: Keybindings `cli.exit` and `cli.enter` cannot be disabled.
</Announcement>

---

# Antigravity CLI Features

### Plugins 

**How Plugins Work**  
Plugins are namespaced bundles that can contain skills, agents, rules, MCP servers, and hooks as a single deployable unit.

When you install a plugin, the CLI stages the files in your home directory under `~/.gemini/antigravity-cli/plugins/<plugin_name>/`. The Antigravity Agent automatically discovers and loads these staged customizations.

```
~/.gemini/antigravity-cli/
├── plugins/
│   └── <plugin_name>/
│       ├── plugin.json         # Required marker file
│       ├── mcp_config.json     # Optional MCP server definitions
│       ├── hooks.json          # Optional event hooks definition
│       ├── skills/             # Optional skills
│       ├── agents/             # Optional subagents
│       └── rules/              # Optional rules
└── import_manifest.json        # Tracking manifest
```

**Accessing Plugin Components**  
Once staged and loaded, you can interact with the plugin components inside the CLI using slash commands.

### Terminal Sandbox 

The Terminal Sandbox is a lightweight security isolation mechanism that protects your host system from potentially destructive file manipulations or unauthorized outbound network requests when the agent executes local shell commands.

Rather than running heavy virtual machines or containers, the CLI leverages native operating system features (`nsjail` on Linux, `sandbox-exec` on macOS, and `AppContainer` on Windows) to enforce strict containment boundaries with zero startup overhead.

**Configuration**  
You can configure the sandbox behavior in your `settings.json` file (located at `~/.gemini/antigravity-cli/settings.json`):

```json
{
  "enableTerminalSandbox": true
}
```

* **`enableTerminalSandbox`** (boolean, default: `false`): Enables general execution containment barriers on all local agent processes.

**Interactive Approvals**  
When the agent proposes a terminal command that requires your confirmation, the CLI prompt adapts dynamically based on your settings:

* **When the Sandbox is Enabled**: The confirmation prompt will include a specific option to **Yes, and run without sandbox restrictions** if you need to temporarily bypass the containment boundary for a single trusted command.  
* **When the Sandbox is Disabled**: The prompt will include an option to **Yes, and run in sandbox** if you want to force a specific, potentially risky command to execute within the safety boundary.

### CLI Slash Commands Reference

The Antigravity CLI supports a variety of slash commands typed directly into the prompt box to manage conversations, configure settings, and inspect agent capabilities.

### Core Slash Commands

| Command | Category | Purpose |  
| :--- | :--- | :--- |  
| **`/resume`** *(alias `/switch`)* | Conversation | Open the conversation picker to resume or switch sessions. |  
| **`/rewind`** *(alias `/undo`)* | Conversation | Roll back conversation history to a previous checkpoint. |  
| **`/rename <name>`** | Conversation | Rename the active conversation thread for easier tracking. |  
| **`/permissions`** | Configuration | Select agent autonomy level (`request-review`, `always-proceed`, or `strict`). |  
| **`/model`** | Configuration | Select the default reasoning model (persists across sessions). |  
| **`/keybindings`** | Configuration | Open the interactive keyboard shortcut editor. |  
| **`/statusline`** | Configuration | Customize real-time indicators displayed in the CLI status bar. |  
| **`/tasks`** | Tools & Monitoring | Monitor, view logs for, or terminate active background tasks. |  
| **`/skills`** | Tools & Monitoring | Browse local and global encapsulated agent workflows. |  
| **`/mcp`** | Tools & Monitoring | Open the panel to configure and manage Model Context Protocol servers. |  
| **`/open <path>`** | Utility | Immediately open a file in your preferred external editor. |  
| **`/usage`** | Utility | Open the inline interactive help manual inside the terminal. |  
| **`/logout`** | Account | Log out of your Google session and clear cached credentials. |

### Advanced Customization via `settings.json`

For power users, several slash commands support deep customization via your `~/.gemini/antigravity-cli/settings.json` configuration:

* **Fine-Grained Permissions**: Instead of global levels, define specific allowed/denied commands:  
  ```json  
  "permissions": {  
    "allow": ["command(git)", "command(npm test)"],  
    "deny": ["command(rm -rf)"]  
  }  
  ```  
* **Custom Status Line & Window Titles**: You can pipe live agent metadata (JSON format containing CWD, active model, token usage, state, etc.) directly into your own custom shell scripts to generate dynamic status bars or terminal window titles.

### Subagents in Antigravity CLI 

Antigravity CLI features an asynchronous subagents framework that allows the main agent to delegate parallel work, perform background research, and run system tests without blocking your active conversation.

**What are Subagents?**  
Subagents are independent, concurrent agent sessions designed to tackle specific background tasks in parallel with the main conversation.

* **Purpose**: The main agent automatically spawns subagents to perform background operations such as looking up documentation, running builds, or validating a fix.  
* **Capabilities**: Subagents have full access to tools such as code search, file editing, terminal commands, and web searches to complete their assigned tasks.   
  * The main agent decides what tools and permissions subagents get, including whether they can use MCP tools and if they can write files.

### Managing Agents: The `/agents` Panel

Antigravity CLI provides an interactive terminal UI to view, manage, and approve actions for running subagents.

* **Access**: Type `/agents` in the prompt to open the subagents panel.  
* **Overview**: The panel shows a list of active and completed subagents, including surface-level details such as their status (running, done, killed, etc.) and the current step they are executing.  

<Announcement>
icon: info
iconColor: var(--theme-primary)
color: var(--theme-surface-surface-container)
text: Selecting a subagent from the panel opens a full-screen detail view. This view shows the entirety of the subagent’s conversation, including its steps, thoughts, and tool execution logs.
</Announcement>

**Tool Confirmations & Approvals**  
When a subagent wants to execute a tool that requires user permissions (such as running a local command or writing a file), it will surface the request. You can manage approvals in two ways: 

1. **Detail View Approvals**  
   The Subagent Detail View features an interaction section containing all pending approvals, where you can selectively approve or deny requests.  
     
   <Announcement>
   icon: lightbulb
   iconColor: var(--theme-primary)
   color: var(--theme-surface-surface-container)
   text: **Tip**: Use the keyboard shortcut `ctrl+j` to "teleport" from the main conversation directly to the detailed view of the next subagent waiting for your approval.
   </Announcement>
     
2. **Fast Path Alerts**  
   To keep you in your flow, Antigravity CLI displays a Fast Path Alert directly above your prompt box when a subagent requests permission.  
     
   <Announcement>
   icon: lightbulb
   iconColor: var(--theme-primary)
   color: var(--theme-surface-surface-container)
   text: **Tip**: You can approve a pending subagent permission instantly using `ctrl+k` without ever having to switch away from the main conversation.
   </Announcement>

---

# Migrating from Gemini CLI

If you are an existing Gemini CLI user looking to migrate your workflow to Antigravity CLI, you have come to the right place. The guide below will help you get familiar with and up and running quickly in Antigravity CLI.

<Announcement>
icon: info
iconColor: var(--theme-primary)
color: var(--theme-surface-surface-container)
text: **TL;DR**: Antigravity CLI supports the majority of features from Gemini CLI. While there is not 100% feature parity, workflow defining features like *Gemini CLI extensions* (Antigravity plugins), *Agent Skills*, *MCP servers*, *hooks*, and *subagents* are all supported in Antigravity CLI.
</Announcement>

On the first launch of Antigravity CLI, you should see **Migration Options** where you can choose to migrate your existing Gemini CLI extensions to the equivalent *Antigravity Plugins*.  

<Announcement>
icon: info
iconColor: var(--theme-primary)
color: var(--theme-surface-surface-container)
text: **Note**: Some Gemini CLI extensions cannot be migrated 1:1 to Antigravity plugins as some components (e.g., custom themes) are not currently supported.
</Announcement>

For the majority of users, you can now get started using Antigravity CLI with the workflows you have come to love in Gemini CLI. Antigravity CLI loads in the same context files and global Agent Skills as Gemini CLI does.

If you notice something not working the way it should or how you expect, refer to the specific details below.

## Gemini CLI Extensions → Antigravity Plugins

Since Gemini CLI launched extensions (a way to extend the CLI by bundling and sharing capabilities), the industry has standardized on the term **plugins**. Antigravity plugins are supported in Antigravity CLI.

Users should be prompted on the first launch of Antigravity CLI to have their extensions automatically migrated to plugins. You can also run an explicit command from your terminal to migrate them:

```bash
agy plugin import gemini
```

Running the `agy plugin import` command will search for each locally installed extension and convert them to an Antigravity plugin:

```text
  [ok]    conductor
          - skills      : skipped (not found)
          - agents      : skipped (not found)
          ✔ commands    : 6 processed (converted to skills)
          - mcpServers  : skipped (not found)
          - hooks       : skipped (not found)
  [ok]    google-workspace
          ✔ skills      : 6 processed
          - agents      : skipped (not found)
          ✔ commands    : 4 processed (converted to skills)
          ✔ mcpServers  : 1 processed
          - hooks       : skipped (not found)
```

## Context Files (Rules)

Antigravity CLI supports the same context files as Gemini CLI:

* **Workspace Context**: Reads both `GEMINI.md` and `AGENTS.md` from your active workspace directory.
* **Global Context**: Automatically loads and enforces global constraints located at `~/.gemini/GEMINI.md`.

## Agent Skills

Agent Skills work in Antigravity CLI just as they do in Gemini CLI. They can be managed with the same `/skills` command and are also converted into slash commands allowing them to be manually invoked.

Global skills for Gemini CLI were located in `~/.gemini/skills/` and are shared with Antigravity CLI across all workspaces. No action is needed for global skills; they are picked up automatically.

Workspace-specific skills for Antigravity CLI are stored in `.agents/skills`, which means if you have project/workspace skills in a given project within the `.gemini/skills` folder, they will need to be moved to `.agents/skills`.

| Attribute | Gemini CLI | Antigravity CLI |
| :--- | :--- | :--- |
| **Location** | Global: `~/.gemini/skills/`<br>Workspace: `.gemini/skills/` or `.agents/skills/` | Global: `~/.gemini/antigravity-cli/skills/`<br>Workspace: `.agents/skills/` |
| **Management** | `/skills` | `/skills` |
| **Behavior** | Skills become slash commands | Skills become slash commands |

<Announcement>
icon: info
iconColor: var(--theme-primary)
color: var(--theme-surface-surface-container)
text: **Note**: Antigravity CLI does not currently have an equivalent to the `gemini skills` command for managing Agent Skills on your terminal. You can create your own skills files manually or use `npx skills install`.
</Announcement>

## MCP Servers

Antigravity CLI supports both local and remote MCP servers and provides the same `/mcp` command to manage them. The main difference from Gemini CLI is the file location where `mcpServers` are defined.  

Antigravity and Antigravity CLI store MCP server configurations in a distinct `mcp_config.json` file, whereas Gemini CLI stores them inline in your `settings.json`.

<Announcement>
icon: warning
iconColor: var(--theme-primary)
color: var(--theme-surface-surface-container)
text: **Important**: Antigravity CLI uses the `serverUrl` field instead of `url` (or the deprecated `httpUrl`) for remote MCP servers.
</Announcement>

| Attribute | Gemini CLI | Antigravity CLI |
| :--- | :--- | :--- |
| **Location** | Global: `~/.gemini/settings.json`<br>Workspace: `.gemini/settings.json` | Global: `~/.gemini/antigravity-cli/mcp_config.json`<br>Workspace: `.agents/mcp_config.json` |
| **Management** | `/mcp` | `/mcp` |

---

## Antigravity SDK

## Google Antigravity SDK

The Antigravity SDK is a programmatic Python framework designed to build, test, and run autonomous AI agents. It extends the same core agent harness that powers the Antigravity CLI and Antigravity 2.0, allowing you to integrate advanced agentic capabilities directly into your own applications and workflows.

The SDK decouples your agent's logic from where it runs, allowing you to focus on what the agent does; the SDK handles how and where it executes. 

### Quick Start

Install the SDK using pip:

```bash
pip install google-antigravity
```

#### Hello World Example

A functional agent that can interact with your local environment in under 15 lines of Python:

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig

async def main():
    config = LocalAgentConfig()
    async with Agent(config) as agent:
        response = await agent.chat("What files are in the current directory?")
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())
```

### Core Pillars

**1. Governed Extensibility (Tools)**  
Every agent starts with a built-in toolset (file I/O, code editing, shell execution, directory search) and can be extended using four types of tools under a unified execution pipeline:

*   **Built-in Tools:** Core file and system manipulation capabilities.  
*   **Custom Python Functions:** Register any Python callable as an agent tool.  
*   **MCP Servers:** Connect any Model Context Protocol (MCP) server (stdio, SSE, or HTTP).  
*   **Agent Skills:** Load reusable packages of instructions and tools.

**2. Declarative Safety Policies**  
Configure agent permissions using a declarative "deny by default" policy system to control when and how tools are executed:

```python
from google.antigravity.hooks.policy import deny, allow, ask_user

policies = [
    deny("*"),                                         # Block all tools by default
    allow("view_file"),                                # Allow reading files silently
    ask_user("run_command", handler=my_handler),       # Require human approval for shell execution 
]
```

**3. Lifecycle Hooks**  
Gain granular control over agent execution with three categories of hooks across nine concrete lifecycle points (e.g., session start, pre/post turn, pre/post tool call):

*   **Inspect** (Read-Only, Non-Blocking): For logging, audit trails, and metrics.  
*   **Decide** (Read-Only, Blocking): For custom approval/denial logic (policies).  
*   **Transform** (Modifying, Blocking): For sanitizing data in transit or recovering from tool errors.

---

#### Key Capabilities

*   **Streaming:** Access live model reasoning and output chunks as they are generated.  
*   **Multimodal Input:** Pass images, PDFs, audio, and video natively using `from_file()`.  
*   **Sub-agents:** Spawn child agents with independent tools and contexts to build multi-agent teams.  
*   **Structured Output:** Define schemas using Pydantic models to return validated, typed data directly.  
*   **Human-in-the-Loop:** Pause execution to ask structured questions and branch based on user input.  
*   **Observability:** Track per-turn and cumulative token usage and access thinking traces.

To use the SDK more easily within Antigravity 2.0, use the Antigravity SDK Skill. To learn more about the Antigravity SDK and see more examples of how to use it, visit [**the GitHub repository**](https://github.com/google-antigravity/antigravity-sdk-python)

---

## Antigravity IDE

# Google Antigravity

Google Antigravity is an agentic development platform, evolving anyone to build in the agent-first era. Antigravity enables developers to operate at a higher, task-oriented level managing agents across workspaces, while also retaining a familiar AI IDE experience for developers. Antigravity extracts agents into their own surface and provides them the tools needed to autonomously operate across the editor, terminal, and browser emphasizing verification and higher-level communication via tasks and artifacts. This capability enables agents to plan and execute more complex, end-to-end software tasks, elevating all aspects of development, from building features, UI iteration, and fixing bugs to research and generating reports.

<FeatureBlocks>
name: Main Features
blocks:
- link: /
  icon: automatic_cluster
  title: Agent Manager
  description: Agent Manager view for an agent-first experience built around planning mode, the conversation UI, and artifact review.
- link: /
  icon: automatic_cluster
  title: AI-powered IDE
  description: An AI-powered IDE with all of the AI features that developers have come to rely on such as Agent, Tab, and Command.
- link: /
  icon: automatic_cluster
  title: Asynchronous Agents
  description: Asynchronous, local agents that can work in parallel on all of your workspaces.
- link: /
  icon: automatic_cluster
  title: Multi-window
  description: A multi-window product with an Editor, Manager, and Browser.
- link: /
  icon: automatic_cluster
  title: Browser Agent
  description: Agent that can actuate the browser for you and to accomplish dev tasks like dashboard reads, SCM actions, UI testing, etc. in the Browser.
</FeatureBlocks>

## Core Surfaces

<IconCardGroup>
- link: /
  icon: automatic_cluster
  title: Agent Manager
  description: An orchestration “no code” view to start and view tasks in a minimalist product focused on the conversation and artifacts.
- link: /
  icon: automatic_cluster
  title: Editor
  description: A fully-functional AI-powered IDE that maps to a single workspace.
- link: /
  icon: automatic_cluster
  title: Browser
  description: Browser-use agent capabilities to read & actuate on more surfaces beyond just the IDE.
</IconCardGroup>

## Key Terms

- **Agent**: The primary AI modality within Antigravity. While the user can work tightly with an Agent within the Editor, they can also have multiple agents working across multiple codebases, orchestrated and monitored through the Agent Manager.
- **Tab & Command**: The other AI modalities within Antigravity, specifically within the text editor part of the editor surface. Tab is a more powerful “autocomplete” and Command is an inline instructive modality. From past experience, these do not get nearly as much use as the Agent.
- **Artifacts**: We define an artifact as anything that the agent creates to allow it to get its work done or communicate its accomplishments to the human user. These include rich markdown files, diff views, architecture diagrams, images, browser recordings, etc.

---

# Getting Started

## Download

Please visit [antigravity.google/download](https://antigravity.google/download) to download Google Antigravity.

<b>Available platforms and minimum versions:</b>
- **macOS**: macOS versions with Apple security update support. This is typically the current and two previous versions. Min Version 12 (Monterey), X86 is not supported
- **Windows**: Windows 10 (64 bit)
- **Linux**: glibc >= 2.28, glibcxx >= 3.4.25 (e.g. Ubuntu 20. Debian 10, Fedora 36, RHEL 8)

The application will prompt when updates are available:

![Update Available](assets/image/docs/restart-to-update.png)

## Basic Navigation

The Agent Manager can be opened from the Editor via the button on the top bar or via keyboard shortcut `Cmd + E`:

![Editor Open Agent Manager](assets/image/docs/editor-open-agent-manager.png)

Similarly, from the Agent Manager, the Editor can be opened from any workspace via the “Focus Editor” option in the workspace’s drop down. When focused on a workspace, the Editor can be opened from any of the “Open Editor” buttons, or via the keyboard shortcut `Cmd + E`.

![Agent Manager Open Editor](assets/image/docs/agent-manager-open-editor.png)

---

# Firebase Studio Migration

Antigravity is Google's next-generation, agent-first platform. It’s designed to be the primary home for high-velocity, autonomous development workflows. Instead of relying on just a cloud-based web editor, Antigravity brings the power of AI right into your local development environment.

## Why Antigravity?

Antigravity offers significant enhancements over the web-based Code view in Firebase Studio:

- **Local environment control**: Antigravity runs locally on your machine, which means you have full control over your filesystem, versions, and terminal.
- **True agentic development**: Move beyond basic code completion. Antigravity provides agentic development workflows that can autonomously format, test, and implement entire tasks across your codebase.
- **Seamless Firebase support**: You can still easily deploy your projects to Firebase, communicate with Firebase services via the Firebase CLI, and test your functions locally as you always have.

## Learn how to navigate Antigravity

To help you settle in, here is where you can find your favorite Firebase Studio features in Antigravity:

<IconCardGroup>
- link: /docs/editor
  icon: code
  title: Cloud IDE Code view
  description: Enjoy the familiar interface of VS Code, but supercharged with AI and running locally on your hardware.
- link: /docs/agent
  icon: auto_awesome
  title: Agentic chat
  description: The AI chat you used in Firebase Studio is now natively integrated into your IDE, capable of taking autonomous actions across your local files.
- link: /docs/tools
  icon: rocket_launch
  title: App Hosting deployments
  description: You can continue to deploy and manage your App Hosting URLs seamlessly using the Firebase CLI or built-in IDE integrations.
- link: /docs/browser
  icon: important_devices
  title: Browser-based emulators
  description: Run the Firebase Local Emulator Suite directly on your machine for faster, offline testing.
</IconCardGroup>

## Migrate your Firebase Studio project to Antigravity

Antigravity is a local, agent-first IDE that brings the power of AI into your local development environment.

### Prerequisites

Ensure you have the following installed locally and fully up-to-date:

- [Google Antigravity IDE](https://antigravity.google/download)
- [Node.js](https://nodejs.org/en) (version 20 or higher)
- [Firebase CLI](https://firebase.google.com/docs/cli) (version 15.10.0 or higher)

### Step 1: Export and initialize your app

**Option 1: Automated migration**

This workflow uses the Antigravity agent to autonomously handle project transformation.

1. In Firebase Studio, click the **Move now** button at the top of your workspace.
2. Follow the export method based on the window that appears:
   - If you see a **Zip and Download** button, click it.
   - Otherwise, open the command palette (`Cmd` + `Shift` + `P` on Mac or `Ctrl` + `Shift` + `P` on ChromeOS, Windows, or Linux) and run the **Firebase Studio: Zip & Download** command.
3. Extract the folder locally and open it in Antigravity.
4. In the Agent pane within Antigravity, enter the following prompt. To optimize your workflow and conserve tokens, we recommend selecting the **Gemini Flash** model. It’s designed for speed and efficiency in high-volume transformation tasks like file conversion.

```
@fbs-to-agy-export
```

   The Antigravity agent will then begin project migration, requesting your assistance along the way. Follow the agent’s guidance to complete the migration process. If you encounter any errors, prompt the agent to try again.

<Announcement>
icon: info
color: "#f5f5f5"
iconColor: "#4285f4"
text: "If the download window doesn’t appear, check your browser’s address bar for a pop-up blocker icon and ensure pop-ups are allowed."
</Announcement>

**Option 2: Manual export**

If you prefer to manage the migration yourself without using AI tokens, you can use the Firebase CLI to manually export your project. This method is direct and does not require agent interaction.

Open your terminal and run the following command, replacing `<path>` with the file path to your extracted project folder or the original `.zip` file:

```bash
npx firebase-tools@latest studio:export <path>
```

<Announcement>
icon: warning
color: "#fff8e1"
iconColor: "#f9ab00"
text: "The <code>studio:export</code> command is currently optimized for Next.js, Flutter, and Angular workspaces. While you can use this command for other workspace types, the migration may not be fully successful. We’re actively working to improve the migration flow."
</Announcement>

### Step 2: Preview your app

Once you have extracted your project and opened it within Antigravity, you can view your application locally:

1. In Antigravity, navigate to the **Run and Debug** menu located in the left sidebar.
2. Click the play button to start your local development server.
3. Follow the instructions in the terminal to preview your app.

<Announcement>
icon: lightbulb
color: "#f5f5f5"
iconColor: "#4285f4"
text: "To refine your app or troubleshoot issues, simply chat with the agent using natural language. If the agent pane is hidden, click the Toggle Agent icon at the top of the window to reopen it."
</Announcement>

### Step 3: Publish your app

Antigravity uses agent skills to publish your app using Firebase best practices.

1. In the chat panel, enter the following prompt: simply instruct the agent:

```
Publish my app
```

2. When prompted to run `firebase deploy`, choose **Yes**. The agent will publish to your existing URL if you’ve previously published to App Hosting. If this is your first time publishing to App Hosting, the agent will walk you through the process.
3. For future updates, simply instruct the agent to `publish my app` in the Antigravity chat panel.

## Continue your work

There are several ways you can continue your development in Antigravity.

- **Running workflows:** In Antigravity, you can seamlessly execute workflows and continue your work with the model by typing `@workflows <workflow_name>` into the agentic chat panel.
- **App Hosting deployments:** You can seamlessly deploy your apps directly through the agent using agent skills, or by using the platform-agnostic Firebase CLI and GitHub.
- **Troubleshooting:** If you experience deployment issues, try re-authenticating with the Firebase CLI or verifying your project secrets.

Thank you for being part of the Firebase Studio journey. Your prototypes and feedback have directly shaped Google's AI tools, and we can’t wait to see what you build next in Antigravity!

## Need help?

File any migration bugs in our [GitHub Issues](https://github.com/firebase/firebase-tools/issues).

---

# Editor

The primary entry point to Antigravity is our Editor, a surface based upon the VS Code codebase but full of rich AI-enabled features designed to improve your code-writing experience. 

Much of this editor is designed to feel the same as prior experiences you may have had. You can open files up, tab through them, edit them directly, get suggestions with [Tab](docs/tab), and work with an agent on [smaller](docs/command) or [larger tasks](docs/agent-side-panel). When you’re done, you can review your changes and interface with your preferred [source control](docs/review-changes-editor). You can also still download extensions from the Open VSX marketplace to augment your experience, through further syntax highlighting, source control integrations, or other additions. 

![Editor Screenshot](assets/image/docs/editor/editor.png)

---

# Antigravity Editor: Tab & Navigation

This guide covers the core navigation and completion tools: **Supercomplete**, **Tab-to-Jump**, and **Tab-to-Import**.

## Supercomplete

Supercomplete provides code suggestions in a region near your current cursor position.

![Supercomplete](assets/image/docs/editor/supercomplete.png)

### How it Works

- **File-Wide Suggestions**: Suggestions can modify code throughout the document, handling tasks like changing variable names or updating separate function definitions simultaneously.
- **Accepting**: Press `Tab` to accept the changes.

## Tab-to-Jump

Tab-to-Jump is a fluid navigation tool that suggests the next logical place in your document to move your cursor to.

![Tab-to-Jump](assets/image/docs/editor/tab_to_jump.png)

### How it Works

- A "Tab to jump" icon will appear offering to move your cursor to where your next logical edit will be. Pressing `Tab` instantly moves your cursor to that location.
- **Accepting**: Press `Tab` to accept the jump.

## Tab-to-Import

Tab-to-Import handles missing dependencies without breaking your flow.

![Tab-to-Import](assets/image/docs/editor/tab_to_import.png)

### How it Works

- **Detection**: If you type a class or function that isn't imported, Antigravity suggests the import.
- **Action**: Press `Tab` to complete the word and instantly add the import statement to the top of the file.

## Settings

In your settings, you can customize the behavior of these features:
- **Enable/Disable Features**: You can individually turn off Autocomplete, Tab-to-Jump, Supercomplete, or Tab-to-Import.
- **Tab Speed**: Controls the responsiveness of suggestions.
  - `Slow`: Waits for more context before suggesting.
  - `Default`: Offers a balanced pace.
  - `Fast`: Provides rapid-fire suggestions.
- **Highlight Inserted Text**: When enabled, text inserted via Tab is highlighted to track changes easily.
- **Clipboard Context**: When enabled, Antigravity uses the contents of your clipboard to improve completion accuracy.
- **Allow Gitignored Files**: Enables Tab features (suggestions and jumping) within files listed in your `.gitignore` file. Tab will only ignore gitignored files if git is installed.

---

# Antigravity Editor: Command

The **Command** feature brings the power of natural language directly into your workflow, allowing you to request specific inline completions or terminal commands on the fly.

## How it Works
1. **Trigger**: Press `Command + I` (Mac) or `Ctrl + I` (Windows/Linux).
2. **Prompt**: A text input box will appear at your current cursor position.
3. **Instruction**: Type your request in natural language (e.g., "Create a function to sort this list" or "Add error handling to this block").
4. **Execution**: Antigravity generates the code or command directly inline for you to review and accept.

## Where to Use It

### In the Editor

![Command in Editor](assets/image/docs/editor/command_editor.png)

Use Command to generate boilerplate code, refactor complex functions, or write documentation without breaking your coding flow.

* _Example_: "Create a React component for a login form."

### In the Terminal

![Command in Terminal](assets/image/docs/editor/command_terminal.png)

Use Command within the integrated Antigravity terminal to generate complex shell commands without needing to memorize syntax.

* _Example_: "Find all processes listening on port 3000 and kill them."

---

# Agent Side Panel

Use the panel on the right side of the editor to work directly with the agent. You can spin up new conversations, attach images, switch [agent modes](/docs/agent-settings), and select between [different models](/docs/models). 

![Editor Agent Panel](assets/image/docs/editor/editor_agent_panel.png)

As your conversation progresses, you’ll be able to keep track of open file changes, running terminal processes, and artifacts in the bottom toolbar above the input.

![Editor Agent Panel](assets/image/docs/editor/agent_panel_toolbar.png)

---

# Review Changes + Source Control

Once the agent has begun writing code within a conversation, you’ll see a `Review Changes` section within the Agent panel’s [bottom toolbar](docs/agent-side-panel). Clicking it will open up a pane within your editor where you can scroll through all of the changes you and your agent made within the conversation. 

![Editor Review Changes](assets/image/docs/editor/review_changes_editor.png)

Just like with artifacts, you can comment on any of the file diffs to communicate with the agent.

![Editor Source Control](assets/image/docs/editor/source_control_editor.png)

---

## Core Concepts & Features

# Projects

In Antigravity 2.0, we are transitioning from the legacy repository-centric workspace model to a more flexible and secure **Project-centric** model. This document outlines what Projects are, how they work, and how they differ from the original workspace structure.

### What is a Project?

A **Project** is a configuration of folders defining the environment and the scope of your agent. Instead of forcing an agent to operate within a single folder, a project can work with one folder or multiple folders (e.g., a frontend and a backend repo), providing your agents with all of the context required for your codebase. All projects have their own isolated agent settings, allowing you to customize different projects’ security settings independently.

### Key Differences: Workspace vs. Projects

| Feature | Original Model (Workspace) | New Model (Project) |  
| :--- | :--- | :--- |  
| **Organization Scope** | Tightly coupled to a single local repository. | Projects are a configuration of all of the context and folders that your agents should work with. |  
| **Directory Boundaries** | Agent is strictly confined to one folder structure. | A single Project can span **multiple folders** at once. |  
| **Settings Isolation** | Settings inherited globally from the machine. | Projects have their own settings. Agents in a project use the project's settings. |  
| **Permissions** | Broad, global permissions. | Global permissions are inherited. Projects can have their own permissions in addition to global permissions. |  
| **Customizations** | Skills/MCPs managed globally or per-workspace. | Reusable skills, MCPs, and hooks are stored at the Project level. |

### Core Project Concepts

**1. Folders**  
A Project is composed of **folders**, which define the directories and repositories the agent is allowed to access:  
* **Local Folders**: A folder that doesn’t have git configured.  
* **Local Git Checkout**: A folder that is a Git repository checkout.

**2. Worktree Selection (Local vs. New Worktree)**  
When starting a new conversation in a Project, you choose how the agent should interact with your folders via the worktree selector:

* **Local Mode**: The agent works directly in your active local folders or Git checkouts. (Best for quick, interactive edits in your current working folder).  
* **New Worktree Mode**: Creates a new Git worktree for the conversation. (Best for complex tasks, keeping your active working folder untouched and preventing parallel subagents from conflicting).

**3. Scoped Settings and Permissions**  
Settings and permissions are both scoped at the project level:  
* **Settings**: When a Project is created, it always starts with the default security preset where it has read and write access to all of your project’s folders and will ask for permission to run all terminal commands. These settings can be modified and apply to all agents within this project.  
* **Permissions**: Projects inherit global permissions but allow you to augment them at the Project level, ensuring agents only have the exact access required for that specific project's tasks.

### Workflows using Projects

* **Working in a Single Folder**: Create a project with a folder and then configure its settings.  
* **Working in Multiple Folders**: Add all related folders into a single Project so the agent has full context across your codebases.  
* **Running Parallel Agents on the Same Folder**: Choose **Local Mode** when starting an agent so that all of your agents work in the same active folders.  
* **Isolating Concurrent Agents**: Choose **New Worktree Mode** when starting an agent so that separate, isolated Git worktrees are provisioned for each agent session, avoiding conflicts between agents.  
* **Mixed Checkouts & Local Folders**: Working locally operates directly in the existing folders. Using "New Worktree Mode" will spawn a new Git worktree for all active Git checkouts, allowing the agent to operate inside the new worktrees and the existing non-git local folders simultaneously.

---

# Models

## Reasoning Model

For the core reasoning model, Antigravity offers leading frontier models from the Gemini Enterprise Agent Platform:

* Gemini 3.5 Flash  
* Gemini 3.1 Pro (high)  
* Gemini 3.1 Pro (low)  
* Gemini 3 Flash  
* Claude Sonnet 4.6 (thinking)  
* Claude Opus 4.6 (thinking)  
* GPT-OSS-120b

Users can select which reasoning model they want to use within the model selector dropdown under the conversation prompt box:

![Model Selector Drop Down](/assets/image/docs/model-selector.png)

The choice of reasoning model is sticky between user messages within a conversation, so if you change the reasoning model while the Agent is running, it will continue to use the previously selected reasoning model until it has completed its steps for that user turn (or until you cancel the current execution).

Learn more about reasoning model rate limits in [our plans page](/docs/plans).

## Additional Models

Antigravity uses a number of other models for various parts of the stack that are not customizable:

* **Nano Banana 2**: Used by the generative image tool when the Agent wants to produce a UI mockup, needs images to populate a web page or application, generate system or architecture diagrams, or other generative image tasks.

---

# Agent Settings

### Terminal Command Auto Execution

Controls how the agent executes generated shell commands:
* **Request Review**: The agent will never auto-execute terminal commands (except those explicitly added to your configurable Allow list).
* **Always Proceed**: The agent will execute commands automatically without prompting (except those explicitly added to your configurable Deny list).

### Agent Non-Workspace File Access

Allows the agent to view and edit files outside of the active project folders. 
* By default, the agent only has access to the folders inside your Project and the application’s local app data directory `~/.gemini/antigravity/` (which contains Artifacts, Knowledge Items, etc.).
* Enforcing this boundary protects your local sensitive data. Enable non-workspace access with caution.

---

# Artifact Review

When starting a new Agent conversation, you can choose between two primary execution modes that determine how changes are proposed and reviewed:

* **Planning Mode**: The agent plans thoroughly before executing tasks. In this mode, the agent organizes its work in [task groups](/docs/task-groups), produces structured implementation plans called [Artifacts](/docs/artifacts), and thoroughly researches the codebase for optimal quality.
* **Fast Mode**: The agent executes tasks directly without a dedicated planning phase. Use this for simple, highly localized tasks that can be completed quickly, such as variable renaming, running a specific bash command, or small refactors.

When working in **Planning Mode**, the Artifact Review Policy controls how you interact with and approve these plans before changes are made to your codebase.

## Artifact Review Policy

You can customize the review workflow in the **Agent** tab of the Settings pane. Choose between two policies:

### 1. Request Review (Recommended)

The agent always halts and requests your explicit approval before proceeding with proposed changes. 

* When the agent generates an implementation plan or code diff, it will pause execution and notify you.
* This allows you to thoroughly review the proposed changes, add inline comments, and verify the plan in your workspace.
* Once you are satisfied, you can approve the plan to let the agent proceed.

![Settings Review Policy Manual](assets/image/docs/agent/settings-review-policy-manual.png)

### 2. Always Proceed

The agent never halts for manual review and immediately proceeds with executing its plans.

* When the agent decides to request a review, it will immediately bypass the pause and continue with the implementation.
* Use this if you want a fully autonomous workflow and do not need to manually verify plans before code is modified.

![Settings Review Policy Proceed](assets/image/docs/agent/settings-review-policy-proceed.png)

---

# Agent Permissions

Antigravity uses a robust, unified permission engine to secure your environment while enabling autonomous workflows. Every sensitive operation the Agent performs is represented as a **permission resource** formatted as `action(target)`.

Permissions are evaluated across three distinct access lists:
-   **Deny**: The action is blocked immediately.
-   **Ask**: The Agent pauses and prompts for your explicit approval before proceeding.
-   **Allow**: The action is auto-approved without prompting.

<Announcement>
icon: warning
color: "#fff8e1"
iconColor: "#f9ab00"
text: "<strong>Precedence Rule:</strong> Conflicting rules are strictly evaluated in priority order: <strong>Deny &gt; Ask &gt; Allow</strong>. For example, if you configure <code>command(*)</code> in Ask and <code>command(git)</code> in Allow, the Ask rule takes precedence and prompts before every command."
</Announcement>

## Supported Actions & Matching Rules

| Action | Target Format | Matching Behavior | Default Fallback |
| :--- | :--- | :--- | :--- |
| `read_file` | `read_file(/path)`, `read_file(dir)`, or `read_file(*)` | Matches absolute paths or paths relative to project workspace roots. Grants recursive read access to all contained files/folders. Using `read_file(*)` matches all files on the system. | **Ask** (Auto-allowed in workspace) |
| `write_file` | `write_file(/path)` or `write_file(*)` | Same as `read_file`. Implicitly grants `read_file` for the exact same target path. | **Ask** (Auto-allowed in workspace) |
| `read_url` | `read_url(domain)` or `read_url(*)` | Matches hostnames and subdomains (e.g., `google.com` covers `mail.google.com`). Ignores URL path segments. Using `read_url(*)` matches any domain. | **Ask** |
| `execute_url` | `execute_url(domain)` or `execute_url(*)` | Actuating on web elements (clicking, typing) or driving interactive browser workflows on a domain. | **Ask** |
| `command` | `command(prefix)`, `command(regex)`, or `command(*)` | Matches by exact word/token prefix. Each whitespace-separated token is evaluated as an anchored regular expression (`^(?:pattern)$`). E.g., `command(npm run (build.*))` matches `npm run build` and `npm run build-prod`. | **Ask** |
| `unsandboxed` | `unsandboxed(prefix)`, `unsandboxed(regex)`, or `unsandboxed(*)` | Matches commands by exact word/token prefix. Commands matching this grant will be executed outside of container isolation (only applicable when terminal sandboxing is enabled). | **Ask** |
| `mcp` | `mcp(server/tool)`, `mcp(server/*)`, or `mcp(*)` | Matches exact MCP tools or all tools on a specified server (applies equally to local `mcpl` servers and remote connections). Using `mcp(*)` matches any tool. | **Ask** |

<Announcement>
icon: info
color: "#f5f5f5"
iconColor: "#4285f4"
text: "<strong>Global Wildcard Syntax (<code>*</code>):</strong> Across all supported action types (e.g., <code>read_file(*)</code>, <code>command(*)</code>, <code>mcp(*)</code>), passing the global wildcard <code>*</code> matches all targets within that entire action namespace."
</Announcement>

### Understanding read_url vs execute_url Across the Platform
The `read_url` permission governs outbound web connectivity across three distinct areas of Antigravity:
1. **The `read_url` Tool:** When the Agent uses the internal `read_url_content` tool to fetch web page markdown for research, it checks your `read_url` grants.
2. **Browser Subagent & Tool:** When driving Chrome sessions, `read_url` authorizes loading and viewing the target domain. However, interactive UI actuation (clicking buttons, typing text) is governed independently by `execute_url`.
3. **Terminal Sandboxing:** In sandbox mode, any domain granted under `read_url` is compiled directly into the container's outbound network allowlist (`AllowedDomains`), permitting commands like `curl` or `npm` to connect to authorized hosts.

### Cross-Platform Command & Path Matching
Antigravity ensures your permission rules work flawlessly whether you are developing on macOS, Linux, or Windows. On macOS and Linux, paths use standard forward slashes (`/`). On Windows, Antigravity automatically normalizes paths prior to rule evaluation by stripping drive letters (e.g., `C:`) and converting all backslashes (`\`) to forward slashes (`/`). 

## Implicit Permission Rules

*   **Write implies Read:** Allowing `write_file` on a path automatically grants `read_file` on that path.
*   **Deny Read implies Deny Write:** Denying `read_file` on a path immediately blocks `write_file` on that path.

## Interactive Permission Prompts

When the Agent encounters an operation requiring approval (**Ask** mode), an interactive card appears in your editor. Before clicking **Allow** for file, URL, or MCP permissions, you can directly edit the target string in the prompt card to expand the granted scope (e.g., broadening a single file request like `/project/file.txt` to the parent directory `/project`). Antigravity validates that your edited target safely covers the operation and applies the expanded grant for the remainder of the turn, preventing repeated prompts for related operations. *(Note: Scope editing is not supported for terminal commands).*

## Terminal Sandboxing (Preview)

Permission grants also apply to commands when sandbox is enabled:
*   Paths granted under `read_file` dynamically populate the sandbox's read-only filesystem allowlist.
*   Paths granted under `write_file` dynamically populate the sandbox's read-write filesystem allowlist.
*   Domains granted under `read_url` define outbound network access policies.

<Announcement>
icon: info
color: "#f5f5f5"
iconColor: "#4285f4"
text: "<strong>Sandbox Availability:</strong> Terminal sandboxing is currently in preview on macOS / Linux, and coming soon to Windows."
</Announcement>

## Default System Behaviors & Guardrails

When an action is not explicitly listed in your Allow, Deny, or Ask lists, Antigravity falls back to secure system defaults:

1.  **Web Browsing Defaults to Ask:** Actions for `read_url` and `execute_url` default to **Ask**. Before the Agent navigates to or actuates on any web page, it will pause and prompt for your explicit approval unless an allow rule is configured.
2.  **Workspaces are Auto-Allowed:** In standard operation, reading and writing files inside your active project directory is automatically allowed. All other unconfigured actions (`command`, `mcp`, `execute_url`, non-workspace files) default to **Ask**.

## Configuration Examples

**Allow list** — actions that run without prompting:
```text
command(git)                       # Standard git commands
command(npm run (build|lint|test)) # Allow safe npm scripts via regex
unsandboxed(git push)              # Allow git push outside sandbox
read_file(/var/log/app)            # Read external log paths
write_file(src/)                   # Edit relative src/ folder
read_url(google.com)               # Fetch Google subdomains
mcp(linter/*)                      # Run linter MCP tools
```

**Deny list** — actions that are permanently blocked:
```text
command(rm -rf)                    # Block destructive deletions
command(curl .*)                   # Block unvetted curl downloads
command(sudo)                      # Block sudo privileges
write_file(.git/)                  # Safeguard Git history
write_file(/home/user/.ssh)        # Safeguard SSH keys
```

**Ask list** — actions that pause for manual confirmation:
```text
command(*)                         # Prompt all commands
execute_url(aws.amazon.com)        # Prompt AWS console actuation
mcp(sql/execute_mutation)          # Prompt modifying SQL queries
```

---

# Asynchronous Subagents

Subagents are an excellent way to parallelize complex tasks and preserve the context of your main agent. Instead of executing every step serially, an agent can delegate tasks—such as running tests or performing extensive codebase searches—to dedicated subagents. This architecture frees the parent agent to continue working on other tasks in parallel and prevents its context window from being polluted by the details of a subagent's work.

## Invoking Subagents

The parent agent calls the `invoke_subagent` tool to spawn a new concurrent session with a dedicated role and initial prompt.

* **Workspace Options**: The subagent can either inherit the same workspace as its parent or create an isolated Git worktree.
* **Context Isolation**: The subagent runs using the same model as its parent but does not inherit the parent's existing conversation history (context window), starting with a clean slate.
* **Execution**: Once invoked, the subagent immediately begins executing its task. A parent agent can invoke multiple subagents at any time.
* **Monitoring**: You can directly monitor the progress of any subagent by clicking into its conversation via the subagent panel.

## Subagent Lifecycle and States

Subagents run asynchronously in the background, allowing the parent agent to delegate a task and immediately resume its own work. At any point, a subagent exists in one of three states:

### 1. Running
The subagent is actively executing its task, calling tools, and generating responses.
* **Cancellation**: You can cancel a running subagent by clicking the **Stop Subagent** button in the subagent panel. This instantly cancels generation and transitions the subagent to an idle state.
* **Parent Control**: The parent agent can also interrupt a subagent (by sending a message) or kill it entirely.

### 2. Idle
The subagent has completed its task, sent a message containing the results to its parent agent, and stopped execution.
* **Re-awakening**: An idle agent can be awoken and return to the *Running* state upon receiving a message from another agent (it does not have to be its parent).
* **Context Retention**: When awoken, the agent retains all context from its prior work.

### 3. Killed
The subagent is permanently terminated and cannot be re-awoken.
* **Cleanup**: Any temporary Git worktrees generated for the subagent are automatically cleaned up.
* **Visibility**: You and other agents can still view the historical conversation transcript of a killed subagent.

## Inter-Agent Communication

Agents communicate by sending messages to each other using unique agent IDs.

* **Flexible Routing**: Agents can communicate not only with their direct parents or subagents, but also with any other active agent whose ID is known.
* **Auto-Wake**: If an idle agent receives a message, it is automatically re-awakened to process the new information.
* **Shared Transcripts**: Agents can view each other's conversation transcripts, providing a comprehensive view of the collaborative workflow.

## Built-In vs. Custom Subagents

### Built-In Subagents
Antigravity comes pre-packaged with several specialized subagents:
* **`research`**: Optimized for codebase research, navigation, and exploration.
* **`browser`**: Operates sandboxed web browsers to perform interactive browser tasks (invoked exclusively via the `/browser` slash command).
* **`self`**: A direct clone of the calling agent, sharing the identical system prompt and toolsets.

### Custom Subagents
Agents can define their own custom subagents dynamically using the `define_subagent` tool.
* **Configuration**: Define a custom system prompt and specific toolsets for read-only, write (including running terminal commands), and subagent delegation capabilities.
* **Scope**: Once defined, the custom subagent can be invoked repeatedly for the remainder of the conversation.

## Delegation Hierarchy and Limits

Subagents can invoke their own subagents, enabling multiple layers of delegation and hierarchical team structures.

<Announcement>
icon: warning
iconColor: var(--theme-primary)
color: var(--theme-surface-surface-container)
text: **Nesting Depth Limit**: A maximum nesting depth of **10 levels** (layers of subagents beneath the main agent) is strictly enforced to prevent runaway resource exhaustion.
</Announcement>

## Permissions and Configuration Inheritance

Subagents inherit their parent's safety configurations to maintain robust security boundaries:

* **Inherited Scopes**: Subagents automatically inherit the parent's allowed terminal command prefixes and file read/write directory scopes. A subagent cannot perform any action that the user has not already approved for the parent.
* **Workspace Access**: Parent agents retain full access to their subagents' workspaces, including those operating on isolated Git worktrees.
* **Permission Bubbling**: If a subagent encounters a tool call that requires explicit user confirmation, the request is automatically bubbled up to the subagent panel UI for your approval.

## Multi-Agent Teamwork (Ultra Plan Only)

Antigravity 2.0 introduces advanced multi-agent orchestration for extremely complex tasks.

<Announcement>
icon: star
iconColor: var(--theme-primary)
color: var(--theme-surface-surface-container)
text: **Ultra Plan Exclusive**: The `/teamwork-preview` slash command is currently in preview and is exclusive to users on the **Ultra ($200/mo) plan**.
</Announcement>

Using `/teamwork-preview` prompts the main agent to launch a collaborative multi-agent framework. This framework features built-in error recovery, automatic retries, and coordination logic, allowing you to simply define the high-level goal while the platform manages the overhead of a cooperative agent team.

---

# Strict Mode

Strict mode provides enhanced security controls for the Agent, allowing you to restrict its access to external resources and sensitive operations. When strict mode is enabled, several security measures are enforced to protect your environment.

## Features

### Browser URL Allowlist/Denylist

In strict mode, the Agent's ability to interact with external websites is governed by the browser's Allowlist and Denylist. This applies to:
- **External Markdown Images**: The Agent will only render images from URLs that are allowed.
- **Read URL Tool**: The Read URL tool will only auto-execute for allowed URLs.

### Terminal, Browser, and Artifact Review Policies

Strict mode enforces the following behavior for terminal, browser, and artifact interactions:
- **Terminal Auto Execution**: Set to "Request Review". The Agent will always prompt for permission before executing any terminal command. The terminal allowlist is ignored when strict mode is enabled.
- **Browser Javascript Execution**: Set to "Request Review". The Agent will always prompt for permission before executing Javascript in the browser.
- **Artifact Review**: Set to "Request Review". The Agent will always prompt for confirmation before acting on plans laid out in artifacts.

### File System Access

Strict mode restricts the Agent's access to the file system to ensure it only interacts with authorized files:
- **Respect .gitignore**: The Agent will respect `.gitignore` rules, preventing it from accessing ignored files.
- **Workspace Isolation**: Access to files outside the workspace is disabled. The Agent can only view and edit files within the designated workspace.

---

# Plugins

Plugins are namespaced bundles that allow you to extend Antigravity's capabilities by grouping skills, rules, MCP servers, and hooks into a single package.

## Directory Structure

If you want to create your own plugins or inspect existing ones, they follow a specific directory structure. A plugin is a directory containing a `plugin.json` file and optional subdirectories for different customization types:

```text
plugins/<plugin-name>/
├── plugin.json       # Required marker file
├── mcp_config.json   # Optional MCP server definitions
├── hooks.json        # Optional hooks definition
├── skills/           # Optional skills
│   └── <skill-name>/
│       └── SKILL.md
└── rules/            # Optional rules
    └── <rule-name>.md
```

### Manifest File (`plugin.json`)

Every plugin must have a `plugin.json` file at its root. This file identifies the directory as a plugin.

```json
{
  "name": "my-custom-plugin"
}
```

The `name` field is optional and defaults to the directory name if omitted.

## Supported Components

A plugin can contain the following components:

1. **Skills**: Located in the `skills/` subdirectory. Each skill must have a `SKILL.md` file containing instructions for the agent.  
2. **Rules**: Located in the `rules/` subdirectory. These are markdown files that define constraints or guidelines for the agent's behavior.  
3. **MCP Servers**: Configured via `mcp_config.json` at the plugin root. This allows you to connect Antigravity to external tools and services.  
4. **Hooks**: Configured via `hooks.json` at the plugin root. These allow you to run scripts or commands when specific events occur.

## How to Add Plugins

There are two ways to add plugins to Antigravity:

### 1. Using Bundled Plugins (Build with Google)

Antigravity comes with a variety of bundled plugins created by Google. You can browse and add these plugins directly from the user interface:

* Navigate to the **Customizations** page.  
* For more details about the available Google-built plugins, see the [Build with Google Page](/docs/build-with-google).

### 2. Manually Adding Plugins

You can also add custom plugins by placing your plugin folders in one of the designated plugin locations. Antigravity automatically scans these directories to discover and load your customizations:

* **Workspace Level**: Place your plugin folder inside a `.agents/plugins/` or `_agents/plugins/` directory at the root of your opened workspace. This makes the plugin available only when working in this specific workspace.  
* **Global Level**: Place your plugin folder inside `~/.gemini/config/plugins/` in your user home directory. This makes the plugin active across all workspaces.

---

# Antigravity Editor: MCP Integration

Antigravity supports the Model Context Protocol (MCP), a standard that allows the editor to securely connect to your local tools, databases, and external services. This integration provides the AI with real-time context beyond just the files open in your editor.

## What is MCP?

MCP acts as a bridge between Antigravity and your broader development environment. Instead of manually pasting context (like database schemas or logs) into the editor, MCP allows Antigravity to fetch this information directly when needed.

## Core Features

### 1. Context Resources

The AI can read data from connected MCP servers to inform its suggestions.

**Example:** When writing a SQL query, Antigravity can inspect your live Neon or Supabase schema to suggest correct table and column names.

**Example:** When debugging, the editor can pull in recent build logs from Netlify or Heroku.

### 2. Custom Tools

MCP enables Antigravity to execute specific, safe actions defined by your connected servers.

**Example:** "Create a Linear issue for this TODO."

**Example:** "Search Notion or GitHub for authentication patterns."

## How to Connect

Connections are managed directly through the built-in MCP Store.

1. **Access the Store:** Open the MCP Store panel within the "..." dropdown at the top of the editor's side panel.
2. **Browse & Install:** Select any of the supported servers from the list and click Install.
3. **Authenticate:** Follow the on-screen prompts to securely link your accounts (where applicable).

Once installed, resources and tools from the server are automatically available to the editor.

## Connecting Custom MCP Servers

To connect to a custom MCP server:

1. Open the MCP store via the "..." dropdown at the top of the editor's agent panel.
2. Click on "Manage MCP Servers"
3. Click on "View raw config"
4. Modify the mcp_config.json with your custom MCP server configuration.

The configuration file is located at `~/.gemini/antigravity/mcp_config.json`.

### Configuration Structure

The configuration file has a single `mcpServers` object where you define each server you want to connect to.

```json
{
  "mcpServers": {
    "serverName": {
      "command": "path/to/executable",
      "args": ["--arg1", "value1"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

### Configuration Properties

Each server entry supports the following properties:

**Transport (one required):**

- **`command`** (string): Path to the executable for stdio transport.
- **`serverUrl`** (string): URL for remote servers for Streamable HTTP transport.

**Optional:**

- **`args`** (string[]): Command-line arguments for stdio transport.
- **`env`** (object): Environment variables for the stdio server process.
- **`cwd`** (string): Working directory for stdio servers.
- **`headers`** (object): Custom HTTP headers for remote servers.
- **`authProviderType`** (string): Authentication provider. Supports `"google_credentials"` for ADC.
- **`oauth`** (object): OAuth client credentials (`clientId`, `clientSecret`).
- **`disabled`** (boolean): Temporarily disable a server without removing its configuration.
- **`disabledTools`** (string[]): Tool names to not provide to the model.

## Authentication

### Google Credentials

Set `authProviderType` to `"google_credentials"` to use Google Application Default Credentials (ADC).

```json
{
  "mcpServers": {
    "my-gcp-service": {
      "serverUrl": "https://example.googleapis.com/mcp/",
      "authProviderType": "google_credentials"
    }
  }
}
```

This requires Application Default Credentials to be configured. To set them up, run:

```bash
gcloud auth application-default login
```

### OAuth

Antigravity can automatically handle OAuth for servers that support dynamic client registration (DCR). For these servers, no additional configuration is needed:

```json
{
  "mcpServers": {
    "oauth-server": {
      "serverUrl": "https://api.example.com/mcp/"
    }
  }
}
```

If the server does not support dynamic client registration, you can provide your client credentials manually:

```json
{
  "mcpServers": {
    "oauth-server": {
      "serverUrl": "https://api.example.com/mcp/",
      "oauth": {
        "clientId": "your-client-id",
        "clientSecret": "your-client-secret"
      }
    }
  }
}
```

If you provided client credentials manually, ensure the following is registered as a redirect URI in your OAuth provider:

```
https://antigravity.google/oauth-callback
```

When connecting to an OAuth-enabled server:

1. Open **Agent Settings** with `Cmd+,` (Mac) or `Ctrl+,` (Windows/Linux).
2. Navigate to the **Customizations** tab and click the **Authenticate** button next to the server.

![Click Authenticate](assets/image/docs/tools/mcp-oauth-authenticate.png)

3. Complete authentication in your browser and copy the authorization code.

![Copy authorization code](assets/image/docs/tools/mcp-oauth-copy-code.png)

4. Paste the code back into the settings panel and click **Submit**.

![Paste auth code](assets/image/docs/tools/mcp-oauth-paste-code.png)

Once authenticated, the server will reconnect automatically.

![Authenticated server](assets/image/docs/tools/mcp-oauth-authenticated.png)

Access tokens are stored in `~/.gemini/antigravity/mcp_oauth_tokens.json`. Expired tokens are refreshed automatically, and invalid tokens are removed.

### Custom Headers

For servers that require custom HTTP headers (e.g. API keys or bearer tokens), add them to the `headers` object. For example:

```json
{
  "mcpServers": {
    "my-remote-server": {
      "serverUrl": "https://api.example.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

## Supported Servers

The MCP Store currently features integrations for:

- Airweave
- Arize
- AlloyDB for PostgreSQL
- Atlassian
- BigQuery
- Chrome DevTools
- ClickHouse
- Cloud SQL for PostgreSQL
- Cloud SQL for MySQL
- Cloud SQL for SQL Server
- Dart
- Dataplex
- Figma Dev Mode MCP
- Firebase
- GitHub
- Harness
- Heroku
- Linear
- Locofy
- Looker
- MCP Toolbox for Databases
- MongoDB
- Neon
- Netlify
- Notion
- PayPal
- Perplexity Ask
- Pinecone
- Postman
- Prisma
- Redis
- Sequential Thinking
- SonarQube
- Spanner
- Stripe
- Supabase

---

# Agent Skills

Skills are an [open standard](https://agentskills.io/home) for extending agent capabilities. A skill is a folder containing a `SKILL.md` file with instructions that the agent can follow when working on specific tasks.

## What are skills?

Skills are reusable packages of knowledge that extend what the agent can do. Each skill contains:

- **Instructions** for how to approach a specific type of task  
- **Best practices** and conventions to follow  
- **Optional scripts and resources** the agent can use

When you start a conversation, the agent sees a list of available skills with their names and descriptions. If a skill looks relevant to your task, the agent reads the full instructions and follows them.

## Where skills live

Antigravity supports two types of skills:

| Location | Scope |
| :---- | :---- |
| `<workspace-root>/.agents/skills/<skill-folder>/` | Workspace-specific |
| `~/.gemini/antigravity/skills/<skill-folder>/` | Global (all workspaces) |

**Workspace skills** are great for project-specific workflows, like your team's deployment process or testing conventions.

**Global skills** work across all your projects. Use these for personal utilities or general-purpose tools you want everywhere.

Note: Antigravity now defaults to .agents/skills, but still maintains backward support for .agent/skills. 

## Creating a skill

To create a skill:

1. Create a folder for your skill in one of the skill directories  
2. Add a `SKILL.md` file inside that folder

```
.agents/skills/
└─── my-skill/
    └─── SKILL.md
```

Every skill needs a `SKILL.md` file with YAML frontmatter at the top:

```
---
name: my-skill
description: Helps with a specific task. Use when you need to do X or Y.
---

# My Skill

Detailed instructions for the agent go here.

## When to use this skill

- Use this when...
- This is helpful for...

## How to use it

Step-by-step guidance, conventions, and patterns the agent should follow.
```

### Frontmatter fields

| Field | Required | Description |
| :---- | :---- | :---- |
| `name` | No | A unique identifier for the skill (lowercase, hyphens for spaces). Defaults to the folder name if not provided. |
| `description` | Yes | A clear description of what the skill does and when to use it. This is what the agent sees when deciding whether to apply the skill. |

Tip: Write your description in third person and include keywords that help the agent recognize when the skill is relevant. For example: "Generates unit tests for Python code using pytest conventions."

## Skill folder structure

While `SKILL.md` is the only required file, you can include additional resources:

```
.agents/skills/my-skill/
├─── SKILL.md       # Main instructions (required)
├─── scripts/       # Helper scripts (optional)
├─── examples/      # Reference implementations (optional)
└─── resources/     # Templates and other assets (optional)
```

The agent can read these files when following your skill's instructions.

## How the agent uses skills

Skills follow a **progressive disclosure** pattern:

1. **Discovery**: When a conversation starts, the agent sees a list of available skills with their names and descriptions  
2. **Activation**: If a skill looks relevant to your task, the agent reads the full `SKILL.md` content  
3. **Execution**: The agent follows the skill's instructions while working on your task

You don't need to explicitly tell the agent to use a skill—it decides based on context. However, you can mention a skill by name if you want to ensure it's used.

## Best practices

### Keep skills focused

Each skill should do one thing well. Instead of a "do everything" skill, create separate skills for distinct tasks.

### Write clear descriptions

The description is how the agent decides whether to use your skill. Make it specific about what the skill does and when it's useful.

### Use scripts as black boxes

If your skill includes scripts, encourage the agent to run them with `--help` first rather than reading the entire source code. This keeps the agent's context focused on the task.

### Include decision trees

For complex skills, add a section that helps the agent choose the right approach based on the situation.

## Example: A code review skill

Here's a simple skill that helps the agent review code:

```
---
name: code-review
description: Reviews code changes for bugs, style issues, and best practices. Use when reviewing PRs or checking code quality.
---

# Code Review Skill

When reviewing code, follow these steps:

## Review checklist

1. **Correctness**: Does the code do what it's supposed to?
2. **Edge cases**: Are error conditions handled?
3. **Style**: Does it follow project conventions?
4. **Performance**: Are there obvious inefficiencies?

## How to provide feedback

- Be specific about what needs to change
- Explain why, not just what
- Suggest alternatives when possible
```

---

# Rules

Rules are manually defined constraints for the Agent to follow, at both the local and global levels. Rules allow users to guide the agent to follow behaviors particular to their own use cases and style.

To get started with Rules:
1. Open the Customizations panel via the "..." dropdown at the top of the editor's agent panel.
2. Navigate to the Rules panel.
3. Click **+ Global** to create new Global Rules, or **+ Workspace** to create new Workspace-specific rules.

A Rule itself is simply a Markdown file, where you can input the constraints to guide the Agent to your tasks, stack, and style.

Rules files are limited to 12,000 characters each.

## Global Rules

Global rules live in ~/.gemini/GEMINI.md and are applied across all workspaces.

## Workspace Rules

Workspace rules live in the .agents/rules folder of your workspace or git root.

At the rule level you can define how a rule should be activated:

- Manual: The rule is manually activated via at mention in Agent’s input box.
- Always On: The rule is always applied.
- Model Decision: Based on a natural language description of the rule, the model decides whether to apply the rule.
- Glob: Based on the glob pattern you define (e.g., *.js, src/**/*.ts), the rule will be applied to all files that match the pattern.

Note: Antigravity now defaults to .agents/rules, but still maintains backward support for .agent/rules. 

## @ Mentions

You can reference other files using @filename in a Rules file. If filename is a relative path, it will be interpreted relative to the location of the Rules file. If filename is an absolute path, it will be resolved as a true absolute path, otherwise it will be resolved relative to the repository. For example, @/path/to/file.md will first attempt to be resolved to /path/to/file.md, and if that file does not exist, it will be resolved to workspace/path/to/file.md.

# Workflows

Workflows enable you to define a series of steps to guide the Agent through a repetitive set of tasks, such as deploying a service or responding to PR comments. These Workflows are saved as markdown files, allowing you to have an easy repeatable way to run key processes. Once saved, Workflows can be invoked in Agent via a slash command with the format /workflow-name.

While Rules provide models with guidance by providing persistent, reusable context at the prompt level, Workflows provide a structured sequence of steps or prompts at the trajectory level, guiding the model through a series of interconnected tasks or actions.

To create a workflow:

1. Open the Customizations panel via the "..." dropdown at the top of the editor's agent panel.
2. Navigate to the Workflows panel.
3. Click the **+ Global** button to create a new global workflow that can be accessed across all your workspaces, or click the **+ Workspace** button to create a workflow specific to your current workspace.

To execute a workflow, simply invoke it in Agent using the /workflow-name command. You can call other Workflows from within a workflow! For example, /workflow-1 can include instructions like “Call /workflow-2” and “Call /workflow-3”. Upon invocation, Agent sequentially processes each step defined in the workflow, performing actions or generating responses as specified.

Workflows are saved as markdown files and contain a title, a description and a series of steps with specific instructions for Agent to follow. Workflow files are limited to 12,000 characters each.

## Agent-Generated Workflows

You can also ask Agent to generate Workflows for you! This works particularly well after manually working with Agent through a series of steps since it can use the conversation history to create the Workflow.

---

# Hooks

Hooks allow you to run custom scripts or shell commands at specific points during Antigravity's execution loop. This is powerful for enforcing custom rules, running linters, or capturing diagnostics automatically.

## Configuration

Hooks are configured in a `hooks.json` file located in your customization directory (e.g., `.agents/` in your workspace or `~/.gemini/config/`).

## Schema and File Format

The `hooks.json` file maps hook names to their event configurations.

```json
{
  "my-linter-hook": {
    "PostToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/lint.sh",
            "timeout": 10
          }
        ]
      }
    ]
  },
  "safety-gate": {
    "enabled": false,
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "command": "./scripts/safety-check.sh"
          }
        ]
      }
    ]
  },
  "reminder": {
    "PreInvocation": [
      {
        "type": "command",
        "command": "./scripts/reminder.sh"
      }
    ]
  }
}
```

### Hook Definition Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `enabled` | boolean | Optional. Set to `false` to disable the hook without removing it. Defaults to `true`. |
| `PreToolUse` | array | Handlers that run before a tool is executed. |
| `PostToolUse` | array | Handlers that run after a tool completes. |
| `PreInvocation` | array | Handlers that run before Antigravity calls the model. |
| `PostInvocation` | array | Handlers that run after tool calls finish. |
| `Stop` | array | Handlers that run when the execution loop terminates. |

## Supported Events

| Event | Description | Matcher Target |
| :--- | :--- | :--- |
| `PreToolUse` | Fires before a tool is executed. | Tool name (e.g., `run_command`) |
| `PostToolUse` | Fires after a tool completes. | Tool name |
| `PreInvocation` | Fires before the model is called. | N/A (matcher ignored) |
| `PostInvocation` | Fires after tool calls finish. | N/A (matcher ignored) |
| `Stop` | Fires when execution terminates. | N/A (matcher ignored) |

### Matcher

For `PreToolUse` and `PostToolUse`, you can use a regular expression in the `matcher` field to specify which tools trigger the hook:

* `""` or `"*"`: Match all tools.  
* `"run_command"`: Match exactly `run_command`.  
* `"run_command|view_file"`: Match either tool.  
* `"browser_.*"`: Match any tool starting with `browser_`.

<Announcement>
icon: info
iconColor: var(--theme-primary)
color: var(--theme-surface-surface-container)
text: **Note**: For `PreInvocation`, `PostInvocation`, and `Stop`, the structure is simpler (a list of handlers directly under the event key) and the matcher is ignored.
</Announcement>

## Supported Tools

For `PreToolUse` and `PostToolUse` matchers, you can match against the following tool names, grouped by category:

### File and Directory Operations

* **`view_file`**: View the contents of a file.  
  * Arguments: `AbsolutePath`, `StartLine` (optional), `EndLine` (optional), `IsSkillFile` (optional)  
* **`write_to_file`**: Create new files.  
  * Arguments: `TargetFile`, `Overwrite`, `CodeContent`, `Description`, `IsArtifact` (optional), `ArtifactMetadata` (optional)  
* **`replace_file_content`**: Edit a single contiguous block of text in a file.  
  * Arguments: `TargetFile`, `Instruction`, `Description`, `AllowMultiple`, `TargetContent`, `ReplacementContent`, `StartLine`, `EndLine`, `TargetLintErrorIds` (optional)  
* **`multi_replace_file_content`**: Make multiple, non-contiguous edits to the same file.  
  * Arguments: `TargetFile`, `Instruction`, `Description`, `ReplacementChunks` (array of chunks), `TargetLintErrorIds` (optional), `ArtifactMetadata` (optional)  
* **`list_dir`**: List the contents of a directory.  
  * Arguments: `DirectoryPath`  
* **`find_by_name`**: Search for files and directories using glob patterns.  
  * Arguments: `SearchDirectory`, `Pattern`, `Type` (optional), `Excludes` (optional), `Extensions` (optional), `FullPath` (optional), `MaxDepth` (optional)

### Search and Research

* **`grep_search`**: Fast text searches within specific paths.  
  * Arguments: `SearchPath`, `Query`, `IsRegex` (optional), `CaseInsensitive` (optional), `Includes` (optional), `MatchPerLine` (optional)  
* **`search_web`**: Perform a general web search.  
  * Arguments: `query`, `domain` (optional)  
* **`read_url_content`**: Fetch text content of a public URL.  
  * Arguments: `Url`

### System and Execution

* **`run_command`**: Propose a bash command to run.  
  * Arguments: `CommandLine`, `Cwd`, `WaitMsBeforeAsync`, `RunPersistent` (optional), `RequestedTerminalID` (optional)  
* **`manage_task`**: Interact with background tasks.  
  * Arguments: `Action` (`'list'`, `'kill'`, `'status'`, `'send_input'`), `TaskId` (optional), `Input` (optional)  
* **`schedule`**: Set timers or recurring cron jobs.  
  * Arguments: `DurationSeconds` (optional), `CronExpression` (optional), `MaxIterations` (optional), `Prompt`  
* **`list_permissions`**: View current resource access grants.  
  * Arguments: None  
* **`ask_permission`**: Request additional scoped permissions.  
  * Arguments: `Action`, `Target`, `Reason`

### Agent Collaboration

* **`invoke_subagent`**: Spawn specialized sub-agents.  
  * Arguments: `Subagents` (array of specs with `Prompt`, `Role`, `TypeName`, `Workspace` (optional))  
* **`define_subagent`**: Create a custom sub-agent.  
  * Arguments: `name`, `description`, `system_prompt`, `enable_mcp_tools` (optional), `enable_write_tools` (optional), `enable_subagent_tools` (optional)  
* **`send_message`**: Communicate with other agents.  
  * Arguments: `Recipient`, `Message`  
* **`manage_subagents`**: List or terminate active sub-agents.  
  * Arguments: `Action` (`'list'`, `'kill'`, `'kill_all'`), `ConversationIds` (optional)

### Interaction and Media

* **`ask_question`**: Ask multiple-choice questions.  
  * Arguments: `questions` (array of questions with `question`, `options`, `is_multi_select`)  
* **`generate_image`**: Create or edit images.  
  * Arguments: `Prompt`, `ImageName`, `ImagePaths` (optional)

## Hook Handler Configuration

Each item in the `hooks` array supports:

| Field | Type | Description |
| :--- | :--- | :--- |
| `type` | string | Optional. Currently only `"command"` is supported. Defaults to `"command"`. |
| `command` | string | Required. The shell command to execute. |
| `timeout` | integer | Optional. Timeout in seconds. Defaults to `30`. |

## Input/Output Contract

Hooks receive input via **stdin** as JSON and should return output via **stdout** as JSON. Field names use camelCase.

### Common Input Fields

All hooks receive the following system metadata fields in their input payload on `stdin`:

| Field | Type | Description |
| :--- | :--- | :--- |
| `conversationId` | string | The unique UUID of the active agent conversation. |
| `workspacePaths` | array of strings | Absolute directory paths representing the user's mounted workspaces. |
| `transcriptPath` | string | The absolute path to the persistent `transcript.jsonl` conversation logs. |
| `artifactDirectoryPath` | string | The absolute path to the directory containing all conversation artifacts and screenshots. |

---

### PreToolUse

Fires before a tool is executed.

#### Schema

**Input Fields (stdin)**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `toolCall` | object | Details of the proposed tool call. |
| `toolCall.name` | string | The name of the tool being executed (e.g., `run_command`). |
| `toolCall.args` | object | The arguments passed to the tool. |
| `stepIdx` | integer | The 0-based index of the current step in the trajectory. |
| *(Common Fields)* | | Includes `conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`. |

**Output Fields (stdout)**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `decision` | string | **Required.** Controls how the tool call is gated:<br>- `"allow"`: Automatically allows the tool execution.<br>- `"deny"`: Hard blocks execution immediately.<br>- `"ask"`: Prompts the user, but respects "Always Allow" settings.<br>- `"force_ask"`: Always prompts the user, ignoring cached permissions. |
| `reason` | string | **Optional.** The explanation shown to the agent or user for the decision. |
| `permissionOverrides` | array of strings | **Optional.** A list of resource strings (e.g. `["read_file(/path)", "command(args)"]`) to override default tool permissions. |

#### Example

* **Input (stdin)**:

```json
{
  "toolCall": {
    "name": "run_command",
    "args": {
      "CommandLine": "npm test",
      "Cwd": "/workspace/project",
      "WaitMsBeforeAsync": 5000
    }
  },
  "stepIdx": 19,
  "conversationId": "ec33ebf9-0cba-4100-8142-c61503f6c587",
  "workspacePaths": ["/workspace/project"],
  "transcriptPath": "/workspace/project/.gemini/jetski/transcript.jsonl",
  "artifactDirectoryPath": "/workspace/project/.gemini/jetski/artifacts"
}
```

* **Output (stdout)**:

```json
{
  "decision": "ask",
  "reason": "Requires confirmation for test execution.",
  "permissionOverrides": ["command(npm test)"]
}
```

---

### PostToolUse

Fires after a tool completes.

#### Schema

**Input Fields (stdin)**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `stepIdx` | integer | The 0-based index of the completed step. |
| `error` | string | Optional. The detailed runtime error message if the tool call failed. Empty if successful. |
| *(Common Fields)* | | Includes `conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`. |

**Output Fields (stdout)**: Returns an empty JSON object `{}`.

#### Example

* **Input (stdin)**:

```json
{
  "stepIdx": 5,
  "error": "exit status 1",
  "conversationId": "ec33ebf9-0cba-4100-8142-c61503f6c587",
  "workspacePaths": ["/workspace/project"],
  "transcriptPath": "/workspace/project/.gemini/jetski/transcript.jsonl",
  "artifactDirectoryPath": "/workspace/project/.gemini/jetski/artifacts"
}
```

* **Output (stdout)**: `{}`

---

### PreInvocation

Fires before the model is called.

#### Schema

**Input Fields (stdin)**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `invocationNum` | integer | The sequence number of the current model invocation. |
| `initialNumSteps` | integer | The number of steps currently in the trajectory. |
| *(Common Fields)* | | Includes `conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`. |

**Output Fields (stdout)**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `injectSteps` | array of objects | **Optional.** List of steps to inject into the conversation trajectory before the model is called. |

*Injected Step Schema*: Each object in the `injectSteps` array can have one of the following fields:

* `toolCall` (object): A tool call to execute.  
* `userMessage` (string): A message from the user.  
* `ephemeralMessage` (string): A transient system message.

#### Example

* **Input (stdin)**:

```json
{
  "invocationNum": 3,
  "initialNumSteps": 10,
  "conversationId": "ec33ebf9-0cba-4100-8142-c61503f6c587",
  "workspacePaths": ["/workspace/project"],
  "transcriptPath": "/workspace/project/.gemini/jetski/transcript.jsonl",
  "artifactDirectoryPath": "/workspace/project/.gemini/jetski/artifacts"
}
```

* **Output (stdout)**:

```json
{
  "injectSteps": [{"ephemeralMessage": "Remember to lint"}]
}
```

---

### PostInvocation

Fires after tool calls finish.

#### Schema

**Input Fields (stdin)**: Same as `PreInvocation` input fields.

**Output Fields (stdout)**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `injectSteps` | array of objects | **Optional.** List of steps to inject after the invocation completes (same schema as `PreInvocation` inject steps). |
| `terminationBehavior` | string | **Optional.** Controls the execution flow after injection:<br>- `"force_continue"`: Forces the loop to continue.<br>- `"terminate"`: Forces the loop to terminate.<br>- `""` (or omitted): Default behavior. |

#### Example

* **Input (stdin)**: Same as `PreInvocation`  
* **Output (stdout)**:

```json
{
  "injectSteps": [],
  "terminationBehavior": ""
}
```

---

### Stop

Fires when the execution loop terminates.

#### Schema

**Input Fields (stdin)**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `executionNum` | integer | The sequence number of the execution attempt. |
| `terminationReason` | string | The reason why the execution is stopping (e.g., `"model_stop"`, `"max_steps_exceeded"`, `"error"`). |
| `error` | string | Optional. The error message if termination was caused by a system error. |
| `fullyIdle` | boolean | **Required.** `true` if the agent is completely finished and all background commands or asynchronous tasks have completed. `false` if active background tasks are still running. |
| *(Common Fields)* | | Includes `conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`. |

**Output Fields (stdout)**:

| Field | Type | Description |
| :--- | :--- | :--- |
| `decision` | string | **Required.** Set to `"continue"` to prevent the agent from stopping and re-enter the execution loop. Any other value allows the stop. |
| `reason` | string | **Optional.** If `decision` is `"continue"`, this message is injected as a system message into the conversation. |

#### Example

* **Input (stdin)**:

```json
{
  "executionNum": 1,
  "terminationReason": "model_stop",
  "error": "",
  "fullyIdle": true,
  "conversationId": "ec33ebf9-0cba-4100-8142-c61503f6c587",
  "workspacePaths": ["/workspace/project"],
  "transcriptPath": "/workspace/project/.gemini/jetski/transcript.jsonl",
  "artifactDirectoryPath": "/workspace/project/.gemini/jetski/artifacts"
}
```

* **Output (stdout)**:

```json
{
  "decision": "continue",
  "reason": "Not done yet"
}
```

---

### Sidecars  

Sidecars are background processes that run alongside Antigravity. Antigravity manages the lifecycle of sidecars, automatically launching them and restarting them if they crash or error.  
They are useful for persistent background scripts, scheduled recurring tasks, and reacting to events.

#### Configuration

Sidecars are discovered by searching for `sidecar.json` configuration files. They can be defined in two locations:

- Global sidecars: Under `~/.gemini/config/sidecars/`  
- Plugin sidecars: Under `~/.gemini/config/plugins/<pluginName>/sidecars/`

Each sidecar has its own directory and the directory name is used as the sidecar’s ID. Sidecars loaded from plugins have the ID `<pluginName>/<sidecarName>`. 

The sidecar’s directory must contain a `sidecar.json` file and may also contain other helper files like scripts to run. The sidecar’s directory also acts as the current working directory for the sidecar’s command.

Example directory structure

```
~/.gemini/config/sidecars/
├── sidecar1/
│   ├── sidecar.json
│   └── script.py
└── sidecar2/
    └── sidecar.json

~/.gemini/config/plugins/
└── my-plugin/
      └── sidecars/
            └── plugin-sidecar/
                  └── sidecar.json
```

##### Config Schema (sidecar.json)

*   **`command`** (string): Command/executable (e.g., `python3` or `/bin/bash` ). Mutually exclusive with `builtin`.  
*   **`builtin`** (string): Builtin command to execute. Currently supports `schedule`. Mutually exclusive with `command`.  
*   **`args`** (string[]): Optional. Arguments passed to the command or builtin function.  
*   **`restart_policy`** (string): Optional. Restart behavior. One of `always`, `on-failure`, or  `never`. Defaults to `always`.  
*   **`description`** (string): Optional. Human-readable description of what the sidecar does.  
*   **`env`** (object): Optional. Map of environment variables to set for the sidecar process.  
*   **`display_name`** (string): Optional. Display name used in the UI.

One of `command` or `builtin` must be set.

Examples:

```json
{
  "description": "Background worker",
  "command": "python3",
  "args": ["worker.py"],
  "restart_policy": "on-failure"
}
```

```json
{
  "description": "Hourly agent to triage review requests.",
  "builtin": "schedule",
  "args": [
    "0 * * * *",
    "agentapi",
    "new-conversation",
    "Give me a summary of incoming review requests."
  ]
}
```

##### User Configuration (config.json)

Sidecars are disabled unless explicitly enabled by the user in the global configuration file, located at `~/.gemini/config/config.json`.

*   **`enabled`** (boolean): Whether the sidecar is enabled.  
*   **`projectId`** (string): Optional. The ID of the project `agentapi` will create conversations in.

Example:

```json
{
  "sidecars": {
    "sidecar1": {
      "enabled": true
    },
    "my-plugin/plugin-sidecar": {
      "enabled": true,
      "projectId": "<projectId>"
    }
  }
}
```

##### Runtime Data

Runtime data produced by sidecars are stored in `~/.gemini/antigravity/sidecar_data/<sidecarId>/`.

This includes:  
*   **`data/`**: Subdirectory for any persistent data. This path is available via the `ANTIGRAVITY_EXECUTABLE_DATA_DIR` environment variable.  
*   **`logs/`**: Auto-generated timestamped logs from stdout and stderr.  
*   **`events/`**: JSON files recorded for `agentapi` calls.

##### `schedule` builtin

`schedule` is a simple builtin scheduler for running recurring commands.

```json
{
  "builtin": "schedule",
  "args": [
    "* * * * *",
    "<command>",
    "<arg1>",
    "<arg2>"
  ]
}
```

The first argument is a standard 5-field cron expression. The remaining arguments are the command and arguments to run on the specified schedule.

##### `agentapi`

Sidecars can use the `agentapi` CLI to programmatically interact with Antigravity. The executable is automatically added to the sidecar’s path and available as `agentapi`.

*   `agentapi new-conversation <prompt>`  
    Sidecars creating conversations must have a `projectId` set.
*   `agentapi send-message <conversation_id> <prompt>`

---

## Artifacts

# Artifacts

An **Artifact** is a structured deliverable created by the agent to accomplish its task and communicate its progress and thinking to the human user. Artifacts include rich markdown plans (Implementation Plans), code diffs, architecture diagrams, images, and browser recordings.

As agents become more autonomous and execute complex tasks over longer periods, Artifacts enable asynchronous collaboration. You do not need to carefully monitor every individual tool call or step synchronously; instead, you review high-level deliverables at key milestones.

## Reviewing Artifacts Across Surfaces

Artifacts are primarily generated during the agent's **Planning Mode** and are accessible across both Antigravity 2.0 and the Antigravity CLI.

### Antigravity 2.0 
The desktop app features a visual sidebar and review pane specifically optimized for displaying, organizing, and managing rich Artifacts. 
*   **Capabilities**: You can inspect interactive plans, review visual code diffs, and play back browser recordings of the agent's UI actions directly within the app interface.

### Antigravity CLI
In the lightweight terminal interface, Artifacts are managed using a fast, keyboard-driven review panel.
*   **Workflow**: When the agent generates or modifies files that require your approval, a notification appears in your terminal status bar.

## Interactive Steering and Feedback

Feedback is a core mechanism of the Artifact workflow. Depending on your configuration, the agent will pause at intermediate milestones and request review on its plans or code edits before executing them.

*   **Steering the Agent**: If an artifact (like an Implementation Plan) does not align with your goal, you can provide inline text feedback to steer the agent's thinking in the proper direction before it modifies any local files.
*   **Granular Control**: This approval loop ensures that you remain in the driver's seat, allowing the agent to operate with high autonomy while maintaining strict human-in-the-loop validation.

---

# Task List

A task list is an artifact that the agent uses to approach complex tasks and monitor progress on various action items. You can find a live snapshot of what the agent is doing in this artifact, which is constructed as a markdown list of items related to research, implementation, verification, and more. This type of artifact is generally used by the agent to keep on track with the user’s overarching goal; typically, you do not need to directly interact with this artifact.

![Task List](assets/image/docs/artifacts/artifact-task.png)

---

# Implementation Plan

Agent utilizes the implementation plan artifact to architect changes within your codebase to accomplish a task. These plans contain technical details on what revisions are necessary and are meant to be reviewed by the user. Below is an example plan generated by the agent.

![Artifact Implementation Plan](assets/image/docs/artifacts/artifact-implementation-plan.png)

Unless you have you artifact review policy set to “Always Proceed” [link to docs on this setting], Agent will typically request your review on the implementation plan before making the changes needed to complete your task. You can click either the in-conversation or artifact header “Proceed” button to instantly continue with Agent’s plan.

![Artifact Implementation Plan Proceed](assets/image/docs/artifacts/artifact-implementation-plan-proceed.png)

Oftentimes, Agent will create a plan that is slightly different from what you exactly want. Antigravity supports commenting on these artifacts so you can provide feedback to Agent for any reason, whether it be to decrease scope of changes, use a different tech stack, or correct any Agent discrepancies.

![Artifact Implementation Plan Comments](assets/image/docs/artifacts/artifact-implementation-plan-comments.png)
 
Once you have left comments on the implementation plan, you can still use the “Proceed” to continue with Agent’s plan; alternatively, you can also toggle the “Review” button in the artifact header, where you can examine all comments and leave a message as feedback instead of directly proceeding, if needed.

![Artifact Implementation Plan Submit Comments](assets/image/docs/artifacts/artifact-implementation-plan-submit-comments.png)

Once you have proceeded or left a review, Agent will continue its work, either iterating on the implementation plan and re-requesting your review or beginning with its work!

![Artifact Implementation Plan Proceeded](assets/image/docs/artifacts/artifact-implementation-plan-proceeded.png)

---

# Walkthrough

Agent creates walkthrough artifacts when it has completed task implementation; this type of artifact includes a concise summary of the changes that have been made to remind the user of what has happened in the active conversation. This is a great way to get up to speed with the state of your codebase after Agent has made its changes in case you were not strictly following it the whole time.

![Walkthrough](assets/image/docs/artifacts/artifact-walkthrough.png)

For browser tasks, walkthroughs often contain screenshots and screen recordings of what Agent has built or created in the browser!

![Walkthrough with Image](assets/image/docs/artifacts/artifact-walkthrough-image.png)

---

# Screenshots

The browser subagent can take screenshots of open pages or elements on pages when it would like your review of the state of the page. This is surfaced as a tool to the agent, and you can also prompt the agent to take a screenshot of a page.

![Browser Screenshot Capture Tool](assets/image/docs/artifacts/browser-screenshot-capture.png)

All screenshots are saved as image artifacts and can be commented on to give feedback to the agent.

![Browser Screenshot Artifact](assets/image/docs/artifacts/browser-screenshot-artifact.png)

---

# Browser Recordings

Every time the browser subagent actuates on the Browser, it may choose to generate a recording of the agent’s actions for your review. You can view this playback, if it is available, at the bottom of the Browser step UI.

![Browser Recording Capture Tool](assets/image/docs/artifacts/browser-recording-capture.png)

All browser recordings are also saved as a recording artifact for your review. This view loops through the browser agent’s actions.

![Browser Recording Artifact](assets/image/docs/artifacts/browser-recording-artifact.png)

---

# Knowledge

Knowledge Items are Antigravity's persistent memory system that automatically captures and organizes important insights, patterns, and solutions from your coding sessions. They help you build upon previous work across conversations.

## What is a Knowledge Item?

A Knowledge Item is a collection of related information on a specific topic. Each Knowledge Item contains a title and summary describing what it covers, and a collection of artifacts providing information on the topic. Possible examples of artifacts include automatically generated documentation, code examples, or persistent memories of user instructions. 

## How are Knowledge Items Generated?

As you interact with the agent, Antigravity automatically analyzes and extracts information from your conversation and uses that information to create new KIs or update existing KIs. 

## Viewing Knowledge Items

You can view your Knowledge Items in the Antigravity **Agent Manager**.

![Knowledge View](assets/image/docs/artifacts/knowledge-view.png)

## How are Knowledge Items used by the Agent?

The summaries of all your Knowledge Items are available to the agent, which uses them to inform its responses. When the agent identifies a Knowledge Item that is relevant to the conversation, it will automatically study the artifacts in that Knowledge Item and use the applicable information.

---

## Agent Manager

# Agent Manager

We've built out the Agent Manager, to provide a higher level view into the work Antigravity agents are doing under your guidance. Here, you can work across multiple workspaces, oversee dozens of agents simultaneously, and interact with your codebase primarily through the agent, rather than through writing code directly. As agents and models continue to get better, we believe that this birds-eye view will be the primary entry point to all of your work. We expect to move it to be central to the Antigravity experience soon.

At any point, you can toggle between the Agent Manager and the editor by hitting CMD+E (Mac) or CTRL+E (Windows), or through the Open Editor & Open Agent Manager buttons at the top right of the menu bar. You can also manage your editor windows through the manager, either hiding, focusing, or closing them.

![Agent Manager Editor](assets/image/docs/agent_manager_editor.png)

---

# Workspaces

In the Agent Manager, you can work across multiple workspaces simultaneously. In order to open a new workspace, just select the button in the left sidebar and select a starting folder. At any point, you can switch between conversations across workspaces through the left sidebar.

![Switch Workspaces](../../../assets/image/docs/workspaces/switch_workspace.png)

To start a new conversation within a workspace, either select the desired workspace from the Start Conversation tab or hit the Plus button next to the workspace name in the sidebar.

![Start Conversation Within Workspace](../../../assets/image/docs/workspaces/start_within_workspace.png)

---

# Playground

Playgrounds are independent workspaces that allow you to start a conversation and explore ideas instantly, without the overhead of setting up a new workspace.

## Creating a Playground

From the Start Conversation page, you can quickly send a message to a new playground by clicking the Use Playground button below the input box.

![Playground Button](../../../assets/image/docs/playground/playground_button.png)

From here, you can send a message as you would normally.

![Playground Send Message](../../../assets/image/docs/playground/playground_send.png)

## Persisting Your Work

If you want to keep the work you've done in a playground, you can move its contents into a dedicated workspace in a folder of your choosing. This action preserves your conversation history and any files created during your session, allowing you to continue exploring with multiple conversations.

![Playground Persist](../../../assets/image/docs/playground/playground_persist.png)

Clicking on the move button in the top bar will pop up the following modal:

![Playground Move Modal](../../../assets/image/docs/playground/playground_move.png)

---

# Inbox

The inbox is your one stop shop to track all of your conversations in one place. From the inbox you can see if any of your conversations are awaiting your approval to run terminal commands, use the browser, or build out an implementation plan.

![Inbox Overview](../../../assets/image/docs/inbox/basic_inbox.png)

You can use the search bar and the pending switch to search for conversations by folder or by title to make sure your inbox is always focused on what is most relevant to you.

Selecting a conversation from the inbox will jump directly to the conversation, where you can continue where you left off.

![Continue Conversation](../../../assets/image/docs/inbox/continue_conversation.png)

---

# Conversation View

The [Agent Panel](/docs/agent-side-panel) takes center stage in the agent manager. As the agent makes progress, you'll be able to follow along with what it's doing. To toggle off this follow-along mode, simply hit the `Following` button at the top right of the conversation.

![Follow Along Manager](assets/image/docs/follow_along_manager.png)

---

# Browser Subagent View

## Overview

The Manager has a dedicated side panel that allows you to expand and inspect the Agent’s work for a task.

![Browser Subagent View](assets/image/docs/browser-subagent-view.png)

In the regular manager conversation view (left half of the image), the browser subagent’s work is hidden.
Clicking the expand button (shown in red box) will bring up the subagent view (right half of the image). Updates to the Agent’s work will be streamed into this view, so you can follow along and interact with steps as required (e.g. confirm/deny actions).

## What’s in the side panel

- All subagent actions (clicking, scrolling, navigating, etc.)
- Visual feedback showing exactly where clicks happened
- Screenshots captured at each step

## Visual Inspection Feature

Tool calls that produce actions in the browser, like clicks, include a button (shown in blue box) which opens a screenshot of the browser at that exact moment and a red dot showing what interaction the agent has done in the browser.

---

# Panes

You can open files, [artifacts](/docs/artifacts), knowledge items, and other content directly within the manager in panes that persist per-conversation. In order to open up a pane, simply open up the quick picker (by hitting CMD+P on Mac or CTRL+P on Windows/Linux) and select a resource. You can also hit the "+" from within a conversation's header.

![Manager New Tab](assets/image/docs/agent-manager/manager_new_tab.png)

![Manager File Picker](assets/image/docs/agent-manager/manager_file_picker.png)

These panes are resizable, splittable, and drag-and-droppable. You should configure them around as makes sense for your workflow.

![Manager Split Pane](assets/image/docs/agent-manager/manager_split_pane.png)

If you use CMD+Click or CMD+Enter (Mac) or CTRL+Click / CTRL+Enter (non-Mac), the contents will open in a new pane, rather than replacing the currently open pane.

---

# Review Changes + Source Control

Just as in the [editor](/docs/review-changes-editor), you can easily review the work you and your agent have collaborated on from within the manager.

Once you enter a conversation, you can toggle the Review Changes pane through the button at the top right to open up a pane where you can scroll through and comment on any file diffs made as a part of the conversation.

![Review Changes Manager](assets/image/docs/review_changes_manager.png)

You can similarly toggle to the Source Control tab within the Review Changes pane to see changed files, stage or unstage them, and commit them upstream.

![Manager Source Control](assets/image/docs/manager_source_control.png)

---

# Changes Sidebar

Similar to the toolbar at the bottom of the editor's [Agent Panel](docs/agent-side-panel), the Changes Sidebar in the manager offers a quick way to see what [artifacts](docs/artifacts) the agent has created and what files it has modified within a conversation.

Clicking on any of the listed resources will open its contents within a pane. The icons on each resource indicate whether there are new changes to a resource since your last review.

![Aux Sidebar](assets/image/docs/aux-sidebar.png)

---

# Terminal

The agent manager window has terminal support as well! To toggle this, use Cmd/Ctrl + J to open the bottom pane of the agent manager, which is where terminals live. They are attached to the workspace that your current conversation is in.

**Note:** Agent manager window's terminal integration works for local workspaces only, and Agent-used terminals run inside the editor window.

![agent-manager-terminal](assets/image/docs/agent-manager-terminal.png)

---

# Files

As you open up [file panes](/docs/panes) within the manager, you can also leave comments for the agent to highlight specific points.

![File commenting manager](assets/image/docs/file_commenting_manager.png)

---

## Browser

# Antigravity Browser

Google Antigravity can open, read, and actuate a local Chrome browser, enabling you to test development websites, read documentation sources, and automate a variety of browser tasks.

---

## Core Mechanisms

Using the specialized [Browser Subagent](/docs/subagents), Antigravity operates on browser tabs as needed, capturing screenshots and saving action videos as interactive artifacts.

To completely disable browser tools, you can toggle the **Browser Tools** setting in the "Browser" section of the User Settings.

---

## Security: Allowlist & Denylist

The browser enforces a two-layer security model to control URL access:
1. **Denylist**: Real-time check against Google's server-side database to block known dangerous or malicious hostnames.
2. **Allowlist**: A customizable local text file initialized with `localhost`. If the agent tries to open a non-allowlisted page, a dialog will prompt you to approve and add the domain to your trusted allowlist.

---

## Isolated Profile

To protect your personal data, the agent executes inside a completely separate, isolated Chrome profile:
- **Cookie Isolation**: Does not share cookies, history, or active sessions from your primary Google Chrome profile.
- **Persistence**: All credentials and cookies entered in the agentic browser profile remain persisted across sessions.
- **Dock Isolation**: Renders as a separate application icon in your macOS dock when your primary browser is open.

---

# Allowlist / Denylist

The browser uses a two-layer security system to control which URLs can be accessed:
- **Denylist** - Deny dangerous/malicious URLs
- **Allowlist** - Explicitly allow trusted URLs

## How It Works

### Denylist
The denylist is maintained and enforced using the Google Superroots’s BadUrlsChecker service (See documentation).
When the browser attempts to navigate to a URL, the hostname is checked against the server-side denylist via RPC.

**NOTE:** If the server is unavailable, access is denied by default.

### Allowlist

The allowlist is a local text file that you can edit to explicitly trust specific URLs.

![Allowlist](assets/image/docs/browser-allowlist.png)

The allowlist is initialized with just localhost, and can be edited at anytime.

When the browser attempts to navigate to a non-allowlisted URL, it will prompt you with an “always allow” button, which if clicked will add the URL to the allowlist and enable the browser to open and interact with the web page. An example situation is shown below:

![Always Allow](assets/image/docs/always-allow-url.png)

You can also add/remove URLS from the allowlist manually. However, the denylist always takes precedence: you cannot allowlist a URL that appears on the denylist.

---

# Separate Chrome Profile

To isolate the browser from your general browsing, it operates on a [separate Chrome profile](https://support.google.com/chrome/answer/2364824).

Since Chrome profiles are isolated, this will not share any of the cookies or sign-in information from your normal browsing profile. However, all sign-ins will be persisted such that anytime you open the browser in the future, all your accounts will still be there. 

If you had your normal Chrome open while launching this profile, it will show up as a separate dock icon and be considered a separate application. If Chrome was not open beforehand, this application will look the same as your default profile. To return to the default profile, you must quit the application and relaunch Chrome.

If you would like to change the location where your browser profile will be created, you can modify the following setting in the browser section.

![Browser Profile](../../../assets/image/docs/browser/browser-profile.png)

---

## Enterprise

# Getting Started with Antigravity and Gemini Enterprise Agent Platform

This guide is for administrators setting up the Google Cloud environment to enable Antigravity integration with Gemini Enterprise Agent Platform. This integration allows enterprise developers to use Antigravity with models hosted in your own Google Cloud project, under Google Cloud Terms of Service, satisfying private networking and data residency requirements, and utilizing consumption-based billing.

## Basic Setup

### Prerequisites

Before you begin, ensure you have:

* A Google Cloud account.  
* Access to the Google Cloud console.

### Step 1: Select or Create a Google Cloud Project

In the Google Cloud console, on the project selector page, select or create a Google Cloud project.

### Roles Required to Select or Create a Project

* **Select a project**: Selecting a project doesn't require a specific IAM role—you can select any project that you've been granted a role on.  
  
  <Announcement>
  icon: info
  iconColor: var(--theme-primary)
  color: var(--theme-surface-surface-container)
  text: **Note**: To switch to a different Google Cloud project or location, you must first log out of the Antigravity CLI or Hub, then log back in and select your new project/location. Directly changing the project or location while logged in is currently not supported.
  </Announcement>
  
* **Create a project**: To create a project, you need the **Project Creator** role (`roles/resourcemanager.projectCreator`), which contains the `resourcemanager.projects.create` permission. [Learn how to grant roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).

<Announcement>
icon: info
iconColor: var(--theme-primary)
color: var(--theme-surface-surface-container)
text: **Note**: If you don't plan to keep the resources that you create in this procedure, create a new project instead of selecting an existing project. After you finish these steps, you can delete the project to remove all associated resources.
</Announcement>

[Go to project selector](https://console.cloud.google.com/projectselector2)

### Step 2: Verify Billing

Verify that billing is enabled for your Google Cloud project. You can check the billing status in the [Google Cloud Billing Console](https://console.cloud.google.com/billing). For detailed instructions, see [Verify the billing status of your projects](https://cloud.google.com/billing/docs/how-to/verify-billing-enabled).

### Step 3: Enable the Agent Platform API

To use Antigravity with Gemini Enterprise Agent Platform, you must enable the Agent Platform API (`aiplatform.googleapis.com`).

### Roles Required to Enable APIs

To enable APIs, you need the **Service Usage Admin** IAM role (`roles/serviceusage.serviceUsageAdmin`), which contains the `serviceusage.services.enable` permission. [Learn how to grant roles](https://cloud.google.com/iam/docs/granting-changing-revoking-access).

### Enable the API

[Enable the Agent Platform API in the API Library](https://console.cloud.google.com/apis/library/aiplatform.googleapis.com)

### User Permissions

To get the permissions that you need to use Gemini Enterprise Agent Platform, ask your administrator to grant you the **Agent Platform User** (`roles/aiplatform.user`) IAM role on your project. For more information about granting roles, see [Manage access to projects, folders, and organizations](https://cloud.google.com/iam/docs/granting-changing-revoking-access).

You might also be able to get the required permissions through [custom roles](https://cloud.google.com/iam/docs/creating-custom-roles) or other [predefined roles](https://cloud.google.com/iam/docs/roles-overview#predefined).

## Advanced Configuration

### Request and Response Logging

For detailed instructions on how to enable and configure request and response logging for the Gemini Enterprise Agent Platform, please refer to the official documentation:

[Request and Response Logging Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/request-response-logging)

### VPC Service Controls (VPC-SC)

If your organization has a service perimeter, then you must add the following resources to your perimeter:

* Agent Platform API

For detailed instructions on how to configure VPC Service Controls, please refer to the official documentation:

[VPC Service Controls Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/general/vpc-service-controls)

## Complementary Resources

### Consumption Options

Gemini Enterprise Agent Platform offers different consumption options to suit your needs.

For detailed information on consumption options, please refer to the official documentation:

[Consumption Options Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/deploy/consumption-options)

### Deployments and Endpoints Locations

For now, Antigravity CLI and 2.0 offer 3 endpoints: global, multi-region eu, and multi-region us.

<Announcement>
icon: info
iconColor: var(--theme-primary)
color: var(--theme-surface-surface-container)
text: **Note**: Image generation is currently not available in `eu` and `us` locations.
</Announcement>

For a full list of available locations and deployment endpoints, please refer to the official documentation:

[Deployment Endpoints Documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/locations#global)

---

## Plans

# Plans

At this moment, Google Antigravity is available with [terms](https://antigravity.google/terms) to individual accounts derived from Google's terms of service, and available to teams under GCP terms through the Gemini Enterprise Agent Platform. To learn more, see Enterprise Get Started
Rate limits and model availability differs based on usage of [Google AI](https://one.google.com/about/google-ai-plans/) plans.

## Baseline Quota

All plans receive a baseline of:

* Use of Gemini models including Gemini 3.1 Pro, Gemini 3.5 Flash, and other offered Gemini Enterprise Agent Platform models as the core agent model
* Unlimited Tab completions
* Access to all product features, such as the Scheduled Tasks and the CLI

Users on Google AI Ultra receive:

* The highest, most generous quota, refreshed every five hours
* Highest weekly rate limits
* Access to third-party models

Users on Google AI Pro receive:

* High, generous quota, refreshed every five hours until weekly limit reached
* Higher weekly rate limit

Users not on AI Pro and Ultra plans receive:

* Meaningful quota, refreshed weekly
* Weekly rate limit

The baseline rate limits are primarily determined to the degree we have capacity, and exist to prevent abuse. Under the hood, the rate limits are correlated with the amount of work done by the agent, which can differ from prompt to prompt. Thus, you may get many more prompts if your tasks are more straightforward and the agent can complete the work quickly, and the opposite is also true.

Usage limits for this service are subject to modification. These adjustments may be necessary to manage system capacity and maintain service stability.

## Overages

Users on Google AI Pro or Ultra plans can utilize [purchased AI credits](http://one.google.com/ai/credits) (or any one-time promotional credits) for additional overage usage above the baseline provided quota. AI credits are consumed at standard Gemini Enterprise Agent Platform consumption pricing.

Usage of credits once the baseline quota is exhausted for any particular model is controlled by the "AI Credit Overages" user setting, which can be set to the following:

* Never: Never use AI credits automatically, wait until the baseline quota refreshes before using this model further
* Always: Always use AI credits when the baseline quota is exhausted (will switch back automatically to using the baseline quota once the refresh hits)

Baseline quota usage across models can be viewed in the settings page.

## Other

There is currently no support for:

* Bring-your-own-key or bring-your-own-endpoint for additional rate limits
* Organizational tiers via contract

---

## Settings

# Settings

## Antigravity 2.0 Settings 

Antigravity 2.0 features a hierarchical settings architecture designed to give you granular control over your development environment. Settings are split between Global application preferences and isolated Project-level boundaries to ensure robust security and flexible workspace configurations.

### Accessing Settings

You can open the Settings panel in Antigravity 2.0 using the following methods:

* **Keyboard Shortcut**: Press `Cmd + ,` on any active surface inside the application.  
* **Sidebar Navigation**: Click Settings at the bottom of the left sidebar.  
* **Project Settings**: Click the Gear Icon located next to a specific project.  
    
<Announcement>
icon: info
iconColor: var(--theme-primary)
color: var(--theme-surface-surface-container)
text: **Note**: By default, if you have an active project open, clicking Settings will automatically open the configurations for that specific project. Otherwise, it will open the global settings.
</Announcement>

### The Four Settings Categories

Settings are organized into four distinct scopes to keep configurations clean and isolated:

**1. Global Settings**

These are global settings that apply to everything:

* Account Settings: Manage authentication sessions and toggle Telemetry (enable/disable sharing interaction logs to improve models).  
* Global Permissions: Centralized default tool boundaries that apply to all conversations.  
* Appearance: Customize visual themes and panel layouts.  
* Browser Integration: Configure how the agent interacts with web surfaces.  
* Model Usage: Choose and configure default reasoning models.  
* Customizations: Manage Model Context Protocol (MCP) servers, custom skills, and "Build with Google" plugins.

**2. Project Settings**

These settings apply exclusively within the scope of a specific Project:

* Folders: Define the list of local folders associated with the project. Antigravity automatically detects Git configurations for these folders to handle conversation targets:  
  * Local: Select this in the new conversation view to work directly in the existing folders.  
  * Worktree: Select this to start a new worktree in the folders. (Note: If a folder does not have Git, the existing local folder is used instead).  
* Agent Settings: Configure project-specific agent behaviors:  
  * Terminal Execution Policy: Control how the agent runs shell commands.  
  * Outside of Folder File Access Policy: Define how the agent accesses files outside the project boundary (Always Allow, Always Ask, or Always Deny).  
  * Sandbox Mode: Toggle the terminal sandbox container on or off within the custom security preset.  
* Project-level Permissions: Configure permissions at the project level. As you interact with an agent, you will accumulate permission requests that can be automatically added to the project permissions.  
* Customizations: Derived from both global customizations and project-specific ones. You can view all skills originating from each folder added to the project.

**3. Conversations Outside of a Project**

You can also start conversations outside of a project (standalone conversations):

* Behavior: These conversations do not have a configurable folder and instead run in a local scratch directory.  
* Settings: They can have their own settings (such as terminal execution, file access policies, and permissions) similar to projects, but operate independently of any project structure.

**4. Miscellaneous**

* Shortcuts: View and customize keyboard shortcut configurations.  
* Feedback: Access the feedback form to send reports directly to the team.

## IDE Settings

You can configure your Antigravity settings across Agent, Browser, Editor, and more via:

* Keyboard shortcut in any surface: `Cmd + ,`
* From the Settings tab or gear icon in the Agent Manager
* From "Settings > Open Antigravity User Settings" in the Editor

### Data Collection Settings

The "Enable Telemetry" setting can be found in the Settings panel under the "Account" section. When toggled on, Antigravity collects interactions for use in evaluating, developing, and improving Antigravity and models that support Antigravity.

---

## FAQ

# FAQ

## Why can I not authenticate into Google Antigravity?

Google Antigravity is currently available for personal Google accounts in approved geographies. Please try using an @gmail.com email address if having challenges with Workspace Google accounts.

## Why is my age unverified?

At the moment, Antigravity is unavailable to under-18 users. If you do meet the minimum age requirement, you may [verify your age](https://myaccount.google.com/age-verification) to continue using Antigravity.

## What is Google Antigravity’s geographical availability?
Google Antigravity is available in the following countries and territories. If you're not in one of these countries or territories, you will be unable to use Google Antigravity at this time:

**Important**: Please check the country listed on the [Google Terms of Service](https://policies.google.com/terms) page. If this is the wrong country, you may [submit a request](https://policies.google.com/country-association-form) to change your associated region.

Americas
- American Samoa
- Anguilla
- Antigua and Barbuda
- Argentina
- Aruba
- The Bahamas
- Barbados
- Belize
- Bermuda
- Bolivia
- Brazil
- British Virgin Islands
- Canada
- Caribbean Netherlands
- Cayman Islands
- Chile
- Colombia
- Costa Rica
- Curaçao
- Dominica
- Dominican Republic
- Ecuador
- El Salvador
- Falkland Islands (Islas Malvinas)
- Greenland
- Grenada
- Guatemala
- Guyana
- Haiti
- Honduras
- Jamaica
- Mexico
- Montserrat
- Nicaragua
- Panama
- Paraguay
- Peru
- Puerto Rico
- Saint Barthélemy
- Saint Kitts and Nevis
- Saint Lucia
- Saint Pierre and Miquelon
- Saint Vincent and the Grenadines
- South Georgia and the South Sandwich Islands
- Suriname
- Trinidad and Tobago
- Turks and Caicos Islands
- United States
- Uruguay
- U.S. Virgin Islands
- Venezuela

Europe
- Albania
- Armenia
- Austria
- Azerbaijan
- Belgium
- Bosnia and Herzegovina
- Bulgaria
- Croatia
- Cyprus
- Czech Republic
- Denmark
- Estonia
- Faroe Islands
- Finland
- France
- Georgia
- Germany
- Gibraltar
- Greece
- Guernsey
- Hungary
- Iceland
- Ireland
- Isle of Man
- Italy
- Jersey
- Kosovo
- Latvia
- Liechtenstein
- Lithuania
- Luxembourg
- Malta
- Montenegro
- Netherlands
- North Macedonia
- Norway
- Poland
- Portugal
- Romania
- Serbia
- Slovakia
- Slovenia
- Spain
- Sweden
- Switzerland
- Ukrainian territories other than Crimea, the so-called Donetsk People's Republic ("DNR"), and the so-called Luhansk People's Republic ("LNR")
- United Kingdom

Africa
- Algeria
- Angola
- Benin
- Botswana
- Burkina Faso
- Burundi
- Cabo Verde
- Cameroon
- Central African Republic
- Chad
- Comoros
- Côte d'Ivoire
- Democratic Republic of the Congo
- Djibouti
- Egypt
- Equatorial Guinea
- Eritrea
- Eswatini
- Ethiopia
- Gabon
- The Gambia
- Ghana
- Guinea
- Guinea-Bissau
- Kenya
- Lesotho
- Liberia
- Libya
- Madagascar
- Malawi
- Mali
- Mauritania
- Mauritius
- Morocco
- Mozambique
- Namibia
- Niger
- Nigeria
- Republic of the Congo
- Rwanda
- Saint Helena, Ascension and Tristan da Cunha
- São Tomé and Príncipe
- Senegal
- Seychelles
- Sierra Leone
- Somalia
- South Africa
- South Sudan
- Sudan
- Tanzania
- Togo
- Tunisia
- Uganda
- Western Sahara
- Zambia
- Zimbabwe

Asia
- Bahrain
- Bangladesh
- Bhutan
- British Indian Ocean Territory
- Brunei
- Cambodia
- Christmas Island
- Cocos (Keeling) Islands
- India
- Indonesia
- Iraq
- Israel
- Japan
- Jordan
- Kazakhstan
- Kuwait
- Kyrgyzstan
- Laos
- Lebanon
- Malaysia
- Maldives
- Mongolia
- Nepal
- Oman
- Pakistan
- Palestine
- Philippines
- Qatar
- Saudi Arabia
- Singapore
- South Korea
- Sri Lanka
- Taiwan
- Tajikistan
- Thailand
- Timor-Leste
- Türkiye
- Turkmenistan
- United Arab Emirates
- Uzbekistan
- Vietnam
- Yemen

Oceania
- Australia
- Cook Islands
- Fiji
- Guam
- Heard Island and McDonald Islands
- Kiribati
- Marshall Islands
- Micronesia
- Nauru
- New Caledonia
- New Zealand
- Niue
- Norfolk Island
- Northern Mariana Islands
- Palau
- Papua New Guinea
- Pitcairn Islands
- Samoa
- Solomon Islands
- Tokelau
- Tonga
- Tuvalu
- United States Minor Outlying Islands
- Vanuatu
- Wallis and Futuna

Antarctica
- Antarctica

## Why am I ineligible for a Google One AI plan?

The following regions do not currently have access to Google One AI plans:

- Antarctica
- Brunei
- Caribbean Netherlands
- Curaçao
- Democratic Republic of the Congo
- Eswatini
- Falkland Islands (Islas Malvinas)
- Faroe Islands
- Greenland
- Guernsey
- Heard Island and McDonald Islands
- Isle of Man
- Jersey
- Kosovo
- Montenegro
- New Caledonia
- Pitcairn Islands
- Republic of the Congo
- Saint Barthélemy
- Saint Helena, Ascension and Tristan da Cunha
- Saint Kitts and Nevis
- Saint Vincent and the Grenadines
- São Tomé and Príncipe
- South Georgia and the South Sandwich Islands
- South Sudan
- Sudan
- The Gambia
- Türkiye
- United States Minor Outlying Islands
- U.S. Virgin Islands
- Wallis and Futuna


## What is Google Antigravity’s stance on data collection?
Please refer to the [Terms of Service](/terms). You may opt out of data collection at any point from the Settings panel.

## How do I sign in with a GCP project?

Follow the steps in the [Enterprise Page](/docs/enterprise) to learn how to sign in with GCP.

## How do I get support?
Check out the communities on our [Support page](/support).

## What are the model rate limits?
Please see more details in the docs on [Plans](/docs/plans).

## Why can’t I use third party software (e.g. Claude Code, OpenClaw, OpenCode) with my Antigravity login?

Using third party software, tools, or services to access Antigravity is a violation of our [Terms of Service](/terms), and severely degrades the experience for legitimate product users. Such actions may be grounds for suspension or termination of your account. If you would like to use a third party coding agent with Gemini, we recommend using a Vertex or AI Studio API key.

## Does Google Antigravity currently support worktrees?
Yes, you can use worktrees in Antigravity 2.0.

## What happens when my computer goes to sleep?
If an agent is running, Antigravity will prevent your computer from sleeping.

---
