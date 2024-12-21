# Virtual Environment 

#### It is better to run such heavy programs or tasks by creating a virtual environment so that they don't get mixed up or conflicts with the previous packages, specially virtual environments are recommended for packages like tensorFlow etc.

# 1. Install virtual_env:

```javascript
pip install virtualenv
```

# 2. Create virtual env:

```javascript
python -m venv .env_name
```

# 3. Activate the environment (if you're using Windows):

```javascript
.env_name\Scripts\activate
```

if this error comes: .venv\Scripts\activate : File C:\Users\frhan\Desktop\03_Farhan\Brain Tumor Detection\.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system (which I got)

# step1: Run this command in the shell where you are working

```javascript
Set-ExecutionPolicy Unrestricted -Scope Process
```

# step2: Now run the command to activate the virtual_env

```javascript
.env_name\Scripts\activate
```

# 4. Deactivate the environment (run this command when you are done using the environment or you want to move out of the environment):

```javascript
deactivate 
```

