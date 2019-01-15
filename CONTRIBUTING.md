# Contributing to Shitcord

Want to contribute? Great! First, read this page.

## 1. Reporting bugs

Encountered a bug? Report it then! Bug reports are very important to us because they help us improving our
library and make it more usable for everyone.  
**Please follow some simple standards for bug reports:**
- Please completely fill out Shitcord's bug report template.
- Include your code, all necessary details and the full traceback.

## 2. Contributing Code and Docs

Before working on a new feature or a bug, please browse [open issues](https://github.com/itsVale/Shitcord/issues?state=open)
to see whether this issue has been previously discussed. If you're planning major changes, it's always better to
open a issue for them or join our [Discord server](https://discord.gg/HbKGrVT) to discuss the changes you're planning to make.
This way, we can support you and you can get feedback from others and us to see whether these changes are even
appreciated.

### Cloning the project

First of all, you need to fork https://github.com/itsVale/Shitcord to your GitHub account. Then you can clone the project and
start working on it.
```git
git clone https://github.com/<Your-Username>/Shitcord
cd Shitcord
```

### Adding changes

Now that you've got a local copy of Shitcord, start working on it. Create a new branch and check it out.
```git
git checkout -b my_cool_new_feature

# Recommended:
# Install all of Shitcord's requirements inside a venv/pipenv.
```

Please use pylava (`python3 -m pip install -U pylava`) to check your changes by using the command `pylava .`.
You **shouldn't** get any output from this command. If there is output, resolve the issues first before committing.

### Committing your changes

So, you cloned the project, created a feature branch, implemented something and pylava passes? Great!
Now it's time for you to commit your changes:
```git
git commit -m "A descriptive and short message about the changes you made."
```

Assuming your branch is called `my_cool_new_feature`, you need to push it to GitHub in order to create a pull request.
```git
git push origin my_cool_new_feature
```

And then you're all ready! Use GitHub's interface to create a pull request for Shitcord on the `dev` branch,
fill out the template and we'll review it.

**Important: Please do not change Shitcord's version yourself. That's what we do for you.**

### The Contributor Role

For merged pull requests opened by you, you'll get rewarded with the `Contributor` role on our
Discord server.

## 3. Feature requests

Feature requests are highly appreciated! Join our Discord server and DM `Vale#5252` or `Wambo#0800`.
Feel free to discuss your idea with other people before. If the majority would reject the feature, then
we'll most likely do so too.