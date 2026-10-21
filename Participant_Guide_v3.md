# Participant guide
NSF Year 1 workshop, session 1 of 3

## Start with an empty folder

Create `workshop-project` on your Desktop in Finder (macOS) or File Explorer (Windows). In VS Code choose File > Open Folder and select it. This opens the actual folder on disk.

The `completed-project` folder is a reference what we should have completed by the end of the session and recovery option.

## Prep

Install VS Code from https://code.visualstudio.com/download and create a github account (ideally before the session). First thing we'll do is add Microsoft's Python and Jupyter extensions. Next, we will install Git.

On macOS:

Type git --version in terminal. 

Git may already be installed or macOS may prompt you to install the Command Line Developer Tools.

If no installation prompt appears and Git isn't available, run: xcode-select --install

On Windows, use PowerShell in VS Code's terminal:

1. Run `git --version`. If a version appears, Git is already installed.
2. Otherwise, run:

```powershell
winget install --id Git.Git -e --source winget
```

3. Follow the prompts. After installation, close and reopen VS Code, open a new terminal, and run `git --version` again.
4. If winget is unavailable, download and run the installer from https://git-scm.com/install/windows.

Installing Git does not sign in to GitHub. VS Code handles GitHub access later, when publishing the repository.




(see: https://git-scm.com/downloads)

Run the commands below in VS Code’s terminal. 

Install uv:

macOS/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Windows PowerShell (one line):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
These commands download and run the official installer. Reopen your terminal or restart VS Code afterward. Check `uv --version` and `git --version`; each should show a version number.

## Create the Python project

Terminal > New Terminal. Run `pwd` to check your location and `ls` to list contents. You should be in your new workshop-project folder. `cd name` enters a folder and `cd ..` moves up a level.

New to the terminal? See Software Carpentry's [terminal command reference](https://swcarpentry.github.io/shell-novice/reference.html). It describes Unix shells. The four navigation commands above also work in Windows PowerShell, although other commands and flags in that reference may differ.

Run one line at a time:
```bash
uv python install 3.12
uv init --python 3.12 --no-package 
uv add pandas matplotlib ipykernel
```
The first obtains Python. 

The second creates project settings and initializes a local Git repository. We will use Git later to record versions of the project. `--no-package` keeps the setup focused on scripts and notebooks. It skips the extra files and settings for making our own code an installable Python package. 

A note: We can still install packages, analyze data, and build on this project. Packaging becomes useful if we want other projects to install and import our own code—for example, a collection of analysis functions shared across several studies. We can add that setup later if needed.

The third records dependencies and installs them into `.venv`. This is an environment, not a container or virtual machine.

Recognize these files:
- `.venv`: your local Python environment and installed packages. Do not commit it.
- `pyproject.toml`: project details and dependency requirements.
- `uv.lock`: resolved dependency versions.
- `.python-version`: Python version selection.

Our `uv add` command has already installed the packages needed for this exercise. No additional setup command is needed here. The configuration files let you or a collaborator set up the project's environment on another computer. We will explain that process after publishing to GitHub.

## Run a script

uv init creates `main.py`. Open it, replace its contents, and save:
```python
print("My project is running")
```
In the terminal:
```bash
uv run python main.py
```
Expected: `My project is running`. In the Command Palette, use Python: Select Interpreter to choose the project's `.venv` for script tooling. The notebook kernel selection below is separate.

## Create a notebook

1. Command Palette: Cmd+Shift+P on macOS or Ctrl+Shift+P on Windows.
2. Choose Create: New Jupyter Notebook.
3. Save it as `analysis.ipynb` inside workshop-project, beside pyproject.toml.
4. Add a Markdown cell with `# Practice analysis`. Run it to render the heading.
5. Add a Code cell for Python instructions. A new notebook may already contain one. Use + Markdown / + Code, or the cell type picker, to create or change cells.
6. Click Select Kernel at the top right.
7. Choose Python Environments.
8. Select `.venv` inside this project folder.

If the first menu shows recently used kernels instead of Python Environments, choose Select Another Kernel to reach that menu.

We installed ipykernel so the Python in our project’s .venv can execute notebook cells. Select that environment as the notebook’s kernel so the notebook uses our project’s Python and installed packages. The kernel keeps variables in memory until it restarts or shuts down. Shift+Enter runs a cell; saving the notebook is a separate action.



### First code cell: check the selected Python

This is a setup check: confirm that the notebook uses the project's Python and can import pandas before starting the analysis.

```python
import sys # Access information about the running Python
import pandas as pd # Load pandas under the name pd

print(sys.executable) # Path to Python running this notebook
print(pd.__version__) # Optional: show the pandas version
```

Run the cell with Shift+Enter. The path should point into this project's `.venv`. On macOS/Linux it usually ends in `.venv/bin/python`; on Windows, `.venv\Scripts\python.exe`. If it points elsewhere, select this project's kernel and run the cell again.

`sys` comes with Python and lets us check which Python is running. Importing pandas confirms it is available to this kernel and makes the name `pd` available for our later `pd.read_csv` call. Printing the pandas version is optional information for troubleshooting; there is no version number to memorize.

## Add the data

In VS Code Explorer create a folder named `data` inside workshop-project. Put the supplied `practice.csv` in it using Finder/File Explorer. Dragging a file onto an editor tab may only open it, so verify its location on disk.

Open `data/practice.csv` in VS Code. CSV means comma-separated values: a plain text file with column names in the header and values in rows. The input has participant, condition, rt_ms. rt_ms is response time in milliseconds.

The task is a toy Stroop example. Imagine participants identifying font color while ignoring a word. Matching word/color information is congruent; conflicting information is incongruent. Each row is one invented participant's average across trials, with three participants in each condition. Do not infer a real behavioral effect or effect size from these six invented values.

## Optional: create the same data yourself

You can skip this section and use the supplied CSV. These optional cells recreate exactly the same values and labels. A DataFrame is a table in Python memory. The CSV is a file on disk.

A dictionary maps column names to lists of values:

```python
import pandas as pd

data = pd.DataFrame({
    "participant": [1, 2, 3, 4, 5, 6],
    "condition": [
        "congruent", "congruent", "congruent",
        "incongruent", "incongruent", "incongruent"],
    "rt_ms": [400, 500, 600, 500, 600, 700]
})
data
```

Quotes mark strings, square brackets contain lists, and braces enclose a dictionary. All lists here have six values. `pd.DataFrame` constructs the table and assigns it to the name data.

Save it:

```python
from pathlib import Path

Path("data").mkdir(exist_ok=True)
data.to_csv("data/practice.csv", index=False)
```

`index=False` leaves out pandas' automatic row index. pathlib comes with Python. mkdir creates data if needed. to_csv overwrites an existing file at the same path, so here it replaces the supplied CSV with equivalent content. Open the saved file to inspect the header and rows.

## Main analysis

Use one new code cell for each step below. Even if you created the table manually, load the CSV so everyone follows the same remaining workflow.

### Load the CSV

```python
data = pd.read_csv("data/practice.csv")
print(data)
```

pd.read_csv reads the file and creates a DataFrame in memory. `data` names that table. `print(data)` displays it. The relative file path assumes the notebook is running from the project root.

### Calculate the means

```python
means = data.groupby("condition")["rt_ms"].mean()
print(means)
```

Group rows by condition, select rt_ms, then calculate the mean. Expected: congruent = 500 ms, incongruent = 600 ms. Each condition has three observations.

### Plot and save

```python
from pathlib import Path
import matplotlib.pyplot as plt

Path("outputs").mkdir(exist_ok=True)
means.plot.bar(ylabel="Mean reaction time (ms)", rot=0)
plt.title("Practice data")
plt.tight_layout()
plt.savefig("outputs/means.png")
plt.show()
```

Open outputs/means.png in Explorer. Edit the plot title, rerun the cell, and inspect the saved file. Saving edits alone does not update output.

## Project organization

Use Explorer to locate the parts of the project:

- `data/practice.csv`: the input CSV.
- `analysis.ipynb`: the notebook containing explanations, code, and saved results.
- `outputs/means.png`: the figure generated by the plot cell. Rerun that cell to update the file after changing the plotting code.
- `README.md`: a description of the project and instructions for running it.
- `pyproject.toml`, `uv.lock`, and `.python-version`: the environment configuration, kept beside the notebook at the project’s top level.

Keep `main.py` at the top level as our earlier script example. `.venv` is the installed environment; do not move its internal files manually. No extra file moves are needed if your folder already matches this layout.

Open `README.md`, replace its placeholder text with the following or your own description, and save:

```markdown
# Stroop practice analysis

This project compares two conditions using six invented participant mean response times.
Open analysis.ipynb in VS Code, select this project's .venv as the kernel,
and run the cells from top to bottom.
Expected means: congruent 500 ms; incongruent 600 ms.
```

The `#` marks a Markdown heading. GitHub will display this README on the repository's main page after publication.

## Notebook state and errors

Restart the kernel, then run the summary before loading data: expect NameError. Restart clears variables from memory. Run all cells in order to recreate them. Old output can remain visible after a restart.

### Read and correct an error

Read the last error message, then find the line of code that failed in the traceback. The error type tells you what to check.

FileNotFoundError practice:

1. In the loading cell, temporarily change `data/practice.csv` to `data/practice_typo.csv` and run the cell.
2. Find the missing filename in the error message. Compare it with the filename shown under `data` in Explorer.
3. Restore `data/practice.csv` and rerun the cell.
4. If the spelling matches but the file still cannot be found, check the notebook's working folder:

```python
from pathlib import Path
print(Path.cwd())
```

`data/practice.csv` is relative to that folder. For our layout, the working folder should be `workshop-project`.

NameError practice:

1. In a temporary new cell, run `print(menas)`. Python reports that `menas` is not defined.
2. Correct it to `print(means)` and run again.
3. If `means` is still undefined, run the cell that calculates it. Restarting the kernel clears variables, even when old displayed outputs remain visible.
4. Delete the temporary practice cell afterward.

ModuleNotFoundError:

- Check the spelling in the import statement.
- To check which Python is running even when importing pandas fails, run `import sys` followed by `print(sys.executable)` in a separate code cell. Select this project's `.venv` if the path points elsewhere.
- If pandas is actually missing from the correct environment, run `uv add pandas` in the project terminal, restart the notebook kernel, and run the notebook from the beginning. Avoid installing into an unrelated Python.

For `uv not found`, reopen the terminal or restart VS Code, then follow the installer's PATH instructions if needed.

Restore the correct code after the deliberate errors and check the known means: 500 ms and 600 ms.

## README and Git

Git records versions locally. GitHub hosts a repository online so you can share files and commits. A repository contains the files Git tracks and their recorded history.

Our earlier `uv init` command already initialized a Git repository in `workshop-project`. We do not need to initialize it again. Nothing has been uploaded to GitHub yet.

The README was written during the project-organization step. Check that it is saved before staging the project files.

### Review .gitignore

uv created `.gitignore` in the project folder. Open it, keep its existing contents, and paste these lines at the bottom. Repeated rules are harmless. Save the file.

```text
.venv/
outputs/
__pycache__/
.ipynb_checkpoints/
.env
.DS_Store
```

Copy only the six patterns above into `.gitignore`, one per line. The explanations below are separate from the file's contents. To add a comment in `.gitignore`, place `#` at the beginning of its own line.

- `.venv/`: the local Python installation and packages. Installed files and paths can depend on the computer and operating system. Share the configuration files so each computer can install its own environment.
- `outputs/`: generated figures we can recreate by running the notebook. Excluding this folder is a choice for this exercise. Other projects may track selected results or final figures. This pattern does not remove saved outputs embedded inside `analysis.ipynb`.
- `__pycache__/`: Python-generated bytecode caches that Python can recreate.
- `.ipynb_checkpoints/`: Jupyter-generated checkpoint copies, separate from the main notebook. This folder might not appear in our VS Code exercise.
- `.env`: a file often used for local settings, passwords, or API keys. We do not create one in this exercise; this rule is a precaution for a file with that exact name.
- `.DS_Store`: macOS folder-display settings that are not part of the analysis.

A trailing slash indicates a folder. These rules affect untracked files. They do not remove files already committed or guarantee that every private file is excluded. We track `.gitignore` itself so collaborators receive the same rules.

### Set Git identity

In the terminal inside `workshop-project`, replace the examples with the author name and email you want attached to your commits:

```bash
git config user.name "Your Name"
git config user.email "your-chosen-email@example.com"
```

These settings apply to this repository. Your author name does not need to match your GitHub username. To connect commits to your GitHub profile, use an email associated with your account or the private email GitHub provides under Settings > Emails. The chosen name and email become part of commit history.

Commits record this name and email as their author. GitHub sign-in lets VS Code upload commits to your online account. Setting the author information does not sign in or upload anything. When publishing, VS Code can ask you to sign in through the browser; it may already have access if you signed in earlier.

Keep the quoted name and email in the commands. Do not put `#` before them: that would make the values a shell comment instead of setting them.

### Record the first commit

Save writes edits to disk. Stage selects the current file contents for the next commit. Commit records that selection in local Git history.

1. Save your edited files.
2. In the terminal, run `git status`. This reports the current branch and files Git sees as new or changed. Untracked means Git has not started tracking a file.
3. Open Source Control from the left sidebar, or choose View > Source Control.
4. Click each file under Changes to inspect it. Hover over its name and click **+** to stage it. The file should move under Staged Changes.
5. Include these files:
   - `.gitignore`
   - `.python-version`
   - `pyproject.toml`
   - `uv.lock`
   - `README.md`
   - `main.py`
   - `analysis.ipynb`
   - `data/practice.csv`
6. Check that `.venv` and `outputs` are excluded. If you edit a file after staging it, stage it again to include the latest edits.
7. Enter `Add practice analysis` in the commit message box and click Commit.
8. Run `git status` again. If you committed all intended changes, it should report a clean working tree.
9. Run `git log --oneline`. You should see your commit message beside a short commit identifier.

This commit exists on your computer. It has not been uploaded yet.

Optional terminal alternative to staging and committing through VS Code:

```bash
git add .gitignore .python-version pyproject.toml uv.lock README.md main.py analysis.ipynb data/practice.csv
git diff --cached
git commit -m "Add practice analysis"
git status
```

Use either the interface or these equivalent commands. You do not need to do both. If the diff opens in a terminal viewer, press `q` to close the viewer.

## Publish to your GitHub account

VS Code can create the GitHub repository and upload your local commits. You do not need to create an empty repository on the GitHub website first.

1. Keep your original `workshop-project` folder open in VS Code.
2. Open the Command Palette: Cmd+Shift+P on macOS or Ctrl+Shift+P on Windows.
3. Search for **Publish to GitHub** and select it.
4. If prompted, complete GitHub sign-in and authorization in your browser, then return to VS Code. Check that you are using your own account.
5. Name the repository `workshop-project`. If that name already exists in your account, choose another, such as `workshop-project-practice`.
6. Choose a private repository for this exercise. Public repositories are viewable by anyone. Private repositories require access.
7. Finish publication. If a file-selection prompt appears, review the included files. Wait for publication to finish.

Publish to GitHub creates a new online repository, connects the local repository to it, and uploads your commits. Git calls the saved connection a remote, normally named `origin`. Publish Branch is a different operation for a repository that already has a remote.

### Find your project online

1. In your browser, sign in at https://github.com.
2. Open your profile menu, choose Your repositories, and open `workshop-project` or the name you chose. You can also use Open on GitHub if VS Code offers it after publishing.
3. Check that the top of the page shows your username and repository name.
4. Open `analysis.ipynb` and `data/practice.csv`. Read the README on the main page. Check that `pyproject.toml`, `uv.lock`, and `.python-version` are present.
5. Open the commits list near the latest commit information. Find `Add practice analysis`.

GitHub can display saved notebook code and outputs. Viewing the notebook there does not run Python. The ignored `.venv` and `outputs` folders should be absent.

## Review a change

1. Return to `analysis.ipynb` in your original local project.
2. Replace the existing plot-title line with:

```python
plt.title("Stroop practice: response times")
```

3. Rerun the plot cell, then save the notebook. If the kernel was restarted, run earlier cells first so `means` exists.
4. Open Source Control. Under Changes, click `analysis.ipynb`.
5. Inspect the diff, which compares the saved edits with the last committed version. Find the changed title. Saved outputs or notebook metadata may also differ.

The GitHub copy has not changed yet. Saving changes locally does not upload them.

## Commit and push the update

1. In Source Control, click **+** beside `analysis.ipynb` and check that it moves under Staged Changes.
2. Enter `Update plot title` in the commit message box and click Commit. This records a new local version.
3. Open the Command Palette and run **Git: Push**. Push uploads the commit to the GitHub repository connected during publication.
4. Wait for completion, then refresh your GitHub repository page.
5. Open the commits list and find `Update plot title`. Open `analysis.ipynb` and locate the new title in its code or saved output.

Push sends commits, so save, stage, and commit first. For this exercise, use Git: Push explicitly. VS Code's Sync Changes action can both pull and push.

`git log --oneline` shows your local commits. `git remote -v` shows the connected GitHub address if you want to inspect it.

## Clone: get a local copy of an existing repository

Cloning is useful when you want your project on another computer or want to work with a collaborator's shared project. It copies the tracked files and Git history into a local folder. Viewing a repository in the browser does not create that folder.

Optional practice: simulate another computer by making a second copy on this computer. Keep it separate from the original project.

1. On your GitHub repository page, select **Code > HTTPS** and copy the repository URL with the copy button.
2. Create a folder on your Desktop named `workshop-copies`. Keep it outside the original `workshop-project` folder.
3. In VS Code, choose File > New Window.
4. In the new window, open the Command Palette and run **Git: Clone**.
5. Paste the repository URL.
6. When asked where to store it, choose `workshop-copies`. VS Code creates a repository folder inside that destination.
7. Open the cloned project when prompted. Confirm Explorer contains `analysis.ipynb`, `data`, and `pyproject.toml`.

On another computer, install Git before cloning. For a private repository, sign in with an account that has access. Cloning someone else's repository does not grant permission to push to it.

### Set up the cloned project's environment with uv sync

Cloning downloaded the project’s tracked files, including analysis.ipynb and its configuration files. It did not download .venv, because we excluded that folder using .gitignore.
1. In the cloned project’s VS Code window, choose Terminal > New Terminal.
2. Run: `uv sync`

uv reads the project’s configuration and installs its dependencies into a local .venv. uv must already be installed on this computer.

3. In Explorer on the left, open analysis.ipynb.
4. Run the first code cell. The path printed by print(sys.executable) should point inside workshop-copies/workshop-project/.venv.
5. If the path points somewhere else, click the kernel name at the notebook’s upper right. Choose Select Another Kernel > Python Environments and select the clone’s .venv. Run the first cell again to check the path.
6. Run all cells from the beginning. Expected means: congruent 500 ms and incongruent 600 ms.
Both environments may be named .venv; their folder locations distinguish them. The original environment could also run this notebook, but selecting the clone’s environment checks that the new copy works independently.

For a new project, uv init creates the configuration. For this existing uv project, uv sync uses the configuration to install its environment. Each computer creates its own .venv rather than copying that folder from another computer.

### Later updates

Clone creates the local copy once. After someone adds new commits online, open that existing copy and use Command Palette > **Git: Pull** to retrieve and integrate them. Start with your own edits committed. If the update changes dependency files, run `uv sync` afterward.

Git: Pull updates the project files. `uv sync` updates the Python environment. They perform different tasks. Ask for help if Git reports conflicts.

Before the agent demonstration, return to your original `workshop-project` VS Code window so you continue editing one working copy.

## Agents

Commit a working notebook first. The instructor will specify platform and access requirements.

Explanation prompt:
> Explain how this notebook loads the data, calculates the condition means, and saves its figure. Do not modify files.

Edit prompt:
> Add the number of observations per condition. Preserve the existing analysis. Explain your change before editing. Run the notebook and report what you checked and what you could not verify.

Inspect the Git diff. Check three observations per condition and unchanged means (congruent 500 ms, incongruent 600 ms). Run the notebook yourself if the agent cannot. Commit only after review.

### Let an agent draft an analysis

An agent can draft a whole analysis or a block of code from your instructions. Choose a small plot or question using the practice data and describe the data and output you want. Ask the agent to explain its plan before editing.

Review what it writes:

1. Identify the file or DataFrame it uses and the columns it selects.
2. Follow how the rows are grouped, summarized, and plotted. Ask for explanations of unfamiliar lines.
3. Run the code and inspect the results. For the same condition means, check against 500 ms and 600 ms, with three observations in each condition.
4. Check labels, units, and whether the method answers your question. If you request error bars, specify what they should represent. These toy rows are participant averages rather than individual trials.
5. Review the Git diff before keeping the changes. If the agent cannot run the notebook, run it yourself.

You can learn to follow the logic without memorizing every command. You remain responsible for whether the analysis is appropriate. Successful execution alone does not establish that the results are correct.

## Using the completed reference

The completed reference is another existing uv project. Use it to compare code or recover if you get stuck. Keep it separate from your own `workshop-project`.

1. In another VS Code window, choose File > Open Folder and select `completed-project`.
2. With uv installed, open Terminal > New Terminal and run `uv sync`.
3. Open `analysis.ipynb`, select this folder's `.venv` as the notebook kernel, and run the cells from the top.

It includes filled notebook cells, an equivalent `analysis.py` script, and `example-output.png`. Expected means: congruent 500 ms and incongruent 600 ms. This is an analysis reference, with no Git history or installed environment included. Its original plot title may differ from the title you changed during the Git exercise.

## Sources and practice

- VS Code notebooks: https://code.visualstudio.com/docs/datascience/jupyter-notebooks
- Kernel selection: https://code.visualstudio.com/docs/datascience/jupyter-kernel-management
- VS Code/GitHub: https://code.visualstudio.com/docs/sourcecontrol/github
- uv: https://docs.astral.sh/uv/guides/projects/
- pandas DataFrame: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
- CSV output: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
- Python: https://docs.python.org/3/tutorial/
- Software Carpentry: https://software-carpentry.org/lessons/
- Terminal command reference: https://swcarpentry.github.io/shell-novice/reference.html
